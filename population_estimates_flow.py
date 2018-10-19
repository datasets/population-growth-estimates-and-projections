import os

from dataflows import Flow, PackageWrapper, ResourceWrapper, validate
from dataflows import add_metadata, load, set_type
from dataflows import add_computed_field, delete_fields, unpivot

resource_names = [
    'population-estimates',
    'population-low-fertility',
    'population-medium-fertility',
    'population-high-fertility',
    'population-constant-fertility',
    'population-instant-replacement',
    'population-momentum',
    'population-zero-migration',
    'population-constant-mortality',
    'population-no-change'
]

source_url = 'https://esa.un.org/unpd/wpp/DVD/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx'


def readme(fpath='README.md'):
    if os.path.exists(fpath):
        return open(fpath).read()


def rename_resources(package: PackageWrapper):
    for idx, name in enumerate(resource_names):
        package.pkg.descriptor['resources'][idx]['name'] = name
        package.pkg.descriptor['resources'][idx]['path'] = 'data/%s.csv' % name
        package.pkg.descriptor['resources'][idx]['dpp:streaming'] = True

    yield package.pkg
    res_iter = iter(package)
    for res in  res_iter:
        yield res.it
    yield from package


population_estimates = Flow(
    add_metadata(
        name="population-growth-estimates-and-projections",
        title= "Population Growth",
        descriptor="Total Population - Both Sexes. De facto population in a country, area or region",
        views=[
            {
                "name": "population-growth-estimates",
                "resources": [
                    {
                        "name": "population-estimates",
                        "transform": [{"expression": "data['Region'] === 'WORLD'","type": "filter"}]
                    }
                ],
                "spec": {"group": "year","series": ["population"],"type": "line"},
                "specType": "simple",
                "title": "Population Growth - World Estimates"
            },
            {
                "name": "population-growth-projections",
                "resources": [
                    {
                        "name": "population-no-change",
                        "transform": [{"expression": "data['Region'] === 'WORLD'", "type": "filter"}]
                    }
                ],
                "spec": {"group": "year","series": ["population"],"type": "line"},
                "specType": "simple",
                "title": "Population Growth - World Projections (No change)"
            },
            {
                "name": "population-growth-projections-low",
                "resources": [
                    {
                        "name": "population-low-fertility",
                        "transform": [{"expression": "data['Region'] === 'WORLD'","type": "filter"}]
                    }
                ],
                "spec": {"group": "year","series": ["population"],"type": "line"},
                "specType": "simple",
                "title": "Population Growth - World Projections (Low Fertility)"
            },
            {
                "name": "population-growth-projections-medium",
                "resources": [
                    {
                        "name": "population-medium-fertility",
                        "transform": [{"expression": "data['Region'] === 'WORLD'","type": "filter"}]
                    }
                ],
                "spec": {"group": "year","series": ["population"],"type": "line"},
                "specType": "simple",
                "title": "Population Growth - World Projections (Medium Fertility)"
            },
            {
                "name": "population-growth-projections-high",
                "resources": [
                    {
                        "name": "population-high-fertility",
                        "transform": [
                            {"expression": "data['Region'] === 'WORLD'","type": "filter"}]
                    }
                ],
                "spec": {"group": "year","series": ["population"],"type": "line"},
                "specType": "simple",
                "title": "Population Growth - World Projections (High Fertility)"
            }
        ],
        readme=readme()
    ),
    load(source_url,format='xlsx',sheet='ESTIMATES',headers=17),
    load(source_url,format='xlsx',sheet='LOW VARIANT',headers=17),
    load(source_url,format='xlsx',sheet='MEDIUM VARIANT',headers=17),
    load(source_url,format='xlsx',sheet='HIGH VARIANT',headers=17),
    load(source_url,format='xlsx',sheet='CONSTANT-FERTILITY',headers=17),
    load(source_url,format='xlsx',sheet='CONSTANT-MORTALITY',headers=17),
    load(source_url,format='xlsx',sheet='INSTANT-REPLACEMENT',headers=17),
    load(source_url,format='xlsx',sheet='MOMENTUM',headers=17),
    load(source_url,format='xlsx',sheet='ZERO-MIGRATION',headers=17),
    load(source_url,format='xlsx',sheet='NO CHANGE',headers=17),
    delete_fields(fields=['Index', 'Variant', 'Notes']),
    rename_resources,
    unpivot(
        unpivot_fields=[{'name': '([0-9]{4})', 'keys': {'year': '\\1'}}],
        extra_keys=[{'name': 'year', 'type': 'year'}],
        extra_value={'name': 'population', 'type': 'number'},
        resources='population-estimates'
    ),
    unpivot(
        unpivot_fields=[{'name': '([0-9]{4})', 'keys': {'year': '\\1'}}],
        extra_keys=[{'name': 'year', 'type': 'year'}],
        extra_value={'name': 'population', 'type': 'number'},
        resources=resource_names[1:]
    ),
    add_computed_field(fields=[
        {
        "operation": "format",
        "target": "Region",
        "with": "{Region, subregion, country or area *}"
        },
        {
        "operation": "format",
        "target": "Country Code",
        "with": "{Country code}"
        },
        {
        "operation": "format",
        "target": "Year",
        "with": "{year}"
        },
        {
        "operation": "format",
        "target": "Population",
        "with": "{population}"
        }
    ]),
    delete_fields(fields=[
        'Region, subregion, country or area *', 'Country code', 'year', 'population'
    ]),
    validate()
)

def flow(parameters, datapackage, resources, stats):
    return population_estimates

if __name__ == '__main__':
    population_estimates.process()
