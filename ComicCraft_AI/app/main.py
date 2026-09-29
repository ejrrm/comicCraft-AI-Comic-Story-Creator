from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="ComicCraft AI", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft AI"}
