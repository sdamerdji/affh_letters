import math


class CityFactory:
    def __init__(self, obi_df, price_df):
        self._obi_data = obi_df
        self._price_df = price_df

    def build(self, city):
        assert city in self._obi_data['Cities/Towns'].values
        city_obi_data = self._obi_data.query('`Cities/Towns` == @city')
        home_price = 0
        pct_white = round(city_obi_data['White'].item(), 3)
        pct_black = round(city_obi_data['Black'].item(), 3)
        pct_latino = round(city_obi_data['Latino'].item(), 3)
        pct_asian = round(city_obi_data['Asian'].item(), 3)
        return City(home_price=home_price, pct_white=pct_white, pct_black=pct_black,
                    pct_latino=pct_latino, pct_asian=pct_asian)


class City:
    def __init__(self, home_price, pct_white, pct_black, pct_latino, pct_asian):
        self._home_price = home_price
        self._median_salary = 0
        self.pct_white = pct_white
        self.pct_black = pct_black
        self.pct_latino = pct_latino
        self.pct_asian = pct_asian

    def min_wage_jobs(self):
        """How many minimum wage jobs does it take to afford an average home in this city?"""
        hourly_wage = 15
        n_hours = 40
        n_weeks = 52
        yearly_pay = hourly_wage * n_hours * n_weeks
        monthly_pay = yearly_pay / 12
        return math.ceil(self.monthly_cost_to_own() / monthly_pay)

    @property
    def home_price(self):
        return self._home_price

    def is_very_white(self):
        # This threshold is arbitrary, duh
        return self.pct_white > .85

    def how_much_whiter(self):
        """By what percent is this city whiter than the rest of the Bay Area?"""
        bay_area_white_pct = .42  # FIXME
        return round(self.pct_white - bay_area_white_pct, 1)

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
        return round(self.home_price / country_avg, 1)

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

        Maintenance costs: average yearly maintenance cost is 16,957. average home price is 600k in California as of
        2020, so the maintenance cost is around 2.8% of the home price.

        This method is only a conservative approximation of monthly costs. It does not account for HOA fees
        or mortgage insurance. It also only returns the cost for the first month of ownership, so the
        interest is simple.
        """
        # Yearly costs
        property_tax = 0.012
        homeowners_insurance = 1565
        mortgage_interest = 0.0496
        maintenance_costs = 0.028
        principal = self.home_price * .80

        # Monthly cost
        m_property_tax = self.home_price * property_tax
        m_insurance = homeowners_insurance / 12
        m_maintenance = maintenance_costs / 12
        m_mortgage = mortgage_interest * principal / 30 / 12
        return m_property_tax + m_insurance + m_maintenance + m_mortgage
