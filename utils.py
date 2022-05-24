import pandas as pd

"""Dataframe with Bay Area segregation statistics. Courtesy of Othering and Belonging Institute (hence OBI)"""
OBI_DATA = None
ZILLOW_DATA = None
SFZ_DATA = None
SFZ_HO_DATA = None


def get_obi_data():
    """Load OBI data only once."""
    global OBI_DATA
    if OBI_DATA is not None:
        return OBI_DATA
    OBI_DATA = pd.read_excel('./data/bay.area_divergence.download.xlsx',
                             sheet_name='Inter-Municipal Divergence')
    return OBI_DATA


def get_sfz_data():
    """Load OBI data only once."""
    global SFZ_DATA
    if SFZ_DATA is not None:
        return SFZ_DATA
    SFZ_DATA = pd.read_csv('./data/sfr_pct.csv', index_col=0)
    return SFZ_DATA


def get_sfz_ho_data():
    """Load OBI data only once."""
    global SFZ_HO_DATA
    if SFZ_HO_DATA is not None:
        return SFZ_HO_DATA
    SFZ_HO_DATA = pd.read_csv('./data/sfr_ho_pct.csv', index_col=0)
    return SFZ_HO_DATA


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


def get_non_obi_cities():
    cities = ['Atherton', 'Brisbane', 'Colma', 'Cotati', 'Fairfax', 'Larkspur', 'Monte Sereno', 'Ross', 'Sausalito',
              'St. Helena', 'Woodside', 'Yountville']
    return cities

def get_exclusionary_non_obi_cities():
    df = pd.read_csv('./data/income.csv')
    non_obi = get_non_obi_cities()
    non_obi_columns = [c for c in df.columns if any((city in c for city in get_non_obi_cities()))]
    mean_income = df[df['Label (Grouping)'] == 'Mean income (dollars)'].T
    mean_income = mean_income.loc[non_obi_columns]
    household_incomes = mean_income[mean_income.index.str.contains('Household')]
    household_incomes.index = household_incomes.index.str.split(',').str[0].str.split().str[:-1].str.join(' ')
    household_incomes.columns = ['avg_income']
    # Get top 5%er cities
    household_incomes['avg_income'] = household_incomes['avg_income'].str.replace(',', '').astype(float)
    household_incomes = household_incomes[household_incomes.avg_income > 221572]

    df = pd.read_csv('./data/race.csv')
    df.iloc[:, 0] = ['Total', '', 'White', 'Black', 'Asian'] + [''] * 66
    df = df.T
    df.index = df.index.str.split(',').str[0].str.split().str[:-1].str.join(' ')
    df.columns = df.iloc[0]
    df = df[[c in household_incomes.index for c in df.index]]
    df = df[[c for c in df.columns if c]]

    result = pd.merge(df, household_incomes, left_index=True, right_index=True)
    return result

def get_abag_data(city, sheet='POPEMP-21'):
    city = '_'.join(city.split(' '))
    subdir = f'./data/ABAG-MTC Housing Needs Data Packets/{city}'
    return pd.read_excel(f'{subdir}/ABAG_MTC_Housing_Needs_Data_Workbook_{city}.xlsx',
                         sheet_name=sheet, skiprows=3)


def get_pct_li(city):
    """Return percent of the city that's low income (encompassing ELI, VLI, & LI)."""
    df = get_abag_data(city, 'POPEMP-21')
    df.set_index('Group', inplace=True)
    total_pop = df.sum().sum().item()
    li_pop = df.sum(axis=1)[:3].sum().item()
    return round(li_pop / total_pop, 3)


def get_racial_change(city):
    df = get_abag_data(city, 'POPEMP-02')
    df.set_index('Year', inplace=True)
    deltas = df.loc[2019] - df.loc[2010]
    black, white, brown = deltas[2], deltas[3], deltas[5]
    return black, white, brown


def get_city_rhna_targets(city):
    df = pd.read_excel('./data/rhna.xlsx', skiprows=3)
    df.set_index('Jurisdiction', inplace=True)
    vli, li, m, am, total = df.loc[city]
    return int(vli), int(li), int(m), int(am), int(total)


def get_city_sfz_pct(city):
    df = get_sfz_data()
    if city == 'Foster City':
        city = 'Foster'
    return df.loc[''.join(city.split())].values.item()


def get_city_sfz_ho_pct(city):
    df = get_sfz_ho_data()
    if city == 'Foster City':
        city = 'Foster'
    if ''.join(city.split()) not in df.index.values:
        print(city, " has no high opportunity areas.")
        return 0
    return round(df.loc[''.join(city.split())].values.item(), 1)
