"""MongoDB data sources."""

import os
import copy
import json
import urllib.parse
from functools import lru_cache


from pymongo import MongoClient
from strct.hash import stable_hash

from shleem.core import (
    DataSource,
    DataTap,
)
from shleem.shared import SHLEEM_DIR_PATH


MONGODB_SOURCE_TYPE = 'MongoDB'
SHLEEM_MONGODB_CRED_FNAME = 'mongodb_credentials.json'
SHLEEM_MONGODB_CRED_FPATH = os.path.join(
    SHLEEM_DIR_PATH, SHLEEM_MONGODB_CRED_FNAME)
MONGO_CRED_FILE_MSG = (
    'MongoDB credentials for shleem should be set by a credentials file. The '
    'credentials file should be named mongodb_credentials.json, placed in the '
    '.shleem folder located in your home folder and constructed in the '
    'following format:\n'
    '{\n'
    '    "servers": {\n'
    '        "production_data_store": {\n'
    '            "hosts": ["ds192763.mlab.com:51829"],\n'
    '             "username": "shleem_reader",\n'
    '             "password": "8d728673tfi8h723yds"\n'
    '        }\n'
    '    }\n'
    '}'
)


def _get_cred():
    """Returns MongoDB credentials dict."""
    try:
        with open(SHLEEM_MONGODB_CRED_FPATH, 'r') as mongo_cred_file:
            return json.load(mongo_cred_file)
    except FileNotFoundError:  # pragma: no cover
        print(MONGO_CRED_FILE_MSG)


class MongoDBSource(DataSource):
    """A MongoDB data source.

    Arguments
    ---------
    identifier : str
        A string identifier unique to this data source.
    """

    def __init__(self, identifier):
        DataSource.__init__(
            self, identifier=identifier, source_type=MONGODB_SOURCE_TYPE)


class MongoDBServer(MongoDBSource):
    """A MongoDB server data source.

    Arguments
    ---------
    server_name : str
        The name of this MongoDB server.
    """

    def __init__(self, server_name):
        MongoDBSource.__init__(self, identifier=server_name)
        self.server_name = server_name

    def __repr__(self):
        return "MongoDB server DataSource: {}".format(self.identifier)

    def __getitem__(self, db_name):
        return self.db(db_name)

    def __getattr__(self, db_name):
        return self.db(db_name)

    @lru_cache(maxsize=1024)
    def db(self, db_name):
        """Returns a MongoDBDataBase object with the given name, hosted on this
        MongoDB server."""
        return MongoDBDatabase(self, db_name)

    @staticmethod
    def _mongodb_uris(usr, pwd, hosts):
        parsed_usr = urllib.parse.quote_plus(usr)
        parsed_pwd = urllib.parse.quote_plus(pwd)
        return [
            "mongodb://{usr}:{pwd}@{host}".format(
                usr=parsed_usr, pwd=parsed_pwd, host=host)
            for host in hosts
        ]

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo client connected to this server.

        Returns
        -------
        pymongo.MongoClient
            Returns a pymongo.MongoClient object with reading permissions
            connected to this server.
        """
        cred = copy.deepcopy(_get_cred())
        try:
            server_cred = cred['servers'][self.server_name]
            uris = MongoDBServer._mongodb_uris(
                usr=server_cred.pop('username'),
                pwd=server_cred.pop('password'),
                hosts=server_cred.pop('hosts'),
            )
            return MongoClient(host=uris, **server_cred)
        except KeyError:
            msg = ("The server {} is missing for shleem's MongoDB credentials"
                   "file.\n".format(self.server_name) + MONGO_CRED_FILE_MSG)
            raise ValueError(msg)


@lru_cache(maxsize=1024)
def server(server_name):
    """Returns a MongoDBServer object with the given name."""
    return MongoDBServer(server_name)


def _add_servers_attr(module):
    cred = _get_cred()
    for server_name in cred['servers']:
        setattr(module, server_name, server(server_name))


class MongoDBDatabase(MongoDBSource):
    """A specific MongoDB database data source.

    Arguments
    ---------
    mongodb_server : MongoDBServer
        The MongoDB server this database is located on.
    db_name : str
        The name of the database.
    """

    def __init__(self, mongodb_server, db_name):
        identifier = mongodb_server.identifier + '.' + db_name
        MongoDBSource.__init__(self, identifier=identifier)
        self.mongodb_server = mongodb_server
        self.db_name = db_name

    def __repr__(self):
        return "MongoDB database DataSource: {}".format(self.identifier)

    @lru_cache(maxsize=1024)
    def __getitem__(self, collection_name):
        return MongoDBCollection(self, collection_name)

    def __getattr__(self, collection_name):
        return self[collection_name]

    def collection(self, collection_name):
        """Returns a MongoDBCollection data source object with the given name,
        located at this MongoDB database."""
        return self[collection_name]

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo.database.Database object connected to this
        database."""
        return self.mongodb_server._get_connection()[self.db_name]


