from unittest.mock import Mock
from legacy import Processor

db_connector_mock = Mock()

processor_test = Processor(db_connector=db_connector_mock)


def test_parse_date():
    date_string = '10/10/10'
    date_result = processor_test.parse_date(date_string)
    assert date_result is not None

def test_parse_date2():
    date_string = '12,,132123232'
    date_result = processor_test.parse_date(date_string)
    assert date_result is None

def test_parse_date3():
    date_string = '10 Jan 2019'
    date_result = processor_test.parse_date(date_string)
    assert date_result is not None

def test_parse_date4():
    date_string = 'Today is January 1, 2047 at 8:21:00AM'
    date_result = processor_test.parse_date(date_string)
    assert date_result is not None
