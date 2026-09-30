import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_STORY_MODEL = os.getenv("GEMINI_STORY_MODEL", "gemini-2.5-flash")
HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-3-medium-diffusers")
USE_AI = os.getenv("USE_AI", "true").lower() == "true"
USE_LOCAL_DIFFUSION = os.getenv("USE_LOCAL_DIFFUSION", "false").lower() == "true"

PANELS_DIR = BASE_DIR / "static" / "panels"
EXPORTS_DIR = BASE_DIR / "static" / "exports"
PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
