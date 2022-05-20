from pathlib import Path

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
    body = f"""
    May 21, 2022
    
    Dear {city} City Council:
    
    We are writing on behalf of <b class="text-bold">YIMBY Law</b> regarding {city}’s 6th Cycle Housing 
    Element Update. 
    <b class="text-bold">YIMBY Law</b> is a legal nonprofit working to make housing 
    in California more accessible and affordable through enforcement of state law.
    
    We are writing to remind you of {city}'s legal duty to affirmatively further fair housing, which requires 'taking
    meaningful actions... that overcome patterns of segregation" §8899.50(a)(1). The City of {city} is wealthier than
    the average Bay Area city and has been identified by researchers as being segregated from other cities. 
    
    An average home in {city} costs {city.home_price}, which is only affordable to someone earning a salary of 
    {city.salary_to_buy()}.
    """
    if city.one_percenter_city():
        body += " This means your city is only affordable to Americans in the top 1%."
    if city.exceeds_private_island():
        body += (" Indeed, the average home in your city costs more than the cost "
                 "of buying a private island in the Carribbeans.")
    if city.exceeds_castle():
        body += " In fact, there are many castles in the France that cost less than an average home in your city."

    body += """
        <br>
        
        Thank you,
        
        <table>
        <tr class="mb-1">
            <td><b class="text-bold">Salim Damerdji</b>, South Bay YIMBY</td>
            <td class="px-1">(sdamerdji1@gmail.com)</td>
        </tr>
        </table>
        """
    return body


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

for city_name in cities:
    city = CityFactory(city_name)
    body = make_body(city)
    cell_classes = 'class="border p-1"'
    body_html = ''.join(
        [
            f'<p class="mb-3 text-justify">{para}</p>'
            for para in body.split('\n\n')
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

    # dump a preview so I can share it on Google Docs for edits
    Path(f'./html/{city}.html').write_text(
        """
        <link rel="stylesheet" href="https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css">
        <style>
        {font_css.string}
        </style>
        """
        + html_str
    )
