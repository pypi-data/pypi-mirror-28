import math
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from cassandra import InvalidRequest
import pandas as pd
from cassandra.util import OrderedMapSerializedKey


class CassandraClient:
    """
    A simple client class for access a Cassandra database, controlling
    the disposal of connections and exposing useful methods for batch
    and dataframe (pandas) querying.

    Usage:

    >   with CassandraClient('127.0.0.1', 9042) as client:
    >       rows = client.execute('select * from spam.eggs where foo = %s', ('bar',))

    >   with CassandraClient('127.0.0.1', 9042) as client:
    >       df = client.execute_df('select * from spam.eggs where foo = %s', ('bar',))

    >   with CassandraClient('127.0.0.1', 9042) as client:
    >       client.execute_batch(
    >           ['select * from spam.eggs where foo = %s', 'select * from spam.eggs where foo = %s'],
    >           [('bar',), ('bar',)]
    >       )
    """

    def __init__(self, server, port, keyspace=None, retries=None, username=None, password=None):
        """
        Instantiates a new client. Disposable, so should be instantiated in a `with` block.
        :param server: The server or servers to connect to. Can be a string or list.
        :param port: The port to connect to.
        :param keyspace: Optionally a keyspace to connect to. If not provided, then this should be specified in queries.
        :param retries: Optionally the number of re-tries to attempt before throwing an exception.
        """
        if username is not None:
            auth_provider = PlainTextAuthProvider(username=username, password=password)
        else:
            auth_provider = None
        self._retries = retries
        self._cluster = Cluster(server if type(server) is list else [server], port=port, auth_provider=auth_provider)
        self._keyspace = keyspace

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cluster.shutdown()

    def _retry(self, function, retries=None):
        retries = self._retries if retries is None else retries
        if retries is None:
            return function()

        for i in range(0, retries):
            try:
                return function()
            except Exception as e:
                if i == (retries - 1):
                    raise
                print('WARN: An exception occured, retrying ({})'.format(e))

    def _try_get_session(self):
        return self._retry(lambda: self._cluster.connect(self._keyspace) if self._keyspace else self._cluster.connect(), 10)

    def execute(self, cql, args=None, **kwargs):
        """
        Executes a standard CQL statement, disposing of the relevant connections.
        :param cql: The CQL to be executed, which can contain %s placeholders.
        :param args: An optional tuple of parameters.
        :param kwargs: Any additional named parameters to pass to `session.execute()` in the Cassandra driver.
        :return:
        """
        session = self._try_get_session()
        statement = SimpleStatement(cql)
        if args is None:
            rows = self._retry(lambda: session.execute(statement, **kwargs))
        else:
            rows = self._retry(lambda: session.execute(statement, args, **kwargs))
        session.shutdown()
        return rows

    def _execute_batch(self, session, statements, args, sub_batches, kwargs):
        sub_batch_size = math.ceil(len(statements) / sub_batches)
        for sub_batch in range(0, sub_batches):
            batch = BatchStatement()
            start_index = min(sub_batch * sub_batch_size, len(statements))
            end_index = min((sub_batch + 1) * sub_batch_size, len(statements))
            for i in range(start_index, end_index):
                batch.add(SimpleStatement(statements[i]), args[i])
            self._retry(lambda: session.execute(batch, **kwargs))

    def execute_batch(self, statements, args, **kwargs):
        """
        Executes a batch of CQL statements or, if this fails, attempts to break
        the batch down into smaller chunks.
        :param statements: A sequence of CQL strings to execute, which can contain %s placeholders.
        :param args: A sequence of parameter tuples, of the same length as `statements`.
        :param kwargs: Any additional named parameters to pass to `session.execute()` in the Cassandra driver.
        :return:
        """
        session = self._try_get_session()
        try:
            for sub_batches in range(1, len(statements) + 1):
                try:
                    self._execute_batch(session, statements, args, sub_batches, kwargs)
                    return
                except InvalidRequest:
                    if len(statements) == sub_batches:
                        raise
                    print(
                        """
                        An error occured on a batch of length {}, split into {} sub_batches.
                        Trying again, with more sub_batches.
                        """.format(len(statements), sub_batches)
                    )
        finally:
            session.shutdown()

    def execute_df(self, cql, args=None, fetchsize=1000, **kwargs):
        """
        Executes the cql and returns the resulting rows as a dataframe, expanding maps as additional columns.
        Useful if map<> fields are being selected that need to be columns in the resultant dataframe.
        :param cql:
        :param args:
        :param fetchsize:
        :param kwargs: Any additional named parameters to pass to `session.execute()` in the Cassandra driver.
        :return:
        """
        session = self._try_get_session()
        statement = SimpleStatement(cql, fetch_size=fetchsize)
        if args is None:
            result_set = self._retry(lambda: session.execute(statement, **kwargs))
        else:
            result_set = self._retry(lambda: session.execute(statement, args, **kwargs))

        results = []
        column_names = set(result_set.column_names)
        for row in result_set:
            result = {}
            for i in range(0, len(result_set.column_names)):
                cell = row[i]
                if type(cell) is OrderedMapSerializedKey:
                    for key in cell.keys():
                        column_name = '{}_{}'.format(result_set.column_names[i], key)
                        column_names.add(column_name)
                        result[column_name] = cell.get(key)
                else:
                    result[result_set.column_names[i]] = cell
            results.append(result)
        session.shutdown()

        return pd.DataFrame(data=results)
