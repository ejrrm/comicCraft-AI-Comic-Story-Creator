from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.schemas import PromptRequest
from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

BASE_DIR=Path(__file__).resolve().parent.parent
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
router=APIRouter()

def make_comic(req):
    outline=generate_outline(req)
    story=generate_story(outline,req)
    images=[generate_image(p["image_prompt"],int(p["panel"])) for p in outline]
    layout=build_comic_layout(outline,story,images)
    pdf=save_pdf(layout)
    return layout,pdf

@router.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return templates.TemplateResponse(request=request,name="index.html",context={})

@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request, story_prompt:str=Form(...), character_name:str=Form(...),
                   setting:str=Form(...), tone:str=Form(...), art_style:str=Form(...)):
    try:
        req={"story_prompt":story_prompt,"character_name":character_name,"setting":setting,"tone":tone,"art_style":art_style}
        layout,pdf=make_comic(req)
        return templates.TemplateResponse(request=request,name="comic_preview.html",context={"layout":layout,"pdf_url":f"/exports/{pdf.name}"})
    except Exception as e:
        return templates.TemplateResponse(request=request,name="index.html",context={"error":f"Generation failed: {e}"},status_code=500)

@router.post("/generate-comic/json")
async def generate_json(payload:PromptRequest):
    try:
        layout,pdf=make_comic(payload.model_dump())
        return {"success":True,"layout":layout,"pdf_url":f"/exports/{pdf.name}"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get("/exports/{filename}")
async def download_export(filename:str):
    path=BASE_DIR/"static"/"exports"/Path(filename).name
    if not path.exists(): raise HTTPException(404,"PDF not found")
    return FileResponse(path,media_type="application/pdf",filename=path.name)

@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request):
    return templates.TemplateResponse(request=request,name="export_success.html",context={})

@router.get("/test-image")
async def test_image(prompt:str="a friendly fox in an enchanted forest, comic book art"):
    path=generate_image(prompt,99)
    return {"success":True,"image_url":f"/static/panels/{path.name}"}
