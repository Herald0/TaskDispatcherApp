import random
import uvicorn

from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.tasks import task_router
from app.api.endpoints.users import user_router
from app.api.endpoints.websocket import ws_router
from app.core.security import get_user_from_token


app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)
app.include_router(ws_router)

templates = Jinja2Templates(directory='app/templates')
app.mount('/static', StaticFiles(directory='app/static'), 'static')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.get('/join_table', response_class=HTMLResponse)
async def join_table(request: Request, username: str = Depends(get_user_from_token)):
    return templates.TemplateResponse('index.html', {
        'request': request,
        'username': username
    })

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000)
    