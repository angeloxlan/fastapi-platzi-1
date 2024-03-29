# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr, HttpUrl

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI() 

# Models

class HairColor(str, Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    red = 'red'
    blonde = 'blonde'

class Person(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        )
    age: int = Field(
        ..., 
        gt=0,
        le=115,
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    email: EmailStr = Field(...)
    website: HttpUrl = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'first_name': 'Jhon',
                'last_name': 'Doe',
                'age': 25,
                'hair_color': 'black',
                'is_married': False,
                'email': 'john@doe.com',
                'website': 'https://johndoe.com'
            }
        }

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    country: str = Field(
        ...,
        min_length=1, 
        max_length=50,
        )

    class Config:
        schema_extra = {
            'example': {
                'city': 'Puebla',
                'state': 'Puebla',
                'country': 'Mexico',
            }
        }


@app.get('/')
def home():
    return { 'message': 'This project uses FastAPI.' }

# Request and Response Body
@app.post('/person/new')
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=30,
        title='Person Name',
        description='This is the person name. It\'s between 1 and 30 characters',
        example='John',
        ),
    age: str = Query(
        ...,
        title='Person Age',
        description='This is the person age. It\'s required.',
        example=25,
        )
):
    return { name: age }

# Validaciones: Path Parameters
@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title='Person id',
        description='This is the person id.',
        example=120,
        )
):
    return { person_id: 'Person id is valid' }

# Validaciones: Request Body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        title='Person ID',
        description='This is the person ID',
        gt=0,
        example=120,
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    return result
