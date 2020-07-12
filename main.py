from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.db import connect_to_mongo, close_mongo_connection
from app.users.routes import router as users_router
from app.words.routes import router as words_router


app = FastAPI()


app.include_router(users_router, prefix='/api/users', tags=['users'])
app.include_router(words_router, prefix='/api/words', tags=['words'])

app.add_event_handler('startup', connect_to_mongo)
app.add_event_handler('shutdown', close_mongo_connection)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({'detail': [{'field': i['loc'][-1], 'msg': i['msg']} for i in exc.errors()]}))


@app.get('/')
async def root():
    return {'hello': 'friend'}
