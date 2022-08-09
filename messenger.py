from pathlib import Path
from textwrap import dedent

import pandas as pd

import gmail

pdfs = list(Path('./letters').glob('*.pdf'))
emails_df = pd.read_csv('./letter_data/emails.csv', names=['city', 'emails'])
for pdf_file in pdfs:
    city_name = pdf_file.stem
    emails = emails_df[
        emails_df['city'] == city_name
        ].squeeze()['emails'].split(',')
    body = dedent(
        f"""\
            Dear {city_name} City Council:

            Please see the attached letter from South Bay YIMBY 
            regarding {city_name}'s duty to AFFH in its 6th cycle Housing Element.

            Best,<br>
            Salim Damerdji<br>
            """
    )

    message = gmail.make_email(
        to=[(email, email) for email in emails],
        cc=[
            ('HousingElements@hcd.ca.gov', 'HousingElements@hcd.ca.gov'),
            ('Keith Diggs', 'keith@yimbylaw.org'),
        ],
        subject=f"Letter on {city_name}'s duty to AFFH in RHNA6.",
        body=body,
        attachments=[(f"{city_name}.pdf", pdf_file)],
    )
    gmail.send_email(message)
