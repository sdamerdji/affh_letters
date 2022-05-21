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
             f"We are writing to remind you of {city}'s legal duty to affirmatively further fair housing, which "
             f"entails 'taking meaningful actions... that overcome patterns of segregation' §8899.50(a)(1).\n")

    backgr = (f'The City of {city} is uniquely positioned to affirmatively further fair housing, as {city} '
              f'is an exclusionary city that is wealthier ')

    if city.how_much_whiter() > 0:
        backgr += 'and whiter '

    backgr += (f'than the rest of the Bay Area. Berkeley researchers have found that your city exhibits high levels '
               f'of segregation. This socioeconomic segregation is caused by the exclusionary '
               f'cost of housing in your community, where the average home is ${round(city.home_price):,}, per '
               f"Zillow's data as of April 2022. This home price is only affordable to someone earning a salary "
               f'of ${round(city.salary_to_buy()):,}')
    if city.one_percenter_city():
        backgr += ", meaning only the top 1% can afford to settle down in your community"
    if city.exceeds_castle():
        backgr += ". In fact, the average home in your community costs more than many castles in the France"
        if city.exceeds_private_island():
            backgr += " as well as private islands in the Caribbeans"
    backgr += '.\n'
    signoff = ('<br>'
               "Thank you,"
               "<table>"
               '<tr class="mb-1">'
               '    <td><b class="text-bold">Salim Damerdji</b>, South Bay YIMBY</td>'
               '    <td class="px-1">(sdamerdji1@gmail.com)</td>'
               "</tr>"
               "</table>")
    return intro + backgr + signoff


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

cities = utils.get_exclusionary_cities()[:3]
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

    html.write_pdf(f'./output/{city}.pdf', stylesheets=[tailwind_css, font_css], font_config=font_config)


