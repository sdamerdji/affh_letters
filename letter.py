from datetime import date

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
    today = date.today().strftime("%B %d, %Y")
    intro = (f'{today}\n'
             f'Dear {city} City Council:\n'
             f'We are writing on behalf of <b class="text-bold">YIMBY Law</b> regarding {city}’s 6th Cycle Housing '
             f'Element Update. <b class="text-bold">YIMBY Law</b> is a legal nonprofit working to make housing in '
             f'California more accessible and affordable through enforcement of state law.\n'
             f"Per §8899.50(a)(1) of state code, {city}'s housing element must affirmatively further fair housing, "
             f"which entails 'taking meaningful actions... that overcome patterns of segregation.'\n")

    backgr = (f'The City of {city} is uniquely positioned to affirmatively further fair housing, as {city} '
              f'is a wealthy, exclusionary city that Berkeley researchers identify as highly segregated from the '
              f'rest of the Bay Area. This socioeconomic segregation is caused by the exclusionary '
              f'cost of housing in your community, where an average home, as of April 30th, costs '
              f'<a href="https://www.zillow.com/research/data/">${int(round(city.home_price, -3)):,}</a>'
              f', which is only affordable to someone earning a salary '
              f'of ${int(round(city.salary_to_buy(), -3)):,}')
    if city.income_percent():
        backgr += (f', meaning <b class="text-bold">only the richest {city.income_percent()} of households can afford '
                   f'to settle down in your community</b>')
    if city.exceeds_castle():
        backgr += (". To put a finer point on the level of affluence in your community, the average home in your "
                   'city costs more than <a href="www.forbes.com/sites/forbes-global-properties/2021/10/28/buying-a-french-chateau-can-cost-less-than-a-los-angeles-teardown/">French castles</a>')
        if city.exceeds_private_island():
            backgr += " and <a href='https://www.jamesedition.com/stories/real-estate/how-much-does-a-private-island-cost/'>private islands in the Caribbeans</a>"
    backgr += f'. It is thus no coincidence that your city is '
    if city.how_much_whiter() > .05:
        backgr += f'{round(city.how_much_whiter() * 100)}% whiter than the rest of the Bay'
        if city.how_much_less_black() > .05 or city.how_much_less_brown() > .05:
            backgr += ', as well as '
    if city.how_much_less_black() > .05:
        backgr += f'{round(city.how_much_less_black() * 100)}% less black'
    if city.how_much_less_brown() > .05:
        if city.how_much_less_black() > .05:
            backgr += ' and '
        backgr += f'{round(city.how_much_less_brown() * 100)}% less brown'
    if city.how_much_less_brown() > .05 or city.how_much_less_black() > .05:
        backgr += ' than the rest of the Bay Area'
    backgr += '.'
    if city.black_population_attrition() or city.brown_population_attrition() or city.white_population_gain():
        backgr += " Sadly, your city's demographics have trended in an even less equitable direction, "
        if city.black_population_attrition():
            backgr += f'losing {city.black_population_attrition()} black residents'
            if city.brown_population_attrition():
                backgr += ' and '
        if city.brown_population_attrition():
            backgr += f'losing {city.brown_population_attrition()} brown residents'
        if (city.black_population_attrition() or city.brown_population_attrition()) and city.white_population_gain():
            backgr += f' while gaining {city.white_population_gain()} white residents'
        backgr += ' since 2010.'
    backgr += '\n'

    wh = ("In a 2021 report entitled 'Exclusionary Zoning: Its Effect on Racial Discrimination in the Housing Market,' "
          "economic advisors for the White House outline how exclusionary zoning, like yours, causes segregation. "
          "Your exclusionary zoning pushes low income children to live in less resourced areas, which begets "
          "worse life outcomes from health to income. The research is clear: exclusionary zoning violates your duty "
          "to further fair housing.\n")
    recs = ("To take meaningful actions that overcome patterns of segregation, we recommend you:\n"
            '1. <b class="text-bold">End apartment bans in high opportunity areas.</b> This will give middle and '
            "working class families the opportunity to share in the resources your rich neighborhoods enjoy. "
            'As of 2020, <b class="text-bold">your city banned apartments in over ')
    if city.pct_ho_sfz() > city.pct_sfz() + 1:
        recs += (f'{city.pct_sfz()}% of residential areas</b>'
                 f', including in {city.pct_ho_sfz()}% of high opportunity residential areas')
    elif city.pct_ho_sfz():
        recs += f'{city.pct_ho_sfz()}% of high opportunity residential areas</b>'
    else:
        # Morgan Hill has no high opportunity areas, so this condition is for Morgan Hill
        recs += f'{city.pct_sfz()}% of residential areas</b>'
    recs += '.\n'
    recs += (f'2. <b class="text-bold">Accommodate {city.affh_needed_li_homes()} low income homes in your site '
             f'inventory.</b> While substantially larger than the floor of {city.li_rhna + city.vli_rhna} low income '
             f'homes required by RHNA, {city.affh_needed_li_homes()} is the number of homes required to bring the '
             f'proportion of low income families '
             f'in your city in line with the rest of the Bay Area. While this number is large enough to be '
             f'politically challenging, it will always be politically challenging to overcome segregation, as AFFH '
             f'requires.\n')
    signoff = ('<br>'
               "Thank you,"
               "<table>"
               '<tr class="mb-1">'
               '    <td><b class="text-bold">Salim Damerdji</b>, South Bay YIMBY</td>'
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

cities = utils.get_exclusionary_cities()
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
