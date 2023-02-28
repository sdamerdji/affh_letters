# affh_letters
This is an automated letter campaign for Bay Area cities with high degrees of segregation. As cities update their housing plans, they have an obligation to demonstrate to California Department of Housing & Community Development (HCD) that they are complying with Affirmatively Furthering Fair Housing (AFFH) law. This repository contains code that sends an email to each exclusionary city, with the state regulator HCD cc'd, regarding the city's housing element and argues that city's existing exclusionary zoning policies violate AFFH law. This letter campaign recieved local press in the Los Altos Town Crier:  https://www.losaltosonline.com/news/la-lah-deemed-exclusionary-as-they-prep-housing-plans

# Data sources

Berkeley's OBI data is available at the bottom of this page: https://belonging.berkeley.edu/racial-segregation-san-francisco-bay-area-part-1

Home price data comes from Zillow: https://www.zillow.com/research/data/
I use Zillow Home Value Index for all homes (seasonally adjusted)

Berkeley's OBI dataset excludes a few cities (e.g. Belvedere and Woodside), so for those cities I use 2019 ACS data (race.csv, income.csv)
