"""
This class contains a constant dict that stores custom analysis for each city.
We're using this class to contain all the local knowledge that housing advocates have for each city.
"""
CUSTOM = {
    'Cupertino':
        ('The city has failed to affirmatively further fair housing in its housing element outreach:\n'
         "1. When several De Anza College students emailed council to request inclusion in the city's "
         'housing element outreach, they were reprimanded by Vice Mayor Liang Chao in an email to the entire '
         "Foothill-De Anza board of trustees. This, as intended, reified existing disparities in which economic "
         "segments of the community are welcome in city hall.\n"
         "2. This year, Cupertino City Council proposed requiring all 501(c) organizations to register as lobbyists "
         'if they perform a requisite amount of lobbying per year and proposed to establish a personal '
         'right to sue anyone who doesn’t register as a lobbyist. Given the prevalence with which housing advocates '
         'are accused of being lobbyists, this move is intended to chill speech and public participation, which '
         'is antithetical to the inclusive public participation AB 686 requires.\n'
         'Indeed, instead of engaging all economic segments of the community, the city has continued to rely on '
         "poorly reasoned analysis from the Planning Commission, including Planning Commissioner R Wang's suggestion "
         "the city place new housing below ground or above highways and Planning Commission Chair Steven Scharf's "
         'argument that the city could AFFH by maintaining high parking minimums. (This is the same Steven '
         'Scharf who once joked about building a wall around Cupertino to keep San Jose residents out.) When middle '
         'and working class families are excluded from the conversation, this is what passes for analysis.\n'
         )
}


def get_customized_cities():
    return CUSTOM.keys()


def get_city_custom_analysis(city):
    return CUSTOM.get(city, '')
