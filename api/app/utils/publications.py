import re
from difflib import SequenceMatcher

def normalize_title(title):
    # Convert to lowercase and remove punctuation
    return re.sub(r'[^\w\s]', '', title.lower())

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def extract_last_names(authors):
    def get_last_name(name):
        tokens = re.split(r'\s+', name.strip())
        return tokens[-1].lower()  # Last token is assumed to be the last name
    
    return {get_last_name(author) for author in authors}

def match_authors(authors1, authors2):
    # Extract last names for comparison
    set1 = extract_last_names(authors1)
    set2 = extract_last_names(authors2)

    # Calculate the intersection and union
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) > 0.5  # Adjust threshold as needed


def normalize_authors(authors):
    return {re.sub(r'\b\w\b', '', author.lower()).strip() for author in authors}



def find_similar_publications(dblp_data, scholar_data):
    matches = []
    scholar_keys_to_ignore = set()

    if isinstance(dblp_data, dict):
        for key1, pub1 in dblp_data.items():
            if not isinstance(pub1, dict):
                continue
            title1 = normalize_title(pub1.get('title', ''))
            authors1 = normalize_authors([author for author in pub1.get('authors', [])])
            year1 = pub1.get('year', '')

            matched = False
            if isinstance(scholar_data, dict):
                for key2, pub2 in scholar_data.items():
                    if not isinstance(pub2, dict):
                        continue

                    title2 = normalize_title(pub2.get('title', ''))
                    authors2 = normalize_authors(pub2.get('authors', []))
                    year2 = pub2.get('year', '')

                    if similar(title1, title2) > 0.7 and match_authors(authors1, authors2) and year1 == year2:
                        matches.append({"dblp": pub1, "scholar": pub2, "match": True})
                        scholar_keys_to_ignore.add(key2)
                        matched = True
                        break

            if not matched:
                pub1['source'] = 'dblp'
                matches.append({"dblp": pub1})

    if isinstance(scholar_data, dict):
        for key2, pub2 in scholar_data.items():
            if key2 in scholar_keys_to_ignore or not isinstance(pub2, dict):
                continue

            pub2['source'] = 'scholar'
            matches.append({"scholar": pub2})

    return matches

