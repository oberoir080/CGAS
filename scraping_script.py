import requests
from bs4 import BeautifulSoup
import json
import time
import random

#recipe name
#recipe url
#recipe ingredients
#recipe instructions
#recipe cuisine
#recipe prep time

def get_recipe_ingredient(json_data,url):
    d={}
    d['recipe_name']=json_data[0]['name']
    d['url']=url
    d['recipe_Ingredients'] = json_data[0]['recipeIngredient']
    d['Instructions'] = json_data[0]['recipeInstructions']
    d['cuisine'] = json_data[0]['recipeCuisine']
    d['prep_time'] = json_data[0]['cookTime']
    return d

c=-1
def get_random_user_agent():
    global c
    c+=1
    """Return a random User-Agent string to avoid being blocked by websites."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    # return random.choice(user_agents)
    return user_agents[c%3]

def extract_ingredients(url):
    """Scrape the ingredients from a recipe URL using BeautifulSoup and JSON-LD data."""
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the script tag containing JSON-LD data
        json_ld_script = soup.find('script', type='application/ld+json')
        
        if json_ld_script:
            # Parse the JSON data
            json_data = json.loads(json_ld_script.string)
            # print(json_data[0])
            return get_recipe_ingredient(json_data,url)
        else:
            print(f"No JSON-LD script found for {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error processing {url}: {str(e)}")
        return None

# Read URLs from file
file_path = 'url_set.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    urls = file.read().splitlines()

# Limit to 5 URLs for testing
urls = urls[:5]

# Extract ingredients from each URL
results = {}
for i, url in enumerate(urls):
    print(f"Processing URL {i+1}/{len(urls)}: {url}")
    ingredients = extract_ingredients(url)
    if ingredients:
        results[url] = ingredients
    
    # Add a random delay between requests
    # time.sleep(random.uniform(1, 3))

# Print results
print("Extracted Ingredients from URLs:")
# for url, ingredients in results.items():
    # print(f"{url}: {ingredients}")

# Save results to a JSON file
output_file = 'recipe_ingredients.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"Processed {len(results)} URLs. Results saved to {output_file}")
