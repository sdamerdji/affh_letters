from datetime import date

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import re
import utils
from city import CityFactory

"""
This code is largely sourced from Sid Kapur's repository here: https://github.com/YIMBYdata/rhna-apr-emails
Thanks Sid!
"""

header = """
<div class="text-center">
    <img class="h-20 inline"
    src="file:./letter_data/sb_yimby_logo.png" />
</div>
"""


def make_body(city):
    today = date.today().strftime("%B %d, %Y")
    intro = (f'{today}\n'
             f'Dear {city} City Council:\n'
             f'We are writing on behalf of <b class="text-bold">South Bay YIMBY</b> regarding {city}’s 6th Cycle Housing '
             f'Element Update. As a regional pro-housing advocacy group, South Bay YIMBY works to ensure '
             f'cities adopt housing elements that are fair, realistic, and lawful.\n'
             f"Per GOV §8899.50(a)(1), {city}'s housing element must affirmatively further fair housing "
             f"by 'taking meaningful actions... that overcome patterns of segregation.'\n")

    backgr = (f'As our past letter showed, your city is segregated from the rest of the Bay, as only the '
              f'richest {city.income_percent()} '
              f'of households can afford an average home in your city. ')

    backgr += (f'To grow into an integrated city, law requires you to provide low income (LI) folks with a range of '
               f'housing options that meet their needs. Yet, your Draft falsely claims {city.li_adus()}% '
               f'of LI folks would have their needs met by ADUs built in {city.name}.\n')

    problem = (f'<b class="text-bold">Few, if any, of your ADUs further fair housing goals.</b> A 2020 survey from '
                f'Berkeley’s Center for Community Innovation found 40% of ADUs are held off '
                f'the long-term rental market, often as home offices, while 32% of ADUs are rented '
                f'to families or friends for discounted rents. Sweetheart deals to family and friends do not promote '
                f'integration, as required by law. When your city is '
                f'{round(city.how_much_whiter() * 100)}% whiter than the Bay Area, providing LI units '
                f'disproportionately to family members reifies existing patterns of racial segregation.\n')
    
    problem += (f'<b class="text-bold">Less than a third of ADUs are actually rented on the open market.</b> '
                f"But ABAG’s general findings on ADU affordability don't extend "
                f"to your city, where LI folks can't afford open market rate rents. "
                f'<b class="text-bold">The cheapest {city.name} ADU on {city.adus_rental_source()} rents '
                f'for ${city.adus_monthly_rental():,}.</b>\n')

    if city.name == 'Hillsborough':
        problem += (f'{city.name} will likely reply to these objections by pointing to a local ADU survey, but <b class="text-bold">that '
                    f"local survey had only five respondents</b> indicate the rent they charge. Portraying this as a "
                    f"valid survey on affordability is malpractice. What's more, the survey does not show a "
                    f"single ADU is rented affordably to a tenant who is not simply a family member.\n")
    recs = ("To be clear, ADUs are a valuable part of a healthy mix of housing choices. But not every low income "
            "family wants to live in "
            "someone else’s backyard. Not every LI family is small enough to live in a small ADU. And even "
            f"those LI families who would happily live in an ADU can’t do it in {city.name} "
            "because virtually no ADUs are available to the public at a rent suitable for LI tenants.\n")
    recs += ("To rectify this, your city should entirely lift its ban on "
             'apartments, condos, and townhomes. As of 2020, your city outlawed these buildings '
             f'in {city.pct_sfz():.0f}% of residential areas, effectively '
             f'banning affordable housing built at-scale. '
             f'Aside from creating more abundant options for LI families, '
             'lifting your exclusionary zoning will also yield homeownership opportunities to build intergenerational '
             'wealth in a high opportunity community that ADUs, as rentals, cannot. Plus, more choice allows '
             "larger low income families to find 3+ bedroom units, rare among ADUs, that meets their needs.\n")

    if city.name == 'Hillsborough':
        recs += ('We appreciate that you already are making significant steps in this direction, but we note that, '
                 f'even among other small, exclusionary cities in the Bay Area, {city.name} slots nearly twice as '
                 f"many low income families into ADUs as other cities do. That is, even with the steps you've made,"
                 " you are still behind the ball in lifting exclusionary zoning. If your city is politically unwilling "
                 f'to make room for low income residents everywhere in {city.name}, you should at least double the '
                 f'amount of upzoning accommodating low income folks to be in line with other exclusionary '
                 f'Bay Area cities. This is the bare minimum.')

    signoff = ('<br>'
               "Thank you,"
               "<table>"
               '<tr class="mb-1">'
               '    <td><b class="text-bold">Salim Damerdji</b>, South Bay YIMBY</td>'
               #"</tr>"
               #'<tr class="mb-1">'
               #'    <td><b class="text-bold">Keith Diggs</b>, YIMBY Law</td>'
               "</tr>")
    signoff += "</table>"
    return intro + backgr + problem + recs + signoff


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

factory = CityFactory(utils.get_obi_data(), utils.get_zillow_data())
cities = ['Monte Sereno', 'Atherton', 'Hillsborough', "Los Altos Hills", 'Woodside']
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

    html.write_pdf(f'./adu_letters/{city}.pdf', stylesheets=[tailwind_css, font_css], font_config=font_config)
