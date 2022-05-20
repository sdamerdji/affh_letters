import utils
import city


def test_get_exclusionary_cities():
    exclusionary_cities = utils.get_exclusionary_cities()
    assert exclusionary_cities
    assert 'Los Altos' in exclusionary_cities
    assert 'Piedmont' in exclusionary_cities
    assert 'East Palo Alto' not in exclusionary_cities
    assert 'San Jose' not in exclusionary_cities


def test_city_factory():
    cf = city.CityFactory(utils.get_obi_data(), None)
    los_altos = cf.build('Los Altos')
    assert los_altos.pct_white == 0.532
