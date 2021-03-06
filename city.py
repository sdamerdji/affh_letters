import math
import utils


class CityFactory:
    def __init__(self, obi_df, price_df):
        self._obi_df = obi_df
        self._price_df = price_df
        self._non_obi_cities = utils.get_non_obi_cities()
        self._non_obi_df = utils.get_exclusionary_non_obi_data()

    def build(self, city):
        if city in self._non_obi_cities:
            return self.build_non_obi(city)
        return self.build_obi(city)

    def build_non_obi(self, city):
        assert city in self._non_obi_df.index
        city_data = self._non_obi_df.loc[city]
        home_price = self._price_df.query('`City` == @city')['2022-04-30'].item()
        pop = city_data['Total'].item()
        pct_white = round(city_data['White'].item() / pop, 3)
        pct_black = round(city_data['Black'].item() / pop, 3)
        pct_latino = round(city_data['Latino'].item() / pop, 3)
        pct_asian = round(city_data['Asian'].item() / pop, 3)
        pct_li = utils.get_pct_li(city)

        vli_rhna, li_rhna, m_rhna, am_rhna, tot_rhna = utils.get_city_rhna_targets(city)
        return City(home_price=home_price, pct_white=pct_white, pct_black=pct_black,
                    pct_latino=pct_latino, pct_asian=pct_asian, name=city, pct_li=pct_li, pop=pop,
                    vli_rhna=vli_rhna, li_rhna=li_rhna, m_rhna=m_rhna, am_rhna=am_rhna, tot_rhna=tot_rhna, obi=False)

    def build_obi(self, city):
        assert city in self._obi_df['Cities/Towns'].values
        city_obi_data = self._obi_df.query('`Cities/Towns` == @city')
        home_price = self._price_df.query('`City` == @city')['2022-04-30'].item()
        pct_white = round(city_obi_data['White'].item(), 3)
        pct_black = round(city_obi_data['Black'].item(), 3)
        pct_latino = round(city_obi_data['Latino'].item(), 3)
        pct_asian = round(city_obi_data['Asian'].item(), 3)
        pct_li = utils.get_pct_li(city)
        pop = city_obi_data['Population'].item()
        vli_rhna, li_rhna, m_rhna, am_rhna, tot_rhna = utils.get_city_rhna_targets(city)
        return City(home_price=home_price, pct_white=pct_white, pct_black=pct_black,
                    pct_latino=pct_latino, pct_asian=pct_asian, name=city, pct_li=pct_li, pop=pop,
                    vli_rhna=vli_rhna, li_rhna=li_rhna, m_rhna=m_rhna, am_rhna=am_rhna, tot_rhna=tot_rhna, obi=True)


