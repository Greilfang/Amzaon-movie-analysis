import pymongo
import json
import os


class IntroHandler:
    def __init__(self, addr='localhost', port=27017, base_name='Amazon-Movies'):
        # def __init__(self,addr='localhost',port=27017,base_name='Amazon-Movie'):
        self.client = pymongo.MongoClient(addr, port)
        self.database = self.client[base_name]

    def insert_all_reviews(self, path, collection_name='Reviews'):
        collection = self.database[collection_name]
        names = os.listdir(path)
        count = 0
        for name in names:
            with open(path + '\\{}'.format(name)) as f:
                data = json.load(f)
                for review in data['Reviews']:
                    count = count + 1
                    review['Title'] = data['Title']
                    review['MovieID'] = data['ID']
                    collection.insert_one(review)
                    if count % 10000 == 0:
                        print("{} reviews inserted".format(count))

    def insert_all_intros(self, path, collection_name='Intros'):
        collection = self.database[collection_name]
        names = os.listdir(path)
        count = 0
        for name in names:
            with open(path + '\\{}'.format(name)) as f:
                data = json.load(f)
                if not data['Intro']:
                    continue
                intro = dict()
                intro['MovieID'] = data['ID']
                intro['Title'] = data['Title']
                intro['Intro'] = data['Intro']
                collection.insert_one(intro)
                count = count + 1
                if count % 1000 == 0:
                    print("{} intros inserted".format(count))

    def insert_all_people(self, path, collection_name='Details'):
        collection = self.database[collection_name]
        names = os.listdir(path)
        count = 0
        for name in names:
            with open(path + '\\{}'.format(name)) as f:
                data = json.load(f)
                peoples = dict()
                peoples['MovieID'] = data['ID']
                peoples['Director'] = data['Director']
                if data['Supporting']:
                    peoples['Actor'] = data['Starring'] + data['Supporting']
                else:
                    peoples['Actor'] = data['Starring']
                peoples['Genre'] = data['Genre']
                peoples["Intro"] = data["Intro"]
                peoples["Emotion"] = data["Emotion"] if "Emotion" in data else 0.5
                collection.insert_one(peoples)
                count = count + 1
                if count % 1000 == 0:
                    print("{} details inserted".format(count))