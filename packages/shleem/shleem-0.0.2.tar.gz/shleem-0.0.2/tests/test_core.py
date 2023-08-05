"""Testing core functionalities of the shleem package."""

from shleem import (
    DataSource,
    DataTap,
)


def test_data_source():
    some_id = "232"
    some_source = DataSource(identifier=some_id)
    assert some_source.identifier == some_id
    assert some_source.source_type == 'unspecified'
    assert some_source.__repr__() == 'DataSource: {}'.format(some_id)

    some_type = "ShleemDB"
    source2 = DataSource(identifier=some_id, source_type=some_type)
    assert source2.identifier == some_id
    assert source2.source_type == some_type


def test_data_tap():
    class ShleemDBQuery(DataTap):
        def __init__(self, query):
            super().__init__(
                identifier="ShleemDB."+str(query), source_type="ShleemDB")
            self.query = query
        def tap(self):
            return []
    shuq = ShleemDBQuery({'a': 4})
    assert shuq.source_type == "ShleemDB"
    assert shuq.__repr__() == "DataTap: ShleemDB.{'a': 4}"
    assert shuq.tap() == []
