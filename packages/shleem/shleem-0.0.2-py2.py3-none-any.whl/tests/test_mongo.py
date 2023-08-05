"""Testing MongoDB data sources for the shleem python package."""

import pytest
from strct.hash import stable_hash

import shleem


def test_mongo_sources():

    # defining a MongoDB server source
    shleem_test_server = shleem.mongodb.server("shleem_test_server")
    assert repr(shleem_test_server) == (
        "MongoDB server DataSource: shleem_test_server")
    assert shleem_test_server.identifier == 'shleem_test_server'
    assert shleem_test_server.server_name == 'shleem_test_server'

    # db source
    test_db = shleem_test_server['shleem_test']
    test_db2 = shleem_test_server.shleem_test
    test_db3 = shleem_test_server.db('shleem_test')
    assert test_db == test_db2
    assert test_db2 == test_db3
    assert repr(test_db) == (
        "MongoDB database DataSource: shleem_test_server.shleem_test")
    assert test_db.identifier == 'shleem_test_server.shleem_test'
    assert test_db.db_name == 'shleem_test'

    # collection source
    examp = test_db['example_data_collection']
    examp2 = test_db.example_data_collection
    examp3 = test_db.collection('example_data_collection')
    assert examp == examp2
    assert examp == examp3
    assert repr(examp) == (
        "MongoDB collection DataSource: shleem_test_server.shleem_test"
        ".example_data_collection")
    assert examp.identifier == (
        'shleem_test_server.shleem_test.example_data_collection')
    assert examp.collection_name == 'example_data_collection'

    # query data tap
    query = {"borough": "Queens"}
    queens_people = examp.query(query)
    assert repr(queens_people) == (
        "MongoDB query DataSource: shleem_test_server.shleem_test"
        ".example_data_collection.{}".format(
            stable_hash(query)))
    assert queens_people.identifier == (
        "shleem_test_server.shleem_test.example_data_collection.{}".format(
            stable_hash(query)))
    assert queens_people.source_type == 'MongoDB'

    # checking the client
    client = shleem_test_server._get_connection()
    some_doc = client['shleem_test']['example_data_collection'].find_one()
    assert some_doc['restaurant_id'] == '30112340'

    # tapping the source
    cursor = queens_people.tap()
    other_doc = cursor.next()
    assert other_doc['restaurant_id'] == '40356068'

    def getter(field_name):
        return lambda **kwargs: kwargs[field_name]

    # parameterized query
    param_query_dict = {"address.zipcode": {
        "$gte": getter("min_val"), "$lte": getter("max_val")
    }}
    # first without identifier, so we check all the code!
    zipcode_range = examp.query(param_query_dict)
    zipcode_range = examp.query(
        query_dict=param_query_dict, identifier="zipcode_range")
    min_val = 11249
    max_val = 11300
    cursor = zipcode_range.tap(min_val=str(min_val), max_val=str(max_val))
    documents = [doc for doc in cursor]
    assert len(documents) == 163
    for doc in documents:
        zipcode = doc['address']['zipcode']
        assert int(zipcode) >= min_val and int(zipcode) <= max_val

    # with skip and limit
    some_limit = 17
    zipcode_range2 = examp.query(
        query_dict=param_query_dict, skip=10, limit=some_limit)
    cursor = zipcode_range2.tap(min_val=str(min_val), max_val=str(max_val))
    documents = [doc for doc in cursor]
    assert len(documents) == some_limit
    for doc in documents:
        zipcode = doc['address']['zipcode']
        assert int(zipcode) >= min_val and int(zipcode) <= max_val

    # aggregation data tap
    agg_pipeline = [
        {'$group': {'_id': '$borough', 'count': {'$sum': 1}}}
    ]
    borough_counts = examp.aggregation(agg_pipeline)
    exp_id = (
        'shleem_test_server.shleem_test.example_data_collection.'
        '1216216893277084555')
    assert borough_counts.identifier == exp_id
    exp_repr = "MongoDB aggregation DataSource: {}".format(exp_id)
    assert repr(borough_counts) == exp_repr

    # tap the source 2: the aggregation strikes back
    cursor = borough_counts.tap()
    res = {doc['_id']: doc['count'] for doc in cursor}
    assert res['Missing'] == 51
    assert res['Queens'] == 5656

    # parameterized aggregation
    param_agg = [
        {"$match": {"address.zipcode": {"$gte": "11695"}}},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": {"name": "$name", "address": "$address"},
            "sum_score": {"$sum": "$grades.score"},
            "num_score": {"$sum": 1}
        }},
        {"$project": {
            "_id": 1, "avg_score": {"$divide": ["$sum_score", "$num_score"]}
        }},
        {"$match": {
            "avg_score": {
                "$gt": lambda **kwargs: kwargs["avg_score_threshold"]
            }
        }}
    ]
    # first without and identifier, so we check all the code handling that!
    by_avg_score_threshold = examp.aggregation(param_agg)
    # now with an identifier!
    by_avg_score_threshold = examp.aggregation(
        param_agg, "restaurant_by_avg_score_threshold")
    thresh = 13.5
    cursor = by_avg_score_threshold.tap(avg_score_threshold=thresh)
    for doc in cursor:
        assert doc['avg_score'] > thresh

    # parameterized aggregation with a callable in a list
    param_agg2 = [
        {"$match": {"address.zipcode": {"$gte": "11695"}}},
        {"$unwind": "$grades"},
        {"$group": {
            "_id": {"name": "$name", "address": "$address"},
            "sum_score": {"$sum": "$grades.score"}
        }},
        {"$project": {
            "_id": 1,
            "avg_score": {"$divide": ["$sum_score", getter("normalizer")]}
        }},
        {"$match": {
            "avg_score": {
                "$gt": lambda **kwargs: kwargs["avg_score_threshold"]
            }
        }}
    ]
    by_norm_score_threshold = examp.aggregation(param_agg2)
    thresh2 = 13.5
    cursor = by_norm_score_threshold.tap(
        avg_score_threshold=thresh2, normalizer=4)
    all_res = [doc for doc in cursor]
    assert len(all_res) == 2
    for doc in all_res:
        assert doc['avg_score'] > thresh2


def test_missing_server():
    missing_server = shleem.mongodb.server("missing_server")
    with pytest.raises(ValueError):
        client = missing_server._get_connection()
        assert not client.database_names
