from fastapi import FastAPI, BackgroundTasks
from raydium import new_pool_alert
from dexlab import new_market_alert


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ray")
async def raydium(background_tasks: BackgroundTasks):
    background_tasks.add_task(new_pool_alert)
    return {"status": "run successfully"}


@app.get("/dex")
async def dexlab(background_tasks: BackgroundTasks):
    background_tasks.add_task(new_market_alert)
    return {"status": "run successfully"}
