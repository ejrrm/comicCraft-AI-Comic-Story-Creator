def build_comic_layout(outline, story, image_paths):
    story_by_panel={int(x["panel"]):x for x in story}
    layout=[]
    for p, path in zip(outline,image_paths):
        s=story_by_panel.get(int(p["panel"]),{})
        layout.append({
          "panel":p["panel"], "title":p["title"],
          "image_url":"/static/panels/"+path.name,
          "image_path":str(path),
          "scene_description":p["scene_description"],
          "image_prompt":p["image_prompt"],
          "caption":s.get("caption",""),
          "narration":s.get("narration","")
        })
    return layout
