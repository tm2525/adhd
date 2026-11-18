import json, pathlib, re
p = pathlib.Path(__file__).parent
data = json.loads((p / "content.json").read_text())
source_ids = {s["id"] for s in data["sources"]}
assert len(source_ids) == len(data["sources"]), "Duplicate source IDs"
module_ids = {m["id"] for m in data["modules"]}
assert len(module_ids) == len(data["modules"]), "Duplicate module IDs"
for group in ("modules", "questions", "vivas"):
    for item in data[group]:
        assert set(item["sources"]) <= source_ids, "Unknown citation"
for q in data["questions"]:
    assert q["module"] in module_ids
    assert 0 <= q["answer"] < len(q["options"])
html = (p / "index.html").read_text()
start = html.index("const APP_DATA=") + len("const APP_DATA=")
end = html.index(";\n", start)
encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
(p / "index.html").write_text(html[:start] + encoded + html[end:])
print("Embedded validated content into index.html")
