import random
import itertools

class Study:
    def __init__(self, json):
        bib = json["bib"]
        self.summary = bib["abstract"]
        self.title = bib["title"]
        self.pub_year = bib["pub_year"]
        self.authors = bib["author"]

        self.links= (json["pub_url"], json["eprint_url"])
        self.num_citations = json["num_citations"]
        

    def __hash__(self):
        return hash(self.title)
     

class Keyword:

    studies = set()

    def __init__(self, name, words):
        self.keyword = name
        self.related_keywords = words.split(", ")


    def addStudy(self, study):
        self.studies.add(study)
        

    def getKeyword(self):
        return random.choice(self.related_keywords)


   
