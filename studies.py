import random
import itertools



class Study:
    def __init__(self, json, keywords):
        print(json)
        self.bib = json["bib"]
        self.summary = self.bib["abstract"]
        self.title = self.bib["title"]
        self.pub_year = self.bib["pub_year"]
        self.authors = self.bib["author"]

        self.links= (json["pub_url"])
        self.num_citations = json["num_citations"]

        self.keywords = keywords
        

    # Hash each study for use in sets based on its title
    def __hash__(self):
        return hash(self.title)
    
    
    def __str__(self):
        return f"{self.title} by {self.authors}"
    
# Formats the study to be output into a json file 
    def toJson(self):
        json = dict()
        json["title"] = self.title
        json["link"] = self.links
        json["citations"] = self.num_citations
        json["summary"] = self.summary
        json["keywords"] = self.keywords

     


class Keyword:

    def __init__(self, name, words):
        self.keyword = name
        self.related_keywords = words.split(", ")
        self.studies = set()


    def addStudy(self, study):
        self.studies.add(study)
        

    def getStudies(self):
        return self.studies

    def getKeyword(self):
        return random.choice(self.related_keywords)
    
    
    def __str__(self):
        return str([str(study) for study in self.studies])



   
