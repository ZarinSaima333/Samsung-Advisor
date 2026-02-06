# main.py
from fastapi import FastAPI
from routes import router  # import the router from routes.py

app = FastAPI(title="Samsung Phone Advisor")

# Include all endpoints from routes.py
app.include_router(router)