class MongoDBCollection(MongoDBSource):
    """A specific MongoDB collection data source.

    Arguments
    ---------
    mongodb_db : MongoDBDatabase
        The MongoDB database this collection is located on.
    collection_name : str
        The name of the collection.
    """

    def __init__(self, mongodb_db, collection_name):
        identifier = mongodb_db.identifier + '.' + collection_name
        MongoDBSource.__init__(self, identifier=identifier)
        self.mongodb_db = mongodb_db
        self.collection_name = collection_name

    def __repr__(self):
        return "MongoDB collection DataSource: {}".format(self.identifier)

    def query(self, query_dict, identifier=None, projection=None, skip=None,
              limit=None):
        """Returns a MongoDBQuery source object representing a query ran
        against this collection.

        Arguments
        ---------
        query_dict : dict
            A pymongo-compliant MongoDB query.
        identifier : str, optional
            A string identifier unique to this query. If none is given, a
            stable hash function is used to compute a good candidate.
        projection : list or dict, optional
            A list of field names that should be returned in the result set or
            a dict specifying the fields to include or exclude.
        skip : int, optional
            the number of documents to omit (from the start of the result set)
            when returning the results.
        limit : int, optional
            the maximum number of results to return.
        """
        return MongoDBQuery(self, query=query_dict, identifier=identifier,
                            projection=projection, skip=skip, limit=limit)

    def aggregation(self, aggregation_pipeline, identifier=None):
        """Returns a MongoDBAggregation source object representing an
        aggregation ran against this collection.

        Arguments
        ---------
        aggregation_piepline : list
            A pymongo-compliant MongoDB aggregation given as a list of dicts.
        identifier : str, optional
            A string identifier unique to this aggregation. If none is given, a
            stable hash function is used to compute a good candidate.
        """
        return MongoDBAggregation(
            self, aggregation_pipeline=aggregation_pipeline,
            identifier=identifier)

    @lru_cache(maxsize=2)
    def _get_connection(self):
        """Returns a pymongo.collection.Collection object connected to this
        database."""
        return self.mongodb_db._get_connection()[self.collection_name]


def _clean_query_helper(obj):
    if isinstance(obj, dict):
        for key in obj:
            if callable(obj[key]):
                obj[key] = obj[key].__name__
            elif isinstance(obj[key], (dict, list, tuple)):
                obj[key] = _clean_query_helper(obj[key])
    if isinstance(obj, (list, tuple)):
        new_list = []
        for item in obj:
            if callable(item):
                new_list.append(item.__name__)
            elif isinstance(item, (dict, list, tuple)):
                new_list.append(_clean_query_helper(item))
            else:
                new_list.append(item)
        return new_list
    return obj


def _clean_query_from_callables(query):
    new = copy.deepcopy(query)
    return _clean_query_helper(new)


