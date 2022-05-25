import pandas as pd
from pathlib import Path
import gmail
from textwrap import dedent


pdfs = list(Path('./letters').glob('*.pdf'))
emails_df = pd.read_csv('ABAG council emails.csv', names=['city', 'emails'])
for pdf_file in pdfs:
    city_name = pdf_file.stem
    # if city_name not in sent_emails and city_name != "Pleasant Hill":
    # if city_name not in ["Pleasant Hill", "Mountain View", "Oakland"]:
    if city_name == "Milpitas":
        emails = emails_df[
            emails_df['city'] == city_name
            ].squeeze()['emails'].split(',')

        body = dedent(
            f"""\
            Dear {city_name} City Council:

            Please see the attached letter from YIMBY Law and Greenbelt Alliance
            regarding {city_name}'s 6th cycle Housing Element.

            The PDF should be correctly attached now.

            Best,<br>
            Sid Kapur<br>
            sidharthkapur1@gmail.com<br>
            (469) 487-9648
            """
        )

        message = gmail.make_email(
            to=[(email, email) for email in emails],
            cc=[
                ('HousingElements@hcd.ca.gov', 'HousingElements@hcd.ca.gov'),
                ('Keith Diggs', 'keith@yimbylaw.org'),
            ],
            # to=[('sidharthkapur1@gmail.com', 'sidharthkapur1@gmail.com')],
            # cc=[],
            subject=f"Letter re. {city_name}'s 6th Cycle Housing Element",
            body=body,
            attachments=[(f"{city_name}.pdf", pdf_file)],
        )
        gmail.send_email(message)