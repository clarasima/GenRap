from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import copy
from urllib.parse import urlparse, parse_qs

LUCANU = 'https://scholar.google.co.uk/citations?user=2YOn9jkAAAAJ&hl=en'
ARUSOAIE = 'https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=uA4nRXEAAAAJ&sortby=title'
RUSU = 'https://scholar.google.com/citations?user=uDBCQR8AAAAJ&hl=en'

def get_html(url):
    chrome_options = Options()

    # Automatically download and setup ChromeDriver
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)
    
    prev_span_text = ""
    try:
        # Loop to repeatedly click the "Show more" button until it's disabled
        while True:
            button = driver.find_element(By.ID, 'gsc_bpf_more')

            # Check if the button is disabled
            if button.get_attribute('disabled'):
                span = driver.find_element(By.ID, 'gsc_a_nn')
                current_span_text = span.text
                if current_span_text != prev_span_text:
                    prev_span_text = current_span_text
                else:
                    html_copy = copy.deepcopy(driver.page_source)
                    return html_copy

            # Click the "Show more" button
            button.click()
            time.sleep(2)

    finally:
        # Close the browser window when done
        driver.quit()

def extractScholar(soup):
    array = []
    publications = soup.find_all("tr", class_="gsc_a_tr")

    nr_pub = 0
    all_publications_json = {}
    for publication in publications:
        nr_pub += 1
        pub_info = publication.find('td', class_='gsc_a_t')
        id_a = pub_info.find('a')
        href_pub = 'https://scholar.google.co.uk/' + id_a.get("href")

        parsed_url = urlparse(href_pub)
        query_params = parse_qs(parsed_url.query)
        user = query_params.get('user', [None])[0]
        citation_for_view = query_params.get('citation_for_view', [None])[0]

        pub_title = id_a.get_text(strip=True)
        pub_data = {"id": href_pub, "authors": [], "href": href_pub, "title": pub_title, "scholar_id":user+'_'+citation_for_view}

        # CONFERENCE
        authors_and_conference = pub_info.findAll('div', class_="gs_gray")
        authors_dom = authors_and_conference[0]
        if len(authors_and_conference) > 1:
            conference_dom = authors_and_conference[1]
        conference_pub = conference_dom.get_text(strip=True)
        pub_data["conference"] = conference_pub

        # AUTHORS
        authors = authors_dom.get_text(strip=True)
        pub_data["authors"] = authors.split(', ')

        # Citations
        citations = publication.find('td', class_='gsc_a_c')
        citations_dom = citations.find('a')
        href_citations = citations_dom.get("href")
        citations_nr = citations_dom.get_text(strip=True)
        pub_data["citations"] = {"href": href_citations}
        if citations_nr != '':
            pub_data["citations"]["nr"] = citations_nr

        # YEAR
        year_dom = publication.find('td', class_='gsc_a_y')
        year = year_dom.get_text(strip=True)
        pub_data["year"] = year
        all_publications_json[year + ' ' + href_pub] = pub_data
        array.append(pub_data)
    return all_publications_json

def get_scholar_info(url):
    html_text = get_html(url)
    soup_text = BeautifulSoup(html_text, 'html.parser')
    return extractScholar(soup_text)
