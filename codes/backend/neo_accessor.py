import neo4j
import time


class RelationHandler:
    def __init__(self):
        self.driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "little_hug1020"))

    def check_d_a_relations(self, name, top_num):
        graph = dict()

        def get_qualified_director(tx, d_name):
            nodes = tx.run(
                "Match (d:director) Where d.Name =~'.*{d_name}.*' Return d Limit 150".format(d_name=d_name)
            )
            results = [node['d'].get("Name") for node in nodes.data()]
            return results

        session = self.driver.session()
        directors = session.write_transaction(get_qualified_director, name)
        session.close()

        def get_d_a_coops(tx, d_name, nums):
            results = tx.run(
                "Match (d:director{Name:$Name})-[r1:D_COOP_A]->(a:actor)"
                "With d,a Order by r1.Times Desc Limit $nums "
                "Match (a)-[r2:ACT_MOVIE]->(m) "
                "With d,a,m Match (m)<-[r3:DIRECT_MOVIE]-(d) "
                "return a,m", Name=d_name, nums=nums
            )
            results = results.data()
            actors_movies = {}
            for result in results:
                actor_name = result['a'].get("Name")
                if actor_name not in actors_movies:
                    actors_movies[actor_name] = []
                actors_movies[actor_name].append(result['m'].get('Title'))
            return actors_movies

        for director in directors:
            session = self.driver.session()
            actors_to_movies = session.write_transaction(get_d_a_coops, director, top_num)
            graph[director] = actors_to_movies
            session.close()
        return graph

    def check_a_a_relations(self, name, top_num):
        graph = dict()

        def get_qualified_actor(tx, a_name):
            nodes = tx.run(
                "Match (a:actor) Where a.Name =~'.*{a_name}.*' Return a Limit 300".format(a_name=a_name)
            )
            results = [node['a'].get("Name") for node in nodes.data()]
            return results

        session = self.driver.session()
        actors = session.write_transaction(get_qualified_actor, name)
        session.close()

        def get_a_a_coops(tx, a_name, nums):
            results = tx.run(
                "Match (a:actor{Name:$Name})-[r1:A_COOP_A]-(d:actor)"
                "With a,d Order by r1.Times Desc Limit $nums "
                "Match (d)-[r2:ACT_MOVIE]->(m) "
                "With a,d,m Match (m)<-[r3:ACT_MOVIE]-(a) "
                "return d,m", Name=a_name, nums=nums
            )
            results = results.data()
            actors_movies = dict()
            for result in results:
                actor_name = result['d'].get("Name")
                if actor_name not in actors_movies:
                    actors_movies[actor_name] = []
                actors_movies[actor_name].append(result['m'].get('Title'))
            return actors_movies

        for actor in actors:
            session = self.driver.session()
            actors_to_movies = session.write_transaction(get_a_a_coops, actor, top_num)
            graph[actor] = actors_to_movies
            session.close()
        return graph

    def check_a_d_relations(self, name, top_num):
        graph = dict()

        def get_qualified_actor(tx, a_name):
            nodes = tx.run(
                "Match (a:actor) Where a.Name =~'.*{a_name}.*' Return a Limit 300".format(a_name=a_name)
            )
            results = [node['a'].get("Name").replace("'", "").replace('"', "") for node in nodes.data()]
            return results

        session = self.driver.session()
        actors = session.write_transaction(get_qualified_actor, name)
        session.close()

        def get_a_d_coops(tx, a_name, nums):
            results = tx.run(
                "Match (a:actor{Name:$Name})<-[r1:D_COOP_A]-(d:director)"
                "With a,d Order by r1.Times Desc Limit $nums "
                "Match (d)-[r2:DIRECT_MOVIE]->(m) "
                "With a,d,m Match (m)<-[r3:ACT_MOVIE]-(a) "
                "return d,m",Name=a_name,nums=nums
            )
            results = results.data()
            directors_movies = dict()
            for result in results:
                director_name = result['d'].get("Name")
                if director_name not in directors_movies:
                    directors_movies[director_name] = []
                directors_movies[director_name].append(result['m'].get('Title'))
            return directors_movies

        for actor in actors:
            session = self.driver.session()
            directors_to_movies = session.write_transaction(get_a_d_coops, actor, top_num)
            graph[actor] = directors_to_movies
            session.close()
        return graph