class City:
    def __init__(self, home_price, pct_white, pct_black, pct_latino, pct_asian, name, pct_li, pop,
                 vli_rhna, li_rhna, m_rhna, am_rhna, tot_rhna, obi):
        self._home_price = home_price
        self._median_salary = 0
        self.pct_white = pct_white
        self.pct_black = pct_black
        self.pct_latino = pct_latino
        self.pct_asian = pct_asian
        self.name = name
        self.pct_li = pct_li
        self.pop = pop
        self.vli_rhna = vli_rhna
        self.li_rhna = li_rhna
        self.m_rhna = m_rhna
        self.am_rhna = am_rhna
        self.tot_rhna = tot_rhna
        self.black_delta, self.white_delta, self.brown_delta = utils.get_racial_change(name)
        self.obi = obi

    def __repr__(self):
        return self.name

    def min_wage_jobs(self):
        """How many minimum wage jobs does it take to afford an average home in this city?"""
        hourly_wage = 15
        n_hours = 40
        n_weeks = 52
        yearly_pay = hourly_wage * n_hours * n_weeks
        monthly_pay = yearly_pay / 12
        affordable_rent = 3 / 10 * monthly_pay
        return math.ceil(self.monthly_cost_to_own() / affordable_rent)

    @property
    def home_price(self):
        return self._home_price

    def is_very_white(self):
        # This threshold is arbitrary, duh
        return self.pct_white > .85

    def how_much_whiter(self):
        """By what percent is this city whiter than the rest of the Bay Area?

        Notes
        -----
        Bay Area is 39% white as of 2019. That's the baseline to compare a city to.
        https://bayareaequityatlas.org/indicators/race-ethnicity#/
        """
        bay_area_white_pct = .39
        delta = round(self.pct_white / bay_area_white_pct, 3) - 1
        return max(delta, 0)

    def how_much_less_black(self):
        """By what percent is this city less Black than the rest of the Bay Area?

        Notes
        -----
        Bay Area is 6% black as of 2019. That's the baseline to compare a city to.
        https://bayareaequityatlas.org/indicators/race-ethnicity#/
        """
        bay_area_black_pct = .06
        delta = 1 - round(self.pct_black / bay_area_black_pct, 3)
        return max(delta, 0)

    def black_population_attrition(self):
        """How many fewer Black residents are there since 2010?"""
        return max(self.black_delta, 0)

    def brown_population_attrition(self):
        """How many fewer brown residents are there since 2010?"""
        return max(self.brown_delta, 0)

    def white_population_gain(self):
        """How many more white residents are there since 2010?"""
        return max(-self.white_delta, 0)

    def how_much_less_brown(self):
        """By what percent is this city less brown than the rest of the Bay Area?

        Notes
        -----
        Bay Area is 24% black as of 2019. That's the baseline to compare a city to.
        https://bayareaequityatlas.org/indicators/race-ethnicity#/
        """
        bay_area_latino_pct = .06
        delta = 1 - round(self.pct_latino / bay_area_latino_pct, 3)
        return max(delta, 0)

    def salary_to_buy(self):
        return self.monthly_cost_to_own() * 10 / 3 * 12

    def one_percenter_city(self):
        """Do you need to be in the 1% to afford an average home in this city?

        :return: bool
        Notes
        -----
        www.cnbc.com/2022/01/24/how-much-money-you-have-to-earn-to-be-in-the-top-1percent-in-every-us-state.html#:~:text=According%20to%20a%20recent%20study,in%20the%20top%201%25%20nationally.
        """
        one_percent = 597815
        return self.salary_to_buy() > one_percent

    def income_percent(self):
        """
        Income data is 2019 data from here https://www.irs.gov/statistics/soi-tax-stats-individual-statistical-tables-by-tax-rate-and-income-percentile#earlyRelease
        See excel sheet under "Number of Returns, Shares of AGI and Total Income Tax, AGI Floor on
        Percentiles in Current and Constant Dollars, and Average Tax Rates"
        :return:
        """
        income_data = {'0.001%': 60658598,
                       '0.01%': 12623539,
                       '0.1%': 2458432,
                       '1%': 546434,
                       '2%': 364693,
                       '3%': 291384,
                       '4%': 249320,
                       '5%': 221572,
                       '10%': 154589,
                       '20%': 103012}
        for pct, income in income_data.items():
            if income <= self.salary_to_buy():
                return pct

    def exceeds_private_island(self):
        """Does buying a home in the city cost more than buy a private island?

        Notes
        -----
        The median private island in the Carribbean costs $4.2m according to this 2022 article.
        https://www.jamesedition.com/stories/real-estate/how-much-does-a-private-island-cost/
        """
        private_island = 4200000
        return self.home_price > private_island

    def exceeds_castle(self):
        """Does buying a home in the city cost more than buying an affordable castle in France?

        Notes
        -----
        Castle prices vary dramatically. This 2021 Forbes article lists several that cost around $2m
        www.forbes.com/sites/forbes-global-properties/2021/10/28/buying-a-french-chateau-can-cost-less-than-a-los-angeles-teardown/
        """
        castle = 2000000
        return self.home_price > castle

    def cost_relative_to_country(self):
        """How much more does a home here cost than a median home in America?

        Notes
        -----
        Data source: Q1 2022 https://fred.stlouisfed.org/series/MSPUS"""
        country_avg = 428700
        return round(self.home_price / country_avg)

    def monthly_cost_to_own(self):
        """How much per month does it cost to buy an average home here?

        Notes
        -----
        Property tax source: "The average tax rate in California is around 1.2% of assessed value,
        including voter-approved local taxes," per the SF Chronicle's July 10, 2020 article.

        Homeowners' insurance source: "the state average of $1,565 per year in California" per PolicyGenius's
        May 1, 2022 article.

        Mortgage interest rate: average rate today for a 30-year fixed rate mortgage is 4.96% per Business Insider as
        of May 2, 2022.

        Maintenance costs: average yearly maintenance cost is 16,957.

        This method is only a conservative approximation of monthly costs. It does not account for HOA fees
        or mortgage insurance. It also only returns the cost for the first month of ownership, so the
        interest is simple.
        """
        # Yearly costs
        property_tax = 0.012
        homeowners_insurance = 1565
        mortgage_interest = 0.0496
        maintenance_cost = 16957
        principal = self.home_price * .80

        # Monthly cost
        m_property_tax = self.home_price * property_tax / 12
        m_insurance = homeowners_insurance / 12
        m_maintenance = maintenance_cost / 12
        m_mortgage = (1 + mortgage_interest) * principal / 30 / 12
        return m_property_tax + m_insurance + m_maintenance + m_mortgage

    def affh_needed_li_homes(self):
        """How many LI homes would this city need to add to achieve parity with the region?
        
        Notes
        -----
        http://www.bayareacensus.ca.gov/california.htm
        https://bayareaequityatlas.org/node/60841#:~:text=About%2016%20percent%20of%20Bay,in%20this%20low%2Dincome%20category.
        """
        li_pct_bay_area = .488
        n_ppl_per_home = 2.9
        return math.ceil(self.pop * (li_pct_bay_area - self.pct_li) / n_ppl_per_home)

    def pct_sfz(self):
        return utils.get_city_sfz_pct(self.name)


    def pct_ho_sfz(self):
        return utils.get_city_sfz_ho_pct(self.name)
