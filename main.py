import random
import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.tasks import task_router
from app.api.endpoints.users import user_router
from app.api.endpoints.websocket import ws_router


app = FastAPI()
app.include_router(task_router)
app.include_router(user_router)
app.include_router(ws_router)

templates = Jinja2Templates(directory='app/templates')
app.mount('/static', StaticFiles(directory='app/static'), 'static')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.post('/join_table', response_class=HTMLResponse)
async def join_table(request: Request, username: str = Form(...)):
    user_id = random.randint(100, 10000)
    return templates.TemplateResponse('index.html', {
        'request': request,
        'username': username,
        'user_id': user_id
    })

if __name__ == '__main__':
    uvicorn.run(app="main:app", port=8000)
    