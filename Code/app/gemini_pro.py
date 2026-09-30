import json
from app.config import GEMINI_API_KEY, GEMINI_STORY_MODEL, USE_AI

def _fallback(outline, req):
    name=req["character_name"]; tone=req["tone"]
    parts=[]
    for p in outline:
        parts.append({
          "panel":p["panel"], "caption":f"{p['title']} — {tone.title()} moment.",
          "narration":f"{name} faces the moment described in this panel. {p['scene_description']} "
        })
    return parts

def generate_story(outline, req):
    if not (USE_AI and GEMINI_API_KEY):
        return _fallback(outline, req)
    try:
        from google import genai
        client=genai.Client(api_key=GEMINI_API_KEY)
        instruction=f"""Expand this five-panel comic outline into exactly five JSON objects.
Character: {req['character_name']}; tone: {req['tone']}.
Return ONLY JSON array. Each object: panel, caption, narration.
Outline:
{json.dumps(outline, ensure_ascii=False)}"""
        response=client.models.generate_content(model=GEMINI_STORY_MODEL, contents=instruction)
        text=response.text.strip()
        if text.startswith("```"):
            text=text.split("\n",1)[1].rsplit("```",1)[0]
        data=json.loads(text)
        if not isinstance(data,list) or len(data)!=5: raise ValueError
        return data
    except Exception:
        return _fallback(outline, req)
