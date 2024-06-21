from bs4 import BeautifulSoup
import time
import re
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from app.config import config




def update_url(original_url, start_value):
    # Parse the original URL
    parsed_url = urlparse(original_url)
    # Parse the query parameters
    query_params = parse_qs(parsed_url.query)
    # Update the start parameter
    query_params['start'] = [str(start_value)]
    # Encode the updated query parameters
    updated_query = urlencode(query_params, doseq=True)
    # Rebuild the updated URL
    updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, 
                              parsed_url.params, updated_query, parsed_url.fragment))
    return updated_url

def get_html(url):
    try:
        payload = { 'api_key': config.SCRAPER_API_KEY, 'url': url }
        response = requests.get('https://api.scraperapi.com/', params=payload)
        if response.status_code != 200:
            print("Error: Failed to retrieve the webpage")
            return
        html_content = response.content
        return html_content
    except Exception as e:
        print(f"error while getting html: {e}")


def extractScholar(soup, all_items_json, start_value):
    array = []
    items = soup.find_all("div", class_="gs_ri")
    nr_items = start_value
    
    for item in items:
        nr_items += 1
        item_data = {}

        h3_tag = item.find('h3', class_='gs_rt')
        a_tag = h3_tag.find('a')
        span_tag = h3_tag.find('span', id=True)
        if a_tag:
            item_data["title"] = a_tag.get_text(strip=True)
            item_data["urlCit"] = a_tag['href']
        elif span_tag:
            item_data["title"] = span_tag.get_text(strip=True)

        div_tag = item.find('div', class_='gs_a')
        if div_tag:
            authors_string = div_tag.get_text(strip=True)
            
            # Find the year (a four-digit number)
            year_match = re.search(r'\b(19\d{2}|20\d{2}|21\d{2}|22\d{2})\b', authors_string)
            item_data["year"] = int(year_match.group(0)) if year_match else None
            
            # Split the string by ' - ' separator
            parts = authors_string.split('- ')
            item_data["authors"] = parts[0] if len(parts) > 0 else ""
            item_data["conference"] = parts[1] if len(parts) > 1 else ""
                        
            # Check for a URL pattern
            url_pattern = re.compile(r'\b[a-zA-Z]+(?:\.[a-zA-Z]+)+\b')
            item_data["url"] = next((part for part in parts if url_pattern.search(part)), '-')
            
            # Add remaining parts to "others" excluding the URL
            item_data["others"] = [part for part in parts[2:] if not url_pattern.search(part)]
        
        array.append(item_data)
        all_items_json[f"cit_{nr_items}"] = item_data
    
    if len(array) == 0 or len(array) < 10:
        return -1
    all_items_json["count"] = len(all_items_json)
    return all_items_json

def get_citations_info(url):
    start_value = 0
    current_url = url
    all_items_json = {}
    html_text = get_html(url)
    while True:
        soup_text = BeautifulSoup(html_text, 'html.parser')
        time.sleep(3)
        result = extractScholar(soup_text, all_items_json, start_value)
        if result == -1:
            break
        time.sleep(2) 
        all_items_json = result
        start_value += 10
        current_url = update_url(url, start_value)
        html_text = get_html(current_url)

    return all_items_json


# AUGMENTED_REALITY= 'https://scholar.google.co.uk/scholar?oi=bibs&hl=en&cites=3534690389194926257'
# AUGMENTED_REALITY2= 'https://scholar.google.co.uk/scholar?start=20&hl=en&cites=3534690389194926257'

# get_citations_info(AUGMENTED_REALITY)