from flask import Flask
from flask import request, jsonify
import click
from sql_accessor import SQLMovieHandler
from mongo_accessor import IntroHandler
from neo_accessor import RelationHandler
import time
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
sql_accessor = SQLMovieHandler()
mongo_accessor = IntroHandler()
neo_accessor = RelationHandler()


@app.cli.command()
def initdb():
    sql_accessor.create_all()
    click.echo('database initialized')


@app.cli.command()
def dropdb():
    sql_accessor.drop_all()
    click.echo('database dropped')


@app.cli.command()
@click.argument("path")
def insert_all_movies(path):
    sql_accessor.insert_all_movie_basics(path)


@app.cli.command()
@click.argument("path")
def insert_all_genres(path):
    sql_accessor.insert_all_movie_genres(path)


@app.cli.command()
@click.argument("path")
def insert_all_reviews(path):
    mongo_accessor.insert_all_reviews(path)


@app.cli.command()
@click.argument("path")
def insert_all_intros(path):
    mongo_accessor.insert_all_intros(path)


@app.cli.command()
@click.argument("path")
def insert_all_peoples(path):
    mongo_accessor.insert_all_people(path)


@app.route('/')
def hello_world():
    return 'This is our DataWarehousing Project'


"""
查询基本信息接口
"""


@app.route('/api/query_movie_list', methods=['POST'])
def query_movie_list():
    stime = time.time()
    # 冗余信息
    director = request.json.get('director')
    actors = request.json.get('actor')
    intro = request.json.get('intro')
    ids = None
    if not director == "" or not actors == "" or not intro == "":
        # 增加一个neo4j 查询 id 的方法
        # 直接全mysql
        ids = mongo_accessor.query_id_with_bundent(director, actors, intro)
    mtime = time.time()
    # 基本信息
    start_from = request.json.get('start_from')
    end_until = request.json.get('end_until')
    genre = request.json.get('genre')
    movie_name = request.json.get('movie_name')
    emotion = request.json.get('emotion')
    score_from = request.json.get('score_from')
    score_to = request.json.get('score_to')

    result = sql_accessor.query_movie_list(
        ids=ids,
        start_from=start_from,
        end_until=end_until,
        movie_name=movie_name,
        genre=genre,
        emotion=emotion,
        score_from=score_from,
        score_to=score_to
    )
    etime = time.time()
    return jsonify({'flag': True, 'data': result,
                    'meta': {'duration': etime - stime, 'mongotime': mtime - stime, 'amount': len(result)}})


"""
查询冗余信息接口
"""


@app.route('/api/query_movie_details', methods=['POST'])
def query_movie_details():
    stime = time.time()
    director = request.json.get('director')
    actors = request.json.get('actor')
    intro = request.json.get('intro')
    genre = request.json.get('genre')
    ids, more_info = None, None
    if not director == "" or not actors == "" or not intro == "" or not genre == "":
        more_info = mongo_accessor.query_more_info_with_bundent(director, actors, intro, genre)
        ids = list(more_info.keys())
    mtime = time.time()
    start_from = request.json.get('start_from')
    end_until = request.json.get('end_until')
    movie_name = request.json.get('movie_name')
    emotion = request.json.get('emotion')
    score_from = request.json.get('score_from')
    score_to = request.json.get('score_to')

    basic_info = sql_accessor.query_movie_details(
        ids=ids,
        start_from=start_from,
        end_until=end_until,
        movie_name=movie_name,
        emotion=emotion,
        score_from=score_from,
        score_to=score_to
    )
    etime = time.time()
    ids = list(basic_info.keys())
    if more_info is None:
        more_info = mongo_accessor.query_more_info_with_ids(ids)
    result = [dict(basic_info[k], **more_info[k]) for k in ids]
    return jsonify({'flag': True, 'data': result,
                    'meta': {'duration': etime - stime, 'mongotime': mtime - stime, 'amount': len(result)}})


"""
查询关系接口
"""


@app.route('/api/query_relations', methods=['POST'])
def query_relations():
    stime = time.time()
    role = request.json.get('role')
    name = request.json.get('name')
    target = request.json.get('target')
    top_nums = request.json.get('top_nums')
    graph = {
        "nodes": [],
        "links": [],
        "category": []
    }
    dict_graph = None
    if role == "director" and target == "actor":
        dict_graph = neo_accessor.check_d_a_relations(name, top_nums)
    elif role == "actor" and target == "actor":
        dict_graph = neo_accessor.check_a_a_relations(name, top_nums)
    elif role == "actor" and target == "director":
        dict_graph = neo_accessor.check_a_d_relations(name, top_nums)
    uuid = 0
    for key_1 in dict_graph.keys():
        graph["nodes"].append({"name": key_1, "category": key_1, "id": uuid})
        graph["category"].append({"name": key_1})
        cuid = uuid
        uuid = uuid + 1
        for key_2 in dict_graph[key_1].keys():
            graph["nodes"].append({"name": key_2, "category": "key_2", "id": uuid})
            graph["links"].append(
                {"source": cuid, "target": uuid, "category": key_1, "description": dict_graph[key_1][key_2]})
            uuid = uuid + 1
    graph["category"].append({"name": "key_2"})
    etime = time.time()
    return jsonify({"data": graph, "meta": {"duration": etime - stime, "amount": uuid}})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
