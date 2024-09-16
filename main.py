from scholarly import scholarly, ProxyGenerator
import json
from studies import Keyword, Study
from itertools import combinations
from time import sleep
from requests import ConnectionError, ConnectTimeout


# number of random keywords to query with each domain
NUM_KEYWORDS = 3
# maximum number of keywords to query google scholar per domain
MAX_COMBINATIONS = 5
# Seconds between each query to avoid a rate limit
QUERY_INTERVAL = 1
# Number of publications to get from each query
NUM_RESULTS = 15
# Path to json output
PATH_TO_OUTPUT = "output/studies.json"


with open("config.json") as f:
    config = json.load(f)
    keywords = config["Keywords"]
    domains = config["Domains"]
    proxy_url = config["ProxyUrl"]


pg = ProxyGenerator()
success = pg.SingleProxy(https = proxy_url)

if not success:
    print("Warning: Could not set up proxy, Are you sure you used the right Url?")
else:
    print("proxies set up succesfully")
    scholarly.use_proxy(pg)


activeKeywords = list()
activeDomains = list()

''' builds keyword objects out of the keywords in the config'''
for word in keywords:
    keyword = Keyword(word, keywords[word])
    activeKeywords.append(keyword)

for domain in domains:
    domain = Keyword(domain, domains[domain])
    activeDomains.append(domain)

count = 0

''' Gets every combination of keywords, builds a query out of the first MAX_COMBINATIONS of them, and builds a study object out of each result. Stores the found studies in each keyword object'''
for domain in activeDomains:
    # Get a NUM_KEYWORDS sized list of every possible combinations of keywords
    combos = combinations(activeKeywords, NUM_KEYWORDS)
    for combo in list(combos)[:MAX_COMBINATIONS]:

        chosen_keywords = [word.getKeyword() for word in combo] + [domain.getKeyword(),]
        query = " ".join(chosen_keywords)
        search_results = scholarly.search_pubs(query)
            
        for i in range(NUM_RESULTS):
            try:
                study = Study(next(search_results), combo)
                print(f"Retrieved study {study.title} with query {query}")
            except StopIteration:
                print(f"Exausted studies with query {query}, skipping")
                continue
            except ConnectTimeout or ConnectionError:
                print("connection or timeout error, disabling proxies")
                scholarly.use_proxy(None)
            except Exception as e:
                # Handles any study with missing information or unforseen issue
                print(f"{e} with paring study, disabling proxy")
                continue

            for keyword in combo:
                keyword.addStudy(study)
        
        sleep(QUERY_INTERVAL)

        count = count + 1


output_json = dict()

''' Outputs each keyword and its studies into a json file'''
output_json["Domains"] = dict()
for domain in activeDomains:
    output_json["Domains"][domain.keyword] = [study.toJson() for study in domain.getStudies()]
    
output_json["Keywords"] = dict()
for keyword in activeKeywords:
    output_json["Keywords"][keyword.keyword] = [study.toJson() for study in keyword.getStudies()]


with open(PATH_TO_OUTPUT, "w") as f:
    json.dump(output_json, f)
    
    






