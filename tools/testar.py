# -*- coding: utf-8 -*-
"""Testa filtros, ver mais, lightbox, Quero este, formulário e menu. Uso: python tools/testar.py [url]"""
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf8')
URL = next((a for a in sys.argv[1:] if a.startswith('http')), 'http://localhost:8891/')
R = []
def ok(n, c, x=''): R.append(bool(c)); print('OK ' if c else 'FALHOU', n, x)
with sync_playwright() as p:
    b = p.chromium.launch(channel='msedge')
    c = b.new_context(viewport={'width': 1440, 'height': 900}); c.grant_permissions(['clipboard-read', 'clipboard-write'])
    g = c.new_page(); err = []
    g.on('pageerror', lambda e: err.append(str(e))); g.goto(URL); g.wait_for_timeout(2200)
    hz = g.evaluate("(()=>{const m=new DOMMatrix(getComputedStyle(document.querySelector('.kk-mask')).transform),p=new DOMMatrix(getComputedStyle(document.querySelector('.kk-pano')).transform);return [m.m42,p.m42]})()")
    ok('hero desenrolado', abs(hz[0]) < 1 and abs(hz[1]) < 1, hz)
    ok('sem clip-path animado', g.evaluate("getComputedStyle(document.querySelector('.kk-pano')).clipPath") == 'none')
    n = lambda: g.evaluate("document.querySelectorAll('#grade li').length")
    ok('grade inicial 16', n() == 16, n())
    g.click('#mais'); ok('ver mais 32', n() == 32, n())
    g.click('.filtro[data-f=corpo]'); ok('filtro costas e pernas 8', n() == 8, n())
    g.click('#grade .cartao >> nth=2'); g.wait_for_timeout(200)
    ok('lightbox abre', g.evaluate("!document.querySelector('#lb').hidden"), g.inner_text('.lb-t'))
    g.keyboard.press('ArrowRight'); t2 = g.inner_text('.lb-t'); g.keyboard.press('Escape')
    ok('lightbox passa e fecha', g.evaluate("document.querySelector('#lb').hidden"), t2)
    g.click('#disp .bt >> nth=1'); g.wait_for_timeout(1500)
    ok('quero este mostra o flash', g.inner_text('#escNome') == 'Bakeneko' and g.is_visible('#escolhido') and abs(g.evaluate("document.querySelector('#marcar').getBoundingClientRect().top")) < 200)
    g.click('#escX'); ok('tirar flash', not g.is_visible('#escolhido'))
    ok('sem formulário', g.evaluate("!document.querySelector('form')"))
    with c.expect_page() as pop:
        g.click('.bt-dm')
    ok('botão abre o Direct', 'instagram.com' in pop.value.url and 'diogo_irezumi' in pop.value.url, pop.value.url[:90]); pop.value.close()
    g.click('.q-bt >> nth=0'); ok('pintura no lightbox', 'Ryū' in g.inner_text('.lb-t')); g.keyboard.press('Escape')
    g.evaluate("scrollTo(0,0)"); g.wait_for_timeout(6500)
    ok('hero trocou de peça', g.inner_text('#kkNome') != 'Daruma tora', g.inner_text('#kkNome'))
    c.close()
    m = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); g = m.new_page(); g.goto(URL); g.wait_for_timeout(800)
    g.click('.menu-bt'); ok('menu abre', g.is_visible('#menu')); g.click('#menu a >> nth=1'); ok('menu fecha', not g.is_visible('#menu'))
    v = g.evaluate("[...document.querySelectorAll('#disp li')].filter(l=>l.offsetParent).length"); ok('disp 4 no celular', v == 4, v)
    g.click('#maisDisp'); v = g.evaluate("[...document.querySelectorAll('#disp li')].filter(l=>l.offsetParent).length"); ok('ver todos flashes', v == 12, v)
    ok('sem erros JS', not err, err)
    b.close()
print('FALHAS:', R.count(False))
