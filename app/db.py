import os
import pathlib

from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import (register_connection,
    set_default_connection)

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = os.path.join(BASE_DIR, 'ignored/connect.zip')
ASTRA_DB_CLIENT_ID = os.getenv('ASTRA_DB_CLIENT_ID')
ASTRA_DB_CLIENT_SECRET = os.getenv('ASTRA_DB_CLIENT_SECRET')


def get_cluster():    
    cloud_config= {
            'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster

def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session

# session = get_session()
# row = session.execute("select release_version from system.local").one()
# 
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")
#     return session

