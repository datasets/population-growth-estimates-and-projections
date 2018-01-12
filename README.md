Total Population - Both Sexes. De facto population in a country, area or region as of 1 July of the year indicated. Figures are presented in thousands.

## Data

Data comes from [United Nations' Population Division datasets](https://esa.un.org/unpd/wpp/Download/Standard/Population/). Total population (both sexes combined) by region, subregion and country, annually for 1950-2100 (thousands). Data is cleaned, normalized, "un-pivoted", and represented in nice machine readable way in CSV format. Dataset represented here has Estimates from 1950 - 2015. Original dataset also includes:
* Medium fertility variant, 2015 - 2100
* High fertility variant, 2015 - 2100
* Low fertility variant, 2015 - 2100
* Constant fertility variant, 2015 - 2100
* Instant replacement fertility variant, 2015 - 2100
* Momentum fertility variant, 2015 - 2100
* Zero Migration variant, 2015 - 2100
* Constant Mortality variant, 2015 - 2100

## Processing

1. You will need python 3.6 and [datapackage-pipelines](https://github.com/frictionlessdata/datapackage-pipelines) to process the data.
2. Create `pipeline-spec.yaml` and copy this into.
```yaml
population-growth:
  pipeline:
    -
      run: add_resource
      parameters:
        name: population
        url: https://esa.un.org/unpd/wpp/DVD/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx
        format: xlsx
        skip_rows: 17
        headers: [index, variant, region, notes, country-code, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
        sheet: 1
    -
      run: stream_remote_resources
    -
      run: delete_fields
      parameters:
        resources: population
        fields:
          - index
          - variant
          - notes
          - country-code
    -
      run: unpivot
      parameters:
        resources: population
        extraKeyFields:
          -
            name: year
            type: year
        extraValueField:
          name: population
          type: number
        unpivot:
          -
            name: ([0-9]{4})
            keys:
              year: \1
    -
      run: dump.to_path
      parameters:
        out-path: population-growth

```
3. run `dpp run population-growth`

## Licence

United Nations, Department of Economic and Social Affairs, Population Division (2017). World Population Prospects: The 2017 Revision, DVD Edition.
