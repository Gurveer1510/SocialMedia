from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from beanie import init_beanie
from app.models.user_model import Users
from app.models.posts_model import Post
from app.models.likes_model import Likes
from app.api.api_v1.router import router
from fastapi.staticfiles import StaticFiles
from app.core.config import settings


app = FastAPI(title='SocialMedia service')


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def greet_user():
    return {
        "message" : "Hello Users!"
    }
app.mount("/app/static", app = StaticFiles(directory="app/static"), name="static")
app.mount("/app/posts", app = StaticFiles(directory="app/posts"), name="posts")

app.include_router(router=router)

# Initialize Beanie when the FastAPI app starts up
@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(settings.mongo_connection_url)
    await init_beanie(database=client.my_db, document_models=[Users, Post, Likes])
    print("connected")








