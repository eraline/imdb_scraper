from typing import List
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from . import config, db, schema, crud
from . models import Film, FilmScrapeEvent

settings = config.get_settings()
app = FastAPI()

session = None

@app.on_event('startup')
def on_startup():
    global session
    session = db.get_session()
    sync_table(Film)
    sync_table(FilmScrapeEvent)

@app.get('/')
def read_index():
    return {'hello': 'world', 'name':settings.name}

@app.get('/films', response_model=List[schema.FilmListSchema])
def films_list_view():
    return list(Film.objects.all())

@app.post('/events/scrape')
def events_scrape_create_view(data:schema.FilmListSchema ):
    film, scrape_obj = crud.add_scrape_event(data.dict())
    return film

@app.get('/films/{imdb_id}')
def films_detail_view(imdb_id):
    data = dict(Film.objects.get(imdb_id=imdb_id))
    events = list(FilmScrapeEvent.objects.filter(imdb_id=imdb_id).limit(5))
    events = [schema.FilmScrapeEventDetailSchema(**x) for x in events]
    data['events'] = events
    data['events_url'] = f'/films/{imdb_id}/events'
    return data 

@app.get('/films/{imdb_id}/events',
        response_model=List[schema.FilmScrapeEventDetailSchema])
def films_scrapes_list_view(imdb_id):
    return list(FilmScrapeEvent.objects.filter(imdb_id=imdb_id))