def _resolve_helper(obj, **kwargs):
    if isinstance(obj, dict):
        for key in obj.keys():
            if callable(obj[key]):
                obj[key] = obj[key](**kwargs)
            if isinstance(obj[key], (dict, list, tuple)):
                obj[key] = _resolve_helper(obj[key], **kwargs)
        return obj
    # else, it's a list or a tuple
    # if isinstance(obj, (list, tuple)):
    new_list = []
    for item in obj:
        if callable(item):
            new_list.append(item(**kwargs))
        elif isinstance(item, (dict, list, tuple)):
            new_list.append(_resolve_helper(item, **kwargs))
        else:
            new_list.append(item)
    return new_list


def _resolve_query(query, **kwargs):
    resolved_query = copy.deepcopy(query)
    return _resolve_helper(resolved_query, **kwargs)


class MongoDBQuery(MongoDBSource, DataTap):
    """A specific MongoDB query data source.

    Objects of this class should not be instantiated directly, but rather using
    the query method of shleem.MongoDBCollection objects.

    Arguments
    ---------
    mongodb_collection : MongoDBCollection
        The MongoDB collection this query will be ran against.
    query : dict
        A pymongo-compliant MongoDB query.
    identifier : str, optional
        A string identifier unique to this query. If none is given, a stable
        hash function is used to compute a good candidate.
    projection : list or dict, optional
        A list of field names that should be returned in the result set or a
        dict specifying the fields to include or exclude.
    skip : int, optional
        the number of documents to omit (from the start of the result set)
        when returning the results.
    limit : int, optional
        the maximum number of results to return.
    """

    def __init__(self, mongodb_collection, query, identifier=None,
                 projection=None, skip=None, limit=None):
        if identifier is None:
            try:
                identifier = str(abs(stable_hash(query)))
            except TypeError:
                clean_query = _clean_query_from_callables(query)
                identifier = str(abs(stable_hash(clean_query)))
        identifier = mongodb_collection.identifier + '.' + identifier
        super().__init__(identifier=identifier)
        self.mongodb_collection = mongodb_collection
        self.query = query
        self.projection = projection
        if skip is None:
            skip = 0
        if limit is None:
            limit = 0  # pargma: no cover
        self.skip = skip
        self.limit = limit

    def __repr__(self):
        return "MongoDB query DataSource: {}".format(self.identifier)

    def tap(self, **kwargs):
        col_obj = self.mongodb_collection._get_connection()
        query = _resolve_query(self.query, **kwargs)
        return col_obj.find(
            filter=query,
            projection=self.projection,
            skip=self.skip,
            limit=self.limit,
        )


class MongoDBAggregation(MongoDBSource, DataTap):
    """A specific MongoDB aggregation data source.

    Arguments
    ---------
    mongodb_collection : MongoDBCollection
        The MongoDB collection this query will be ran against.
    aggregation_pipeline : list
        A pymongo-compliant MongoDB aggregation pipelien, given as a list of
        dicts.
    identifier : str, optional
        A string identifier unique to this aggregation. If none is given, a
        stable hash function is used to compute a good candidate.
    """

    def __init__(self, mongodb_collection, aggregation_pipeline,
                 identifier=None):
        if identifier is None:
            try:
                identifier = str(abs(stable_hash(
                    aggregation_pipeline)))
            except TypeError:
                clean_pipe = _clean_query_from_callables(
                    aggregation_pipeline)
                identifier = str(abs(stable_hash(clean_pipe)))
        identifier = mongodb_collection.identifier + '.' + identifier
        super().__init__(identifier=identifier)
        self.mongodb_collection = mongodb_collection
        self.aggregation_pipeline = aggregation_pipeline

    def __repr__(self):
        return "MongoDB aggregation DataSource: {}".format(self.identifier)

    def tap(self, **kwargs):
        col_obj = self.mongodb_collection._get_connection()
        pipe = _resolve_query(self.aggregation_pipeline, **kwargs)
        return col_obj.aggregate(pipe)
