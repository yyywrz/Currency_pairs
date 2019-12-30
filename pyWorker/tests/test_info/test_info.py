from info import helper


def test_ref():
    test_codes=['CNY','JPY','USD','EUR']
    test_regions=['China','Japan','United States','Spain']
    test_currencies=['Chinese Renminbi','Japanese Yen','US Dollar','Euro']
    false_data=['Kunming','123','wd23d23','32wqd']
    test_codes = test_codes + false_data
    test_regions = test_regions + false_data
    test_currencies = test_currencies + false_data
    ans = [
        {'Currency Code': 'CNY', 'Currency Name': 'Chinese Renminbi', 'Region': 'China'},
        {'Currency Code': 'JPY', 'Currency Name': 'Japanese Yen', 'Region': 'Japan'},
        {'Currency Code': 'USD', 'Currency Name': 'US Dollar', 'Region': 'United States'},
        {'Currency Code': 'EUR', 'Currency Name': 'Euro', 'Region': 'Europe'},
        'invalid',
        'invalid',
        'invalid',
        'invalid']

    ref = helper.ref()
    for i in range(0,8):
        instance = ans[i]
        print(instance)
        assert instance == ref.code(test_codes[i])
        if test_regions[i] == 'Spain':
            assert {'Currency Code': 'EUR', 'Currency Name': 'Euro', 'Region': 'Spain'}\
                == ref.region(test_regions[i])
        else:
            assert instance == ref.region(test_regions[i])
        assert instance == ref.currency_name(test_currencies[i])
