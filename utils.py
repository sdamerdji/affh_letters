import pandas as pd

"""Dataframe with Bay Area segregation statistics. Courtesy of Othering and Belonging Institute (hence OBI)"""
OBI_DATA = None


def get_obi_data():
    """Load OBI data only once."""
    global OBI_DATA
    if OBI_DATA is not None:
        return OBI_DATA
    OBI_DATA = pd.read_excel('./data/bay.area_divergence.download.xlsx',
                             sheet_name='Inter-Municipal Divergence')
    return OBI_DATA


def get_exclusionary_cities():
    """Return list of city names that OBI labels as high intercity segregation & above avg income & home price."""
    df = get_obi_data()

    # Get cities that are racially or socioeconomically segregated from neighboring cities
    cities = df[df['Level of Segregation'] == 'High Segregation']

    # And just pick the rich ones
    cities = cities[cities['Median Household Income (2019 ACS)'] > df['Median Household Income (2019 ACS)'].mean()]
    cities = cities['Cities/Towns'].values.tolist()
    cities.sort()
    return cities


