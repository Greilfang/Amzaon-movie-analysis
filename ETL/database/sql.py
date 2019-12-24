import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, ForeignKey, func, String, Text, Float, Integer, MetaData
import sqlalchemy.orm
import json

Base = declarative_base()


class MovieBasics(Base):
    __tablename__ = 'movie_basics'
    ID = Column(String(length=40), primary_key=True, nullable=False)
    Title = Column(String(length=500), nullable=False)
    Intro = Column(Text, nullable=True)
    Imdb = Column(Float, nullable=True)
    Score = Column(Float, nullable=True)
    Year = Column(Integer, nullable=True, default=-1, index=True)
    Emotion = Column(Float, nullable=True)

    def __repr__(self):
        return '<MovieBasics %r>' % self.ID

    def to_json(self):
        result = {
            'ID': self.ID,
            'Title': self.Title,
            'Score': self.Score,
            'Year': self.Year
        }
        return result


class MovieGenres(Base):
    __tablename__ = 'movie_genres'
    ID = Column(String(length=40), primary_key=True, nullable=False)
    Genre = Column(String(length=40), primary_key=True, nullable=False)


class SQLMovieHandler:
    @staticmethod
    def conn():
        pass

    @staticmethod
    def get_dict(results):
        result_list = []
        for result in results:
            result_list.append(result.to_json())
        return result_list

    def __init__(self):
        self.engine = create_engine("mysql+pymysql://root:little_hug1020@localhost:3306/amazon_movies",
                                    encoding="utf-8",
                                    echo=True)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)

    def insert_all_movie_basics(self, path):
        session = self.session()
        movie_list = os.listdir(path)
        count = 0
        for movie in movie_list:
            # print(movie)
            with open(path + '\\{}'.format(movie)) as f:
                data = json.load(f)
                if 'Imdb' not in data:
                    data['Imdb'] = None
                if 'Emotion' not in data:
                    data['Emotion'] = None
                movie_basic = MovieBasics(
                    ID=data['ID'],
                    Title=data['Title'],
                    Intro=data['Intro'],
                    Imdb=data['Imdb'],
                    Score=data['Score'],
                    Year=data['Year'],
                    Emotion=data['Emotion']
                )
                session.add(movie_basic)
                count = count + 1
                if count % 1000 == 0:
                    print('{} inserted'.format(count))
        session.commit()

    def insert_all_movie_genres(self, path):
        session = self.session()
        movie_list = os.listdir(path)
        count = 0
        for movie in movie_list:
            with open(path + '\\{}'.format(movie)) as f:
                data = json.load(f)
                if 'Genre' not in data: continue
                for genre in data['Genre']:
                    movie_genre = MovieGenres(
                        ID=data['ID'],
                        Genre=genre
                    )
                    session.add(movie_genre)
                    count = count + 1
                    if count % 1000 == 0:
                        print('{} Genres inserted'.format(count))
        session.commit()
