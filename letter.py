from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

import utils
from city import CityFactory

"""
This code is largely sourced from Sid Kapur's repository here: https://github.com/YIMBYdata/rhna-apr-emails
Thanks Sid!
"""

header = """
<div class="text-center">
    <img class="h-20 inline"
    src="file:./letter_data/yimby_law_logo.png" />
</div>
"""


def make_body(city):
    intro = (f'May 21, 2022\n'
             f'Dear {city} City Council:\n'
             f'We are writing on behalf of <b class="text-bold">YIMBY Law</b> regarding {city}’s 6th Cycle Housing '
             f'Element Update. '
             f'<b class="text-bold">YIMBY Law</b> is a legal nonprofit working to make housing in California more '
             f'accessible and affordable through enforcement of state law.\n'
             f"We are writing to remind you of {city}'s legal duty in its housing element to affirmatively further "
             f"fair housing, which entails 'taking meaningful actions... that overcome patterns of segregation' "
             f"§8899.50(a)(1).\n")

    backgr = (f'The City of {city} is uniquely positioned to affirmatively further fair housing, as {city} '
              f'is a wealthy, exclusionary city that Berkeley researchers have found is highly segregated from the '
              f'rest of the Bay Area. This socioeconomic segregation is caused by the exclusionary '
              f'cost of housing in your community, where an average home, as of April 30th, costs '
              f'${round(city.home_price):,}, which is only affordable to someone earning a salary '
              f'of ${round(city.salary_to_buy()):,}')
    if city.one_percenter_city():
        backgr += ', meaning <b class="text-bold">only the top 1% can afford to settle down in your community</b>'
    if city.exceeds_castle():
        backgr += (". To put a finer point on the level of affluence in your community, the average home in your " 
                   "city costs more than French castles")
        if city.exceeds_private_island():
            backgr += " and private islands in the Caribbeans"
    backgr += f'. It is thus no coincidence at all that your city is '
    if city.how_much_whiter():
        backgr += f'{round(city.how_much_whiter() * 100)}% whiter than the rest of the Bay'
        if city.how_much_less_black() or city.how_much_less_brown():
            backgr += ', as well as '
    if city.how_much_less_black():
        backgr += f'{round(city.how_much_less_black() * 100)}% less black'
    if city.how_much_less_brown():
        if city.how_much_less_black():
            backgr += ' and '
        backgr += f'{round(city.how_much_less_brown() * 100)}% less brown than the rest of the Bay'
    backgr += '.\n'

    wh = ("In a 2021 report entitled 'Exclusionary Zoning: Its Effect on Racial Discrimination in the Housing Market,' "
          "the White House's leading economic advisors outlined the troves of academic research that shows how "
          "exclusionary zoning, such as your city's, contributes to racial segregation. The White House's report "
          "cites cutting-edge research that shows housing 'likely explains more than 30% of the Black-white racial "
          "wealth gap.' By banning apartments and zoning working class families out of your city, your city, "
          "award-winning Harvard research shows, is causing low income children to have worse life outcomes, from "
          "health to income. Exclusionary zoning is not consistent with your city's values and it is not consistent "
          "with your legal obligation to affirmatively further fair housing.\n")
    recs = (f"To take meaningful actions that overcome patterns of segregation, we recommend you:\n"
            f'1. <b class="text-bold">End apartment bans in high opportunity areas.</b> This will give working class '
            f"and middle class families the opportunity to share in the resources your city's high opportunity areas "
            f"enjoys. Furthermore, ending apartment bans is no longer subject to lengthy CEQA analysis thanks to SB 10,"
            f" so your city's apartment ban in R1 areas can be lifted tomorrow.\n"
            f'2. <b class="text-bold">Accommodate {city.affh_needed_li_homes()} low income homes in your site '
            f'inventory.</b> This is the number of homes required to bring the proportion of low income families '
            f'in your city in line with the rest of the Bay Area. While this number is large enough to be '
            f'politically challenging, it will always be politically challenging to overcome segregation, as AFFH '
            f'requires.\n')
    signoff = ('<br>'
               "Thank you,"
               "<table>"
               '<tr class="mb-1">'
               '    <td><b class="text-bold">Salim Damerdji</b>, South Bay YIMBY</td>'
               '    <td class="px-1">(sdamerdji1@gmail.com)</td>'
               "</tr>"
               "</table>")
    return intro + backgr + wh + recs + signoff


font_css = CSS(string="""
h3 {
    font-family: "Founders Grotesk";
}
h1, h2, p {
    font-family: ETbb;
}

p {
    hyphens: auto;
    font-size: 14px;
}

@page {
    margin-left: 2cm;
    margin-right: 2cm;
    margin-top: 1cm;
    margin-bottom: 1cm;
}
"""
               )
font_config = FontConfiguration()

tailwind_css = CSS(url='https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css')

cities = utils.get_exclusionary_cities()[:10]
factory = CityFactory(utils.get_obi_data(), utils.get_zillow_data())

for city_name in cities:
    city = factory.build(city_name)
    body = make_body(city)
    cell_classes = 'class="border p-1"'
    body_html = ''.join(
        [
            f'<p class="mb-3 text-justify">{para.strip()}</p>'
            for para in body.split('\n') if para.strip()
        ]
    )
    html_str = f"""
        {header}
        <html lang="en">
        <main class="mt-4">
            {body_html}
        </main>
        </html>
        """

    html = HTML(string=html_str)

    html.write_pdf(f'./letters/{city}.pdf', stylesheets=[tailwind_css, font_css], font_config=font_config)


