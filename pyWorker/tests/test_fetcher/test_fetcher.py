import pytest
from fetcher import fetcher
from time import gmtime, strftime

def test_fetcher():
    testdata=['USD','CNY']
    for code in testdata:
        data = fetcher.fetcher(code)
        verify_fetcher(data)
    assert False == fetcher.fetcher('123')

def test_instance():
    verify_fetcher(fetcher.instance())




def verify_fetcher(data):
    assert 52 == len(data['rates'])
    assert strftime("%Y-%m-%d", gmtime()) == data['date']