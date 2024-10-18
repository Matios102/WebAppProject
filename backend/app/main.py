from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, get_db
from app.routers import expenses_router, auth_router, user_router, team_router, category_router
from app.utils.init import user_dump, initial_users, category_dump, team_dump

app = FastAPI()
if engine is not None:
    Base.metadata.create_all(bind=engine)

db = next(get_db())
category_dump(db)
initial_users(db)
user_dump(db)
team_dump(db)


origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


app.include_router(expenses_router.router, prefix="/api", tags=["expenses"])
app.include_router(auth_router.router, tags=["auth"])
app.include_router(user_router.router, prefix="/api", tags=["users"])
app.include_router(team_router.router, prefix="/api", tags=["team"])
app.include_router(category_router.router, prefix="/api", tags=["categories"])
