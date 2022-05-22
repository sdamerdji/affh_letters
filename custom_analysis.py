"""
This class contains a constant dict that stores custom analysis for each city.
We're using this class to contain all the local knowledge that housing advocates have for each city.
"""
CUSTOM = {
    'Cupertino':
        ('The city has furthermore failed to affirmatively further fair housing in its outreach:\n'
         "1. When a number of De Anza College students emailed council to request inclusion in the city's"
         'housing element outreach, they were reprimanded by Vice Mayor Liang Chao in an email to the entire '
         'Foothill-De Anza board of trustees. De Anza College students are precisely one of the demographic '
         'groups who should be the subject of AFFH focus — people who have clear housing needs in Cupertino '
         "but cannot afford housing in the city. The Vice Mayor's admonishment creates a chilling effect "
         "around housing element advocacy and reifies existing disparities in which economic segments of "
         "the community are welcome in city hall.\n"
         "2. This year, Cupertino City Council proposed requiring all 501(c) organizations to register as lobbyists "
         'if they perform a requisite amount of lobbying per year and proposed to establish a personal '
         'right to sue anyone who doesn’t register as lobbyist. Given the prevalence with which pro-housing renters '
         'are accused of being lobbyists, this move is intended to chill speech and public participation, which '
         'is antithetical to the inclusive public participation AB 686 requires.\n'
         'Indeed, instead of engaging all economic segments of the community, the city has continued to rely on '
         "poorly reasoned analysis from the Planning Commission, including Planning Commissioner Wang's suggestion "
         'the city place new housing below ground or above highways. Planning Commission Chair Steven Scharf '
         'argued high parking mandates fulfill AFFH standards. When low income renters are excluded from the '
         'conversation, this is what passes for analysis.'
         )
}


def get_customized_cities():
    return CUSTOM.keys()


def get_city_custom_analysis(city):
    return CUSTOM.get(city, '')
