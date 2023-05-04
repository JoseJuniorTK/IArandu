from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse, FileResponse, UJSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import json
from fastapi.middleware.cors import CORSMiddleware
import core
import numpy as np
import cv2
from io import BytesIO

# https://stackoverflow.com/questions/70069619/refresh-data-on-button-click-react

app = FastAPI()
app.mount("/static", StaticFiles(directory="./api/static"), name="static")

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


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse('./api/static/freebie.html')


@app.get("/scanner", response_class=HTMLResponse)
async def index():
    return FileResponse('./api/static/scanner.html')


@app.get("/antigo", response_class=HTMLResponse)
async def index():
    return FileResponse('./api/static/index.html')


@app.post("/file")
async def atualizadados(file: UploadFile):
    # Dados entram em forma de bytes
    data = await file.read()
    # Converte os bytes recebidos para um array numpy
    img_array = np.frombuffer(data, np.uint8)
    # Decodifica a imagem
    img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
    # Processamento
    saida = core.scanner(img)
    print("Acabou o processamento")
    # Saida da imagem para download
    _, encoded_image = cv2.imencode('.jpg', saida)
    print("Chegou ate aqui")
    # Cria um objeto de resposta com a imagem codificada
    return StreamingResponse(BytesIO(encoded_image.tobytes()), media_type="image/png")
