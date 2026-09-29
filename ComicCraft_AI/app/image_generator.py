import base64, io, re, uuid
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from app.config import HF_API_KEY, HF_IMAGE_MODEL, USE_AI, USE_LOCAL_DIFFUSION, PANELS_DIR

def _filename(panel):
    return f"panel_{panel}_{uuid.uuid4().hex[:10]}.png"

def _placeholder(prompt, panel):
    img=Image.new("RGB",(1024,768),"white")
    draw=ImageDraw.Draw(img)
    draw.rectangle((20,20,1004,748), outline="black", width=6)
    title=f"COMICCRAFT • PANEL {panel}"
    draw.text((50,55),title,fill="black")
    # Keep the placeholder deterministic and dependency-light.
    words=re.findall(r"\w+", prompt)[:22]
    text=" ".join(words)
    draw.text((50,140),text[:90],fill="black")
    draw.text((50,190),text[90:180],fill="black")
    path=PANELS_DIR/_filename(panel); img.save(path); return path

def _hf_image(prompt, panel):
    import requests
    url=f"https://router.huggingface.co/hf-inference/models/{HF_IMAGE_MODEL}"
    r=requests.post(url, headers={"Authorization":f"Bearer {HF_API_KEY}"}, json={"inputs":prompt}, timeout=180)
    r.raise_for_status()
    img=Image.open(io.BytesIO(r.content)).convert("RGB")
    path=PANELS_DIR/_filename(panel); img.save(path); return path

def _local_image(prompt, panel):
    from diffusers import AutoPipelineForText2Image
    import torch
    device="cuda" if torch.cuda.is_available() else "cpu"
    pipe=AutoPipelineForText2Image.from_pretrained(HF_IMAGE_MODEL)
    pipe=pipe.to(device)
    img=pipe(prompt, num_inference_steps=20).images[0]
    path=PANELS_DIR/_filename(panel); img.save(path); return path

def generate_image(prompt, panel=1):
    if USE_AI and HF_API_KEY:
        try: return _hf_image(prompt,panel)
        except Exception: pass
    if USE_AI and USE_LOCAL_DIFFUSION:
        try: return _local_image(prompt,panel)
        except Exception: pass
    return _placeholder(prompt,panel)
