from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO
import sys
from pathlib import Path
import csv
import time

from fastai import *
from fastai.text import *

model_file_url = 'https://drive.google.com/uc?export=download&id=1m09MYFgZ7_FGMbMNMCEoPfK332stCSlv'
model_file_name = 'poetmodel'
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, path/'models'/f'{model_file_name}.pth')
    data_lm = TextLMDataBunch.load(path/'static', 'data_lm')
    data_bunch = (TextList.from_csv(path, csv_name='static/blank.csv', vocab=data_lm.vocab)
        .random_split_by_pct()
        .label_for_lm()
        .databunch(bs=10))
    learn = language_model_learner(data_bunch, pretrained_model=None)
    learn.load(model_file_name)
    return learn

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()

    return JSONResponse({'result': textResponse(data)})

def textResponse(data):
    csv_string = learn.predict(data['file'], 40, temperature=1.1, min_p=0.001)
    time.sleep(2)

    words = csv_string.split()
    for i, word in enumerate(words):
        if word == 'xxbos':
            words[i] = '<br/>'
        elif word == 'xxmaj':
            words[i+1] = words[i+1][0].upper() + words[i+1][1:]
            words[i] = ''
        elif word == 'xxup':
            words[i+1] = words[i+1].upper()
            words[i] = ''     
        elif word == 'xxunk' or word == '(' or word == ')' or word == '"':
            words[i] = ''   
        elif word == ',':
            words[i] = ''
        elif word == '.' or word == '?' or word == '!' or word == ';':
            words[i-1]+= words[i]
            words[i] = ''
        elif word[0] == "'":
            words[i-1]+= words[i]
            words[i] = ''

    return ' '.join(words)

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app, host='0.0.0.0', port=5042)

