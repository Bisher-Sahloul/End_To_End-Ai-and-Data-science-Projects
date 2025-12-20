from fastapi import FastAPI , Path , HTTPException , Query 
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import sys 
import os 
import json 
import util
from typing import Annotated   
from pydantic import BaseModel , Field

class House(BaseModel) : 
    total_sqft: Annotated[float , Field(... , gt = 0 , description='The area of the house')]
    balcony: Annotated[int , Field(... , description='The number of balcony')]
    bedroom: Annotated[int , Field(... , description="The number of Bedroom")]
    bath:Annotated[int , Field(... , description = "The number of bathroom")]
    location:Annotated[str , Field(... , description="The House's location")]

app = FastAPI()

def load_data():
    util.load_save_artifacts()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get('/get_location_names')
def get_location_names():
    load_data()
    return {
        'message' : util.get_location_names()
    }

@app.post('/predict_home_price')
async def predict_home_price(request: Request):
    load_data()
    payload = House(**await request.json())
    try:
        total_sqft = payload.total_sqft
        balcony = payload.balcony
        bedroom = payload.bedroom
        bath = payload.bath
        location = payload.location
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {e}")
    print(f"Here {payload}")
    return JSONResponse(
        content={
            'estimated_price': util.get_estimated_price(location, total_sqft, bath, balcony, bedroom)
        }
    )