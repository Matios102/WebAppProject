from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import expenses_router, auth_router, user_router, team_router, category_router

app = FastAPI()
if engine is not None:
    Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",  
    
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
