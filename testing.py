import utils
import city


def test_get_exclusionary_cities():
    exclusionary_cities = utils.get_exclusionary_cities()
    assert exclusionary_cities
    assert 'Los Altos' in exclusionary_cities
    assert 'Piedmont' in exclusionary_cities
    assert 'East Palo Alto' not in exclusionary_cities
    assert 'San Jose' not in exclusionary_cities


def test_get_zillow_data():
    zillow = utils.get_zillow_data()
    assert zillow.size
    exclusionary_cities = utils.get_exclusionary_cities()
    for city in exclusionary_cities:
        assert city in zillow.City.values
        

def test_get_abag_data():
    la = utils.get_abag_data('Los Altos')
    lah = utils.get_abag_data('Los Altos Hills')
    exclusionary_cities = utils.get_exclusionary_cities()
    for city in exclusionary_cities:
        df = utils.get_abag_data(city)
        assert df.size
        assert 'Group' in df.columns


def test_city_factory():
    cf = city.CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    los_altos = cf.build('Los Altos')
    assert los_altos.pct_white > 0.50
    assert los_altos.home_price > 4000000
    assert los_altos.salary_to_buy() > 500000
    assert los_altos.one_percenter_city()
    assert los_altos.exceeds_castle()
    assert los_altos.exceeds_private_island()
    assert los_altos.cost_relative_to_country() > 9
    assert los_altos.min_wage_jobs() > 15
    assert los_altos.how_much_whiter() * 100 > 5
