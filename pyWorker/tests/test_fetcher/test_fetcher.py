import pytest
from fetcher import fetcher

def test_fetcher():
    data = fetcher.fetcher('USD')
    print(data)

if __name__=="__main__":
    test_fetcher()