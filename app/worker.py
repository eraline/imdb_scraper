from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from celery.schedules import crontab
from celery import Celery
from celery.signals import beat_init, worker_process_init
from . import config, db
from .models import Film, FilmScrapeEvent


settings = config.get_settings()
REDIS_URL = settings.redis_url

celery_app = Celery(__name__)
celery_app.conf.broker_url = REDIS_URL
celery_app.conf.result_backend = REDIS_URL 

def celery_on_startup(*args, **kwargs):
    print('Hello world! ')
    cluster = db.get_cluster()
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    sync_table(Film)
    sync_table(FilmScrapeEvent)

worker_process_init.connect(celery_on_startup)
beat_init.connect(celery_on_startup )

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(1, random_task.s('Hello!'), expires=10)

@celery_app.task
def random_task(name):
    print(f"Who throws a shoe? It's {name}")

@celery_app.task
def list_films():
    q = Film.objects.all().values_list('imdb_id', flat=True)
    print(list(q))