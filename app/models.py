from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

data = {
    'imdb_id':'tt123456',
    'title':'Interstellar',
    'year':'2014'
}

class Film(Model):
    __keyspace__ = 'imdb_scraper_app'
    imdb_id = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    year = columns.Integer()

class FilmScrapeEvent(Model):
    __keyspace__ = 'imdb_scraper_app'
    uuid = columns.UUID(primary_key=True)
    imdb_id = columns.Text(index=True)
    title = columns.Text()
    year = columns.Integer()