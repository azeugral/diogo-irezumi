# -*- coding: utf-8 -*-
"""Fotos de página inteira (desktop e celular) e quadros do hero. Uso: python tools/fotos.py [url]"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
URL = next((a for a in sys.argv[1:] if a.startswith('http')), 'http://localhost:8891/')
SAI = Path(__file__).resolve().parent.parent.parent / '_ref/fotos'; SAI.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    for nome, vp, m in [('pc', (1440, 900), False), ('cel', (390, 844), True)]:
        c = b.new_context(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=1, is_mobile=m, has_touch=m)
        g = c.new_page(); g.goto(URL)
        prev = 0
        for t in (300, 700, 1100, 1600, 2400):
            g.wait_for_timeout(t - (0 if t == 300 else prev)); prev = t
            g.screenshot(path=str(SAI / f'{nome}-hero-{t}.png'))
        g.evaluate("document.querySelectorAll('.rev').forEach(e=>e.classList.add('vis'))")
        g.wait_for_timeout(800)
        g.screenshot(path=str(SAI / f'{nome}-full.png'), full_page=True)
        c.close()
    b.close()
print('ok', SAI)
