import pandas as pd

"""Dataframe with Bay Area segregation statistics. Courtesy of Othering and Belonging Institute (hence OBI)"""
OBI_DATA = None
ZILLOW_DATA = None


def get_obi_data():
    """Load OBI data only once."""
    global OBI_DATA
    if OBI_DATA is not None:
        return OBI_DATA
    OBI_DATA = pd.read_excel('./data/bay.area_divergence.download.xlsx',
                             sheet_name='Inter-Municipal Divergence')
    return OBI_DATA


def get_zillow_data():
    """Load Zillow data only once."""
    global ZILLOW_DATA
    if ZILLOW_DATA is not None:
        return ZILLOW_DATA
    df = pd.read_csv('./data/zillow.csv')
    df = simplify_zillow_data(df)
    ZILLOW_DATA = df
    return ZILLOW_DATA


def simplify_zillow_data(df):
    """Only return Californian cities with their latest home prices & prices from the start of RHNA5."""
    df = df[df.State == 'CA'][['RegionName', '2014-01-31', '2022-04-30']].copy()
    df.rename(columns={'RegionName': 'City'}, inplace=True)
    return df


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


def get_abag_data(city):
    city = '_'.join(city.split(' '))
    subdir = f'./data/ABAG-MTC Housing Needs Data Packets/{city}'
    return pd.read_excel(f'{subdir}/ABAG_MTC_Housing_Needs_Data_Workbook_{city}.xlsx',
                         sheet_name='POPEMP-21', skiprows=3)