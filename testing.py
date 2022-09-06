import utils
from city import CityFactory
import pandas as pd


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
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    los_altos = cf.build('Los Altos')
    assert los_altos.pct_white > 0.50
    assert los_altos.home_price > 4000000


def test_city_cost_methods():
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
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
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    los_altos_hills = cf.build('Los Altos Hills')
    assert los_altos_hills.how_much_whiter() * 100 > 5
    assert los_altos_hills.how_much_less_black() * 100 > 5
    assert los_altos_hills.how_much_less_brown() * 100 > 5


def test_city_methods_another_city():
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    cupertino = cf.build('Cupertino')
    assert 200000 < cupertino.salary_to_buy() < 500000
    assert cupertino.income_percent() == '2%'


def test_non_obi_cities_city_factor():
    """Ensure CityFactor works for non obi cities."""
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    belvedere = cf.build('Belvedere')
    assert 500000 < belvedere.salary_to_buy()
    assert belvedere.one_percenter_city()
    assert belvedere.exceeds_castle()
    assert belvedere.exceeds_private_island()
    assert belvedere.cost_relative_to_country() > 9
    assert belvedere.min_wage_jobs() > 10
    assert belvedere.income_percent() == '1%'
    assert 100 < belvedere.affh_needed_li_homes()


def test_rhna_targets():
    vli, li, m, am, tot = utils.get_city_rhna_targets('Los Altos')
    assert (vli + li + m + am) == tot
    vli, li, m, am, tot = utils.get_city_rhna_targets('Mountain View')
    assert (vli + li + m + am) == tot


def test_li_pct():
    assert 1 < utils.get_pct_li('Los Altos') * 100 < 20


def test_racial_change():
    df = utils.get_racial_change('Cupertino')


def test_sfr_pct_data():
    df = utils.get_sfz_data()
    assert df.size


def test_get_sfz_for_city():
    for city in utils.get_exclusionary_cities():
        assert utils.get_city_sfz_pct(city)


def test_sfr_ho_pct_data():
    df = utils.get_sfz_ho_data()
    assert df.size


def test_get_sfz_ho_for_city():
    for city in utils.get_exclusionary_cities():
        if city != 'Morgan Hill': # Morgan Hill has no high opportunity areas.
            assert utils.get_city_sfz_ho_pct(city)


def test_segregation_rankings():
    cities = utils.get_exclusionary_cities()
    df = utils.get_obi_data()
    cities = df[df['Level of Segregation'] == 'High Segregation']

    # And just pick the rich ones
    cities = cities[cities['Median Household Income (2019 ACS)'] > df['Median Household Income (2019 ACS)'].mean()]
    cities = cities['Cities/Towns'].values.tolist()


def test_non_obi_cities():
    cities = utils.get_exclusionary_non_obi_cities()
    assert len(cities)
    assert 'Belvedere' in cities
    assert 'Atherton' in cities


def test_one_pctr_cities():
    cities = utils.get_exclusionary_cities()
    result = []
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    for city in cities:
        c = cf.build(city)

        if c.one_percenter_city():
            print(city, c.pct_ho_sfz())

def test_two_pctr_cities():
    cities = utils.get_exclusionary_cities()
    result = []
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    for city in cities:
        c = cf.build(city)

        if c.two_percenter_city():
            print(city, c.income_percent(), c.pct_ho_sfz())

        elif c.pct_ho_sfz() > 95:
            print('hi')
            print(city, c.income_percent(), c.pct_ho_sfz())

def test_city_contacts():
    cities = utils.get_exclusionary_cities()
    print(len(cities))
    contactable = pd.read_csv('./letter_data/emails.csv', names=['city', 'emails'])
    assert set(cities) <= set(contactable.city)

def test_city_black_attrition():
    cities = utils.get_exclusionary_cities()
    cf = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
    most = 0
    most_name = None
    for city in cities:
        c = cf.build(city)
        most = max(most, c.brown_population_attrition())
        if most == c.brown_population_attrition():
            most_name = city
    print(most)
    print(most_name)

