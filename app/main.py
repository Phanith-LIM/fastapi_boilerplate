from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware

from app.core.middleware.current_user import CurrentUserMiddleware
from app.module.users.controller import router as user_router
from app.module.books.controller import router as book_router
from app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    try:
        Base.metadata.create_all(bind=engine)
        yield
    finally:
        print("Shutting down")


app = FastAPI(
    docs_url='/',
    title="FastAPI",
    description="This is my API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CurrentUserMiddleware)
app.include_router(user_router)
app.include_router(book_router)

