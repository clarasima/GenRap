import requests
from bs4 import BeautifulSoup

def extractDBLP(url):
    response = requests.get(url)
    array = []
    if response.status_code != 200:
        print("Error: Failed to retrieve the webpage")
        return
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")

    publications = soup.find_all("li", class_="entry")
    nr_pub =0
    # Iterate over the publications 
    all_publications_json= {}
    for publication in publications:
        nr_pub= nr_pub +1
        pub_id = publication.get("id")
        pub_data = {"dblp_id": pub_id, "authors": []}

        title_span = publication.find('cite').find('span', class_='title')
        pub_title = title_span.get_text(strip=True)
        pub_title = pub_title.rstrip('.')
        pub_data["title"] = pub_title

        pub_class = publication.get("class")

        nr_span = publication.find('div', class_='nr')
        pub_nr = nr_span.get_text(strip=True)

        category_name = publication.find('div', class_='box').find('img').get('title')

        pub_data["category_dblp"] = {
            "category_name": category_name,
            "nr": pub_nr,
            "class":pub_class
        }

        conference_span = publication.find('cite', class_='data tts-content').find('span', itemprop='isPartOf')
        if conference_span is not None:
            pub_conference = conference_span.get_text(strip=True)
            pub_data["conference"] = pub_conference
        else:
            # happens for books
            filtered_strings = [s for s in publication.find('cite').contents if '<' not in str(s) and ':' not in str(s)]
            result_string = ''.join(filtered_strings)
            pub_data["conference"] = result_string
        date_span = publication.find('cite', class_='data tts-content').find('span', itemprop='datePublished')
        pub_date = date_span.get_text(strip=True)
        pub_data["year"] = pub_date

        author_spans= publication.find_all("span", itemprop="author")
        for author_span in author_spans:
            author_name = author_span.get_text(strip=True)
            pub_data["authors"].append(author_name)
        all_publications_json[pub_date + ' '+  pub_id] = pub_data
        array.append(pub_data)
    return all_publications_json


andrei_arusoaie="https://dblp.org/pid/76/9867.html"
ciobaca="https://dblp.org/pid/08/7193.html"  
lucanu="https://dblp.org/pid/43/2947.html" 
vlad_rusu="https://dblp.org/pid/42/834.html" 
grigore_rosu="https://dblp.org/pid/r/GrigoreRosu.html"
daniel_stamate="https://dblp.org/pid/49/3534.html"

extractDBLP(daniel_stamate)
