# ComicCraft AI

A FastAPI + Jinja2 web application based on the supplied ComicCraft project documentation.

## Features
- Five-panel comic outline
- AI story narration and dialogue
- AI image generation through Hugging Face (optional)
- Optional local Diffusers/Stable Diffusion
- Comic preview in browser
- PDF export
- HTML form and JSON API
- `/docs` Swagger API documentation
- Safe fallback mode so the application can run without AI keys

## 1. Windows setup

Use Python 3.11 or 3.12.

```powershell
cd ComicCraft_AI
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 2. API keys
Edit `.env` and add `GEMINI_API_KEY` for real AI story generation.
Add `HF_API_KEY` if you want Hugging Face image generation.

Without keys, the project still runs using a built-in deterministic image placeholder and fallback story generation. This is useful for testing the full frontend/backend/PDF pipeline.

## 3. Run
```powershell
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs

## 4. JSON API
POST `/generate-comic/json`:
```json
{
  "story_prompt":"A brave fox exploring an enchanted forest",
  "character_name":"Finn",
  "setting":"forest",
  "tone":"dramatic",
  "art_style":"comic book"
}
```

## 5. Optional local Stable Diffusion
Install the extra requirements and set `USE_LOCAL_DIFFUSION=true`.
This requires substantial disk space/RAM/VRAM and may take a long time on CPU.

## Project structure
```text
ComicCraft_AI/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
├── static/
│   ├── css/
│   ├── panels/
│   └── exports/
├── .env.example
├── requirements.txt
└── README.md
```

## Important
The original documentation names Gemini 1.5 Flash/Pro and Stable Diffusion v1.5. AI model availability changes over time, so this implementation uses current configurable model names by default while preserving the documented workflow. The exact model can be changed in `.env`.
