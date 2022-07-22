import copy
import uuid
from cassandra.cqlengine.management import sync_table
from .db import get_session
from .models import Film, FilmScrapeEvent

session = get_session()
sync_table(Film)
sync_table(FilmScrapeEvent )

def create_entry(data:dict):
    return Film.create(**data) 


def create_scrape_entry(data:dict):
    data['uuid'] = uuid.uuid1()
    return FilmScrapeEvent.create(**data) 

def add_scrape_event(data:dict, fresh=False):
    if fresh:
        data = copy.deepcopy(data)
    film = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return film, scrape_obj