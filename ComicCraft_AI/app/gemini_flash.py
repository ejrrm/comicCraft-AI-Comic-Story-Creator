import json
from app.config import GEMINI_API_KEY, GEMINI_MODEL, USE_AI

def _fallback(req):
    name=req["character_name"]; setting=req["setting"]; tone=req["tone"]; style=req["art_style"]
    prompt=req["story_prompt"]
    return [
      {"panel":1,"title":"The Beginning","scene_description":f"{name} begins the adventure in the {setting}.","image_prompt":f"{name} beginning an adventure in a {setting}, {style} comic art, {tone} mood, cinematic panel"},
      {"panel":2,"title":"A New Discovery","scene_description":f"{name} discovers something unexpected while following the idea: {prompt}.","image_prompt":f"{name} making a surprising discovery in a {setting}, {style} comic art, expressive character, detailed background"},
      {"panel":3,"title":"The Challenge","scene_description":f"A challenge appears and {name} must decide what to do next.","image_prompt":f"{name} facing a dramatic challenge in a {setting}, {style} comic art, dynamic action, strong composition"},
      {"panel":4,"title":"The Turning Point","scene_description":f"{name} finds a clever way forward and the story reaches its turning point.","image_prompt":f"{name} overcoming a challenge in a {setting}, {style} comic art, heroic moment, vivid details"},
      {"panel":5,"title":"A New Beginning","scene_description":f"{name} reaches the end of this adventure with a memorable lesson.","image_prompt":f"{name} celebrating at the end of an adventure in a {setting}, {style} comic art, warm ending, cinematic"}
    ]

def generate_outline(req):
    if not (USE_AI and GEMINI_API_KEY):
        return _fallback(req)
    try:
        from google import genai
        client=genai.Client(api_key=GEMINI_API_KEY)
        instruction=f"""Create exactly 5 comic panels. Return ONLY valid JSON array.
User story: {req['story_prompt']}
Character: {req['character_name']}
Setting: {req['setting']}
Tone: {req['tone']}
Art style: {req['art_style']}
Each item must contain integer panel, title, scene_description, image_prompt."""
        response=client.models.generate_content(model=GEMINI_MODEL, contents=instruction)
        text=response.text.strip()
        if text.startswith("```"):
            text=text.split("\n",1)[1].rsplit("```",1)[0]
        data=json.loads(text)
        if not isinstance(data,list) or len(data)!=5:
            raise ValueError("Gemini did not return exactly five panels")
        return data
    except Exception:
        return _fallback(req)
