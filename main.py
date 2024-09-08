from scholarly import scholarly
import json
from studies import Keyword, Study
from itertools import combinations
from time import sleep

# number of random keywords to query with each domain
NUM_KEYWORDS = 3
# maximum number of keywords to query google scholar per domain
MAX_COMBINATIONS = 5
# Seconds between each query to avoid a rate limit
QUERY_INTERVAL = 5
# Number of publications to get from each query
NUM_RESULTS = 15

PATH_TO_OUTPUT = "output/studies.json"


with open("config.json") as f:
    config = json.load(f)
    keywords = config["Keywords"]
    domains = config["Domains"]


activeKeywords = list()
activeDomains = list()


for word in keywords:
    keyword = Keyword(word, keywords[word])
    activeKeywords.append(keyword)


for domain in domains:
    domain = Keyword(domain, domains[domain])
    activeDomains.append(domain)


for domain in activeDomains:
    combos = combinations(activeKeywords, NUM_KEYWORDS)
    for combo in list(combos)[:MAX_COMBINATIONS]:
        chosen_keywords = [word.getKeyword() for word in combo] + [domain.getKeyword(),]
        query = " ".join(chosen_keywords)
        search_results = scholarly.search_pubs(query)

        for i in range(NUM_RESULTS):
            try:
                study = Study(next(search_results), combo)
                print(f"Retrieved study {study.title}")
            except Exception:
                print(str(Exception))
                continue

            for keyword in combo:
                keyword.addStudy(study)
        
        sleep(QUERY_INTERVAL)


output_json = dict()


for domain in activeDomains:
    output_json["Domains"] = dict()
    output_json["Domains"][domain.keyword] = [study.toJson() for study in domain.getStudies()]
    
for keyword in activeKeywords:
    output_json["Keywords"] = dict()
    output_json["Keywords"][keyword.keyword] = [study.toJson() for study in keyword.getStudies()]


with open(PATH_TO_OUTPUT) as f:
    json.dump(output_json)
    
    






