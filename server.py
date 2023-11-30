from fastapi import FastAPI 
from icecream import ic 
import requests
import redis
import json

# App initialization 
app = FastAPI() 

# Redis Client 
rds = redis.Redis(host='localhost', port=6379, db=0)

@app.get('/home')
def home():
    ic('Home route hit ..')
    return "Home" 

@app.get('/todo/{id}')
def get_todo(id: int):    
    print('Hit in Todo API')
    
    CACHE_EXP = 30*60 # 30 mins cache exp 
    
    try:
        cache = rds.get(f'todo:{id}')
        
        if cache:
            ic('Cache hit ..')
            return json.loads(cache)
        
        else:
            ic('Cache miss ..')
            r = requests.get(f"https://jsonplaceholder.typicode.com/todos/{id}")
            rds.setex(f'todo:{id}', CACHE_EXP, r.text)
            return r.json()
            
    except Exception as err:
        ic(f'An error occured: {err}')
        return err