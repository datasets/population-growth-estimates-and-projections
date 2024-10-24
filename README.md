<a href="https://datahub.io/core/population-growth-estimates-and-projections"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25)" alt="badge" /></a>

Total Population - Both Sexes. De facto population in a country, area or region as of 1 July of the year indicated. Figures are presented in thousands.

## Data

Data comes from [United Nations' Population Division datasets](https://esa.un.org/unpd/wpp/Download/Standard/Population/). Total population (both sexes combined) by region, subregion and country, annually for 1950-2100 (thousands). Data is cleaned, normalized, "un-pivoted", and represented in nice machine readable way in CSV format. Dataset represented here has several resources:
* Estimates from 1950 - 2015. Original
* Medium fertility variant, 2015 - 2100
* High fertility variant, 2015 - 2100
* Low fertility variant, 2015 - 2100
* Constant fertility variant, 2015 - 2100
* Instant replacement fertility variant, 2015 - 2100
* Momentum fertility variant, 2015 - 2100
* Zero Migration variant, 2015 - 2100
* Constant Mortality variant, 2015 - 2100

## Preparation

You will need Python 3.6 or greater and dataflows library to run the script

To update the data run the process script locally:

```
# Install dataflows
pip install dataflows

# Run the script
python population_estimates.py
Several steps will be done to get the final data.
```

## Licence

United Nations, Department of Economic and Social Affairs, Population Division (2017). World Population Prospects: The 2017 Revision, DVD Edition.
