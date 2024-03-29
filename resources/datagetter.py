# -*- coding: utf-8 -*-
from owid import catalog
import pandas as pd
import random
import re
import numpy as np
import sys

content_path = sys.argv[1]

yesno = re.compile(" \(1 = yes(;|,) 0 = no\)", re.IGNORECASE)

def prepare_data(table):
    # Create a dataframe with a dummy index from the table.
    df = pd.DataFrame(table).reset_index()

    # Sort rows and columns conveniently.
    #if ('country' in 
    #df = df.sort_values(["country", "year"]).reset_index(drop=True)
    #first_columns = ["country", "year", "iso_code"]
    
    return df

def format_country(country):
    if '(' in country:
        return '"' + country + '"'
    return country

def format_year(year):
    if year < 0:
        return str(-year) + ' BC'
    return str(year)
def clean_desc_with_value(raw_desc, value, year):
    clean_desc = raw_desc[::]
    print(raw_desc)
    if '(%)' in raw_desc:
        clean_desc = clean_desc.replace(' (%)', '')
        value_str = str(value) + '%'
        
    elif yesno.search(clean_desc):
        print('yesno')
        clean_desc = yesno.sub(clean_desc)
        value_str = 'yes' if str(value) == '1' else 'no'
    else:
        print(type(value))
        if isinstance(value, np.uint32):
            value_str = format(value, ',d')
        elif isinstance(value, np.float32):
            value_str = str(round(value, 2))
        else:
            value_str = str(value)
        
    clean_desc = clean_desc.replace(' (ratio)', '')
    clean_desc = '*' + clean_desc[0].lower() + clean_desc[1:] + '*'
    verb = 'is' if year == 2023 else 'was'
    return clean_desc, verb, value_str

def test_clean_desc():
    clean_desc,verb,value_str = clean_desc_with_value('the countries with an allocation from the national budget to manage the threat of invasive alien species (1 = yes, 0 = no)', 0, 2020)
    output = get_output('Burundi', 2020, clean_desc, verb, value_str)
    print(output)
    return output == "In Burundi in 2020, the countries with an allocation from the national budget to manage the threat of invasive alien species (1 = yes, 0 = no) was 0"


def get_output(country, clean_year, clean_desc, verb, value_str):
    end_of_phrase = clean_desc + ' ' + verb + ' ' + value_str
    if value_str in { 'yes','no'}:
        return "In {0}, {1} was one of {2} ".format(clean_year, country, clean_desc)
    else:
        return "In {0} in {1}, the {2}".format(country, clean_year, end_of_phrase)

country_overview_translations = {
        'population': 'population',
        'emissions_total_per_capita': 'total emissions per capita', 
        'share_pop_using_internet': 'share of population using the internet',
        'gdp_per_capita': 'gdp per capita', 
        'share_electricity_access': 'share of electricity access',
        'life_expectancy_at_birth': 'life expectancy at birth',
        'deaths__interpersonal_violence__sex__both__age__all_ages__rate': 'rate of death due to interpersonal violence across all ages and sexes'
       }

datasets_to_skip = {
'Additional variables',
'Equaldex dataset'
        }

def get_random_data():
    title = None
    while any([(title == None) or (d in title) for d in datasets_to_skip]):
        results = catalog.find('')
        result = results.sample().load()
        metadata = result.metadata
        data = metadata.dataset
        title = metadata.title
        description = metadata.dataset.description
        if title == None:
            title = metadata.dataset.title

        print(title)
        print(description)

        df= prepare_data(result)

    return result,df,metadata

def get_output_string_from_df(result, df, metadata):
    title = metadata.dataset.title
    row = df.sample(1)


    if 'Country Profile Overview' in title:
        column = random.choice([c for c in set(country_overview_translations.keys()).intersection(row.columns) if not pd.isna(row[c].iloc[0])])
        desc = country_overview_translations[column]
        value = row[column].iloc[0]

    elif 'seriesdescription' not in row.columns:
        column = random.choice([c for c in row.columns if c not in {'country', 'year'} and not pd.isna(row[c].iloc[0])])
        desc = result[column].metadata.title
        if result[column].metadata.description:
            desc += ' (' + result[column].metadata.description + ')'
        value = row[column].iloc[0]

    else:
        desc = row.seriesdescription.iloc[0]
        value = row.value.iloc[0]

    country = row.country.iloc[0]
    year = row.year.iloc[0]
    (clean_desc,verb,value_str) = clean_desc_with_value(desc, value, year)
    clean_year = format_year(year)
    clean_country = format_country(country)

    return get_output(clean_country, clean_year, clean_desc, verb, value_str)

if __name__ == "__main__":
    data_sent = False
    while not data_sent:
        try:
            result,df,metadata = get_random_data()
            output = get_output_string_from_df(result,df,metadata)
            print(output)
            with open (content_path, 'w') as f:
                f.write(output)
            data_sent = True
        except Exception as e:
            print(e)
