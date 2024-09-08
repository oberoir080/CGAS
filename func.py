from spacy.matcher import Matcher
from spacy.tokens import Span
from spacy.language import Language
from collections import defaultdict
import pandas as pd
import spacy
import csv
import re


#Extracting text from the list of dictionary
def extract_instruction_text(df):
    def combine_text(instructions):
        if isinstance(instructions, list):
            return ' '.join(step['text'] for step in instructions if 'text' in step)
        return instructions  # Return as is if it's not a list

    df['Instructions'] = df['Instructions'].apply(combine_text)
    return df

#Extracting the numerical value from prep time column
def extract_prep_time_minutes(df, column_name='prep_time'):
    def extract_minutes(time_string):
        if pd.isna(time_string):
            return None
        match = re.search(r'PT(\d+)M', time_string)
        return int(match.group(1)) if match else None

    # Extract minutes and create a new column
    df['Prep Time in Minutes'] = df[column_name].apply(extract_minutes)
    
    # Drop the original column
    df = df.drop(columns=[column_name])
    
    return df

#Converting the list to string
def list_to_string(ingredients_list):
    return ', '.join(ingredients_list)


#Creating the recipe frequency distribution
def process_recipes(recipe_text):
    lines = recipe_text.strip().split('\n')
    ingredient_freq = defaultdict(int)

    for line in lines:
        parts = line.split('-')
        if len(parts) == 2:
            recipe_id, ingredient = parts
            recipe_id = recipe_id.strip()
            ingredient = ingredient.strip()

            # Attempt to capture the full ingredient name, ignoring leading numbers
            ingredient_parts = ingredient.split()
            if ingredient_parts[0].isdigit():
                ingredient_name = ' '.join(ingredient_parts[1:])
            else:
                ingredient_name = ingredient

            # Increase the frequency count for the ingredient
            ingredient_freq[ingredient_name] += 1

    return dict(ingredient_freq)


def save_to_csv(ingredient_freq, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Ingredient', 'Frequency'])
        for ingredient, frequency in ingredient_freq.items():
            writer.writerow([ingredient, frequency])


