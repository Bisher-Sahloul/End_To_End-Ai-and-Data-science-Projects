
import json 
import pickle
import numpy as np 
__locations = None
__data_columns = None
__model = None

def get_estimated_price(location , total_sqft , bath , balcony , bedroom):
    try :
        loc_ind = __data_columns.index(location.lower())
    except :
        loc_ind = -1
    
    x = np.zeros(len(__data_columns))

    x[0] = total_sqft
    x[1] = bath
    x[2] = balcony
    x[3] = bedroom 
    
    if loc_ind >= 0 :
        x[loc_ind] = 1
    
    return round(__model.predict([x])[0] , 2)


def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

def load_save_artifacts():
    global  __data_columns
    global __locations
    global __model

    print("Loading saved artifacts...start")
    with open('./artifacts/columns.json' , "r") as f :
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[4:]

    with open('./artifacts/banglore_home_prices_model.pickle' , 'rb') as f :
        __model = pickle.load(f)

    print('Loading save artifacts is done')
    
