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


def test_city_cost_methods():
    cf = city.CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    los_altos = cf.build('Los Altos')
    assert 500000 < los_altos.salary_to_buy() < 700000
    assert los_altos.one_percenter_city()
    assert los_altos.exceeds_castle()
    assert los_altos.exceeds_private_island()
    assert los_altos.cost_relative_to_country() > 9
    assert los_altos.min_wage_jobs() > 10
    assert los_altos.income_percent() == '1%'
    assert 1000 < los_altos.affh_needed_li_homes() < 10000


def test_city_race_disparity_methods():
    cf = city.CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    los_altos_hills = cf.build('Los Altos Hills')
    assert los_altos_hills.how_much_whiter() * 100 > 5
    assert los_altos_hills.how_much_less_black() * 100 > 5
    assert los_altos_hills.how_much_less_brown() * 100 > 5


def test_city_methods2():
    cf = city.CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    cupertino = cf.build('Cupertino')
    assert 200000 < cupertino.salary_to_buy() < 500000
    assert cupertino.income_percent() == '2%'


def test_rhna_targets():
    vli, li, m, am, tot = utils.get_city_rhna_targets('Los Altos')
    assert (vli + li + m + am) == tot
    vli, li, m, am, tot = utils.get_city_rhna_targets('Mountain View')
    assert (vli + li + m + am) == tot


def test_li_pct():
    assert 1 < utils.get_pct_li('Los Altos') * 100 < 20

def test_racial_change():
    df = utils.get_racial_change('Cupertino')