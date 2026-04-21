from fastapi import APIRouter

from app.api.routes import utils, users, login, books, library, community


api_router = APIRouter()
api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(library.router, prefix="/library", tags=["library"])
api_router.include_router(community.router, prefix="/communities", tags=["communities"])
