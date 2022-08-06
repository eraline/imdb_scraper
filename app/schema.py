from uuid import UUID
from typing import Optional, Any
from pydantic import BaseModel, root_validator
from . import utils

class FilmSchema(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str]

class FilmListSchema(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str]

class FilmScrapeEventSchema(BaseModel):
    uuid: UUID
    imdb_id: str
    title: str
    year: Optional[str]

class FilmScrapeEventDetailSchema(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str]
    created: Optional[Any] = None 
    
    @root_validator(pre=True)
    def extra_create_time_from_uuid(cls, values):
        values['created'] = utils.uuid1_time_to_datetime(values['uuid'].time).timestamp()
        return values 