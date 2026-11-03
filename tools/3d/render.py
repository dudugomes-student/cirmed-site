#!/usr/bin/env python3
"""Renderiza as ilustrações 3D (tools/3d/scenes.js) e salva em assets/3d/*.webp.

Uso: python3 tools/3d/render.py /caminho/para/three   (pasta "package" do pacote npm three@0.170.0)
Precisa de Playwright e de um Chrome com WebGL (SwiftShader serve).
"""
import sys, json, base64, io, pathlib, shutil, http.server, threading, functools, tempfile
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
THREE = pathlib.Path(sys.argv[1])
BR = json.loads((ROOT / "tools" / "brasil.json").read_text())

# projeção usada em tools/brasil.cjs (lon/lat -> pixels do contorno)
def proj(lon, lat):
    return [10.205 * lon + 755.36, -10.49 * lat + 55.9]

CITIES = [(-49.07, -22.33), (-37.77, -4.56), (-46.32, -23.40), (-50.23, -30.25), (-51.23, -30.03), (-46.17, -19.70),
          (-56.13, -15.65), (-55.71, -12.55), (-54.81, -22.22), (-43.94, -19.92), (-50.55, -20.27), (-54.64, -16.47),
          (-40.31, -20.13), (-51.10, -21.13), (-47.27, -22.82), (-48.69, -23.92), (-49.22, -20.79)]
CTX = {"BR": BR, "pins": [proj(*c) for c in CITIES]}

# nome, largura, altura do quadro, largura final
JOBS = [("hero", 1400, 1100, 1100), ("mapPins", 1400, 1100, 1000), ("stethoscope", 1200, 900, 760),
        ("calendar", 1000, 800, 520), ("hospital", 1000, 800, 520), ("ubs", 1000, 800, 520), ("upa", 1000, 800, 520),
        ("ambulance", 1000, 800, 520), ("shield", 900, 900, 420)]
only = set(sys.argv[2:])

serve = pathlib.Path(tempfile.mkdtemp())
shutil.copytree(THREE / "build", serve / "three" / "build")
shutil.copytree(THREE / "examples" / "jsm", serve / "three" / "jsm")
shutil.copy(pathlib.Path(__file__).parent / "scenes.js", serve / "scenes.js")
(serve / "index.html").write_text('''<!doctype html><html><head><meta charset="utf-8">
<script type="importmap">{"imports":{"three":"./three/build/three.module.js","three/addons/":"./three/jsm/"}}</script>
<script type="module">import { render } from './scenes.js'; window.renderScene = render; window.ready = true;</script>
</head><body style="margin:0;background:transparent"></body></html>''')

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 4190), functools.partial(Q, directory=str(serve)))
threading.Thread(target=srv.serve_forever, daemon=True).start()

out = ROOT / "assets" / "3d"; out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome",
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    for name, w, h, final in JOBS:
        if only and name not in only: continue
        pg = b.new_page()
        errs = []; pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.goto("http://127.0.0.1:4190/index.html"); pg.wait_for_function("window.ready === true")
        data = pg.evaluate("([n, c, w, h]) => window.renderScene(n, c, {width: w, height: h})", [name, CTX, w, h])
        if errs: print(name, "ERROS:", errs[:3])
        im = Image.open(io.BytesIO(base64.b64decode(data.split(",")[1]))).convert("RGBA")
        bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bbox:
            pad = 16; im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
        im = im.resize((final, round(im.height * final / im.width)), Image.LANCZOS)
        im.save(out / f"{name}.webp", quality=88, method=6)
        print(name, im.size)
        pg.close()
    b.close()
