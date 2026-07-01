from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def home(request: Request):
    # Pass the request as a keyword argument 'request'
    return templates.TemplateResponse(request=request, name='index.html')

@app.get('/{page}')
async def get_page(request: Request, page: str):
    # Pass the request as a keyword argument 'request'
    return templates.TemplateResponse(request=request, name=f'{page}.html')