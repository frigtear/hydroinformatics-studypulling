import scholarly
import json
from studies import Keyword, Study
from itertools import combinations
from time import sleep

# number of keywords to query with each domain
NUMBER_KEYWORDS = 3
# maximum number of keywords to query google scholar per domain
MAX_COMBINATIONS = 5
# Seconds between each query to avoid a rate limit
QUERY_INTERVAL = 5

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
    keyword = Keyword(domain, domains[domain])
    activeDomains.append(domain)


for domain in activeDomains:
    combos = combinations(activeKeywords, NUMBER_KEYWORDS)
    for combo in list(combos)[:MAX_COMBINATIONS]:
        chosen_keywords = [word.getKeyword() for word in combo] + [domain,]
        querystring = " ".join(chosen_keywords)
        print(chosen_keywords)
    

# do every combo of 2 keywords



