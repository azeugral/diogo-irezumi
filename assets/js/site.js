(function(){
'use strict';
var D=window.DADOS, doc=document, root=doc.documentElement;
root.classList.add('js');
var $=function(s,c){return (c||doc).querySelector(s)}, $$=function(s,c){return [].slice.call((c||doc).querySelectorAll(s))};
var reduz=matchMedia('(prefers-reduced-motion: reduce)').matches;
var IMG='assets/img/';

/* ---------- menu ---------- */
var menuBt=$('.menu-bt'), menu=$('#menu');
function fechaMenu(){menu.hidden=true;menuBt.setAttribute('aria-expanded','false');doc.body.style.overflow=''}
menuBt.addEventListener('click',function(){var a=menu.hidden;menu.hidden=!a;menuBt.setAttribute('aria-expanded',String(a));doc.body.style.overflow=a?'hidden':''});
$$('#menu a').forEach(function(a){a.addEventListener('click',fechaMenu)});
addEventListener('resize',function(){if(innerWidth>960&&!menu.hidden)fechaMenu()});

/* ---------- kakejiku ---------- */
var hero=$('.hero'), kake=$('#kake'), pano=$('.kk-pano',kake), jiku=$('.kk-jiku',kake), kImg=$('#kkImg'), kNome=$('#kkNome');
var obras=D.hero, idx=0, cache={};
obras.forEach(function(o){var i=new Image();i.src=IMG+'hero/'+o.c+'.webp';cache[o.c]=i});
function alturaPano(){return pano.offsetHeight}
var EASE_D='cubic-bezier(.5,.02,.18,1)', EASE_U='cubic-bezier(.6,0,.4,1)';
function desenrola(d,atraso){
  var H=alturaPano();
  var a=pano.animate([{clipPath:'inset(0 0 100% 0)'},{clipPath:'inset(0 0 0% 0)'}],{duration:d,delay:atraso||0,easing:EASE_D,fill:'both'});
  jiku.animate([{transform:'translateY('+(-H+6)+'px)'},{transform:'translateY(0)'}],{duration:d,delay:atraso||0,easing:EASE_D,fill:'both'});
  return a.finished;
}
function enrola(d){
  var H=alturaPano();
  var a=pano.animate([{clipPath:'inset(0 0 0% 0)'},{clipPath:'inset(0 0 100% 0)'}],{duration:d,easing:EASE_U,fill:'both'});
  jiku.animate([{transform:'translateY(0)'},{transform:'translateY('+(-H+6)+'px)'}],{duration:d,easing:EASE_U,fill:'both'});
  return a.finished;
}
function balanca(){
  if(reduz)return;
  kake.animate([{transform:'rotate(0)'},{transform:'rotate(.55deg)'},{transform:'rotate(-.35deg)'},{transform:'rotate(.18deg)'},{transform:'rotate(-.06deg)'},{transform:'rotate(0)'}],{duration:1900,easing:'ease-out'});
}
function espera(ms){return new Promise(function(r){setTimeout(r,ms)})}
function troca(){
  idx=(idx+1)%obras.length; var o=obras[idx], im=cache[o.c];
  var pronto=im.decode?im.decode().catch(function(){}):Promise.resolve();
  return pronto.then(function(){kImg.src=im.src;kImg.alt='Flash '+o.t;kNome.textContent=o.t});
}
var visivel=true;
if('IntersectionObserver' in window){new IntersectionObserver(function(e){visivel=e[0].isIntersecting},{threshold:.05}).observe(kake)}
function ciclo(){
  return espera(3300).then(function(){
    if(!visivel||doc.hidden){return espera(600).then(ciclo)}
    kNome.style.opacity=0;
    return enrola(620).then(function(){return troca()}).then(function(){return espera(120)}).then(function(){
      kNome.style.opacity=1; balanca(); return desenrola(1000);
    }).then(ciclo);
  });
}
function iniciaHero(){
  hero.classList.add('in');
  if(reduz||!pano.animate){return}
  desenrola(1000,180).then(ciclo);
  setTimeout(balanca,180);
}
if(pano.animate&&!reduz){pano.style.clipPath='inset(0 0 100% 0)';jiku.style.transform='translateY('+(-alturaPano()+6)+'px)'}
var p0=kImg.decode?kImg.decode().catch(function(){}):Promise.resolve();
Promise.race([p0,espera(1200)]).then(iniciaHero);

/* ---------- portfólio ---------- */
var grade=$('#grade'), maisBt=$('#mais'), filtro='todos', aberto=false;
var LIM=16;
function itensFiltro(){return D.port.filter(function(p){return filtro==='todos'||p.cat===filtro})}
function montaGrade(){
  var its=itensFiltro(), mostra=(filtro==='todos'&&!aberto)?its.slice(0,LIM):its;
  grade.innerHTML=mostra.map(function(p,i){return '<li><button class="cartao" type="button" data-lb="port" data-i="'+i+'"><span class="im"><img src="'+IMG+'p/'+p.c+'.webp" alt="'+p.t+'" width="720" height="900"></span><span class="t">'+p.t+'</span></button></li>'}).join('');
  maisBt.parentNode.hidden=!(filtro==='todos'&&!aberto&&its.length>LIM);
}
$$('.filtro').forEach(function(b){b.addEventListener('click',function(){
  $$('.filtro').forEach(function(x){x.classList.toggle('on',x===b);x.setAttribute('aria-pressed',String(x===b))});
  filtro=b.dataset.f; montaGrade();
})});
maisBt.addEventListener('click',function(){aberto=true;montaGrade()});
montaGrade();
/* carrega tudo na abertura: imagens escondidas do "ver mais" já entram em cache */
D.port.forEach(function(p){var i=new Image();i.src=IMG+'p/'+p.c+'.webp'});

/* ---------- disponíveis ---------- */
var dispEl=$('#disp'), projEl=$('#proj');
dispEl.innerHTML=D.disp.map(function(f,i){return '<li class="flash rev"><button class="ver" type="button" data-lb="disp" data-i="'+i+'" aria-label="Ver '+f.t+' em grande"><img src="'+IMG+'disp/'+f.c+'.webp" alt="Flash '+f.t+'" width="720" height="960"></button><h3>'+f.t+'</h3><a class="bt bt-tinta" href="#marcar" data-quero="'+f.c+'" data-nome="'+f.t+'" data-tipo="Flash disponível">Quero este</a></li>'}).join('');
projEl.innerHTML=D.proj.map(function(f,i){return '<li class="flash rev"><button class="ver" type="button" data-lb="proj" data-i="'+i+'" aria-label="Ver '+f.t+' em grande"><img src="'+IMG+'disp/'+f.c+'.webp" alt="Projeto '+f.t+'" width="720" height="960"></button><h3>'+f.t+'</h3><p class="z">'+f.z+'</p><a class="bt bt-tinta" href="#marcar" data-quero="'+f.c+'" data-nome="'+f.t+'" data-tipo="Projeto à medida">Quero este</a></li>'}).join('');
dispEl.classList.add('fechado');
$('#maisDisp').addEventListener('click',function(){dispEl.classList.remove('fechado');this.parentNode.hidden=true});

/* ---------- pokédex ---------- */
var pk=$('#poke');
pk.innerHTML=D.poke.map(function(p){return '<li class="pk rev"><span class="im"><img src="'+IMG+'poke/'+p.c+'.webp" alt="Tatuagem de '+p.t+'" width="600" height="600"></span><span class="n">#'+p.n+'</span><b>'+p.t+'</b></li>'}).join('')+
  '<li class="pk pk-vazio rev"><a class="im" href="#marcar" data-tipo="Pokédex" aria-label="Pedir o próximo Pokémon"><span>?</span></a><span class="n">#???</span><b>O próximo</b></li>';
pk.classList.add('fechado');
$('#pokeN').textContent=D.poke.length;
$('#maisPoke').addEventListener('click',function(){pk.classList.remove('fechado');this.parentNode.hidden=true});

/* ---------- lightbox ---------- */
var LB={
  port:function(){return itensFiltro().map(function(p){return {s:IMG+'full/'+p.c+'.webp',t:p.t}})},
  disp:function(){return D.disp.map(function(f){return {s:IMG+'full/'+f.c+'.webp',t:f.t,q:f,tipo:'Flash disponível'}})},
  proj:function(){return D.proj.map(function(f){return {s:IMG+'full/'+f.c+'.webp',t:f.t+' · '+f.z,q:f,tipo:'Projeto à medida'}})},
  pint:function(){return [{s:IMG+'pint/037_1.webp',t:'Ryū · pintura em 70 × 100 cm'},{s:IMG+'pint/008_0.webp',t:'Kintarō e koi · prints disponíveis'}]}
};
var lb=$('#lb'), lbImg=$('img',lb), lbT=$('.lb-t',lb), lbQ=$('.lb-q',lb), lista=[], li=0, foco=null;
function mostra(){var it=lista[li];lbImg.src=it.s;lbImg.alt=it.t;lbT.textContent=it.t;
  if(it.q){lbQ.hidden=false;lbQ.dataset.quero=it.q.c;lbQ.dataset.nome=it.q.t;lbQ.dataset.tipo=it.tipo}else{lbQ.hidden=true}}
function abre(tipo,i){lista=LB[tipo]();li=i;foco=doc.activeElement;mostra();lb.hidden=false;doc.body.style.overflow='hidden';$('.lb-x',lb).focus()}
function fecha(){lb.hidden=true;doc.body.style.overflow='';if(foco)foco.focus()}
function passa(n){li=(li+n+lista.length)%lista.length;mostra()}
doc.addEventListener('click',function(e){var b=e.target.closest('[data-lb]');if(b){abre(b.dataset.lb,+b.dataset.i)}});
$('.lb-x',lb).addEventListener('click',fecha);
$('.lb-a',lb).addEventListener('click',function(){passa(-1)});
$('.lb-p',lb).addEventListener('click',function(){passa(1)});
lb.addEventListener('click',function(e){if(e.target===lb)fecha()});
doc.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')fecha();if(e.key==='ArrowLeft')passa(-1);if(e.key==='ArrowRight')passa(1)});
var tx=null;lbImg.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});
lbImg.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>50)passa(dx<0?1:-1);tx=null});
lbQ.addEventListener('click',function(){fecha()});

/* ---------- formulário ---------- */
var form=$('#form'), escW=$('#fEscolhaW'), esc=$('#fEscolha'), escImg=$('#fEscolhaImg'), erro=$('#fErro'), nota=$('#fNota'), escolha=null;
function chips(id,multi){var g=$(id);$$('button',g).forEach(function(b){b.addEventListener('click',function(){
  var on=b.getAttribute('aria-pressed')!=='true';if(!multi)$$('button',g).forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed',String(on))})})}
chips('#fTipo');chips('#fAcab');
function valChip(id){var b=$(id+' [aria-pressed=true]');return b?b.textContent:''}
function marcaTipo(t){$$('#fTipo button').forEach(function(b){b.setAttribute('aria-pressed',String(b.textContent===t))})}
doc.addEventListener('click',function(e){var a=e.target.closest('[data-quero],[data-tipo]');if(!a||a.closest('#fTipo'))return;
  if(a.dataset.tipo)marcaTipo(a.dataset.tipo);
  if(a.dataset.quero){escolha=a.dataset.nome;esc.textContent=a.dataset.nome;escImg.src=IMG+'disp/'+a.dataset.quero+'.webp';escImg.alt=a.dataset.nome;escW.hidden=false}
});
$('#fEscolhaX').addEventListener('click',function(){escolha=null;escW.hidden=true});
function mensagem(){
  var v=function(id){return $(id).value.trim()}, l=['Olá Diogo! Sou '+(v('#fNome')||'—')+'.'];
  var tipo=valChip('#fTipo'); if(tipo)l.push('Procuro: '+tipo);
  if(escolha)l.push('Desenho: '+escolha);
  if(v('#fZona'))l.push('Zona do corpo: '+v('#fZona'));
  if(v('#fTam'))l.push('Tamanho: '+v('#fTam'));
  var ac=valChip('#fAcab'); if(ac)l.push('Acabamento: '+ac);
  if(v('#fPrim'))l.push('Primeira tatuagem: '+v('#fPrim'));
  if(v('#fIdeia'))l.push('','Ideia: '+v('#fIdeia'));
  return l.join('\n');
}
function valida(){
  if(!$('#fNome').value.trim()){erro.textContent='Escreve o teu nome.';erro.hidden=false;$('#fNome').focus();return false}
  if(!$('#fIdeia').value.trim()&&!escolha){erro.textContent='Conta a tua ideia ou escolhe um flash disponível.';erro.hidden=false;$('#fIdeia').focus();return false}
  erro.hidden=true;return true;
}
function copia(t){
  if(navigator.clipboard&&window.isSecureContext)return navigator.clipboard.writeText(t).then(function(){return true},function(){return falso(t)});
  return Promise.resolve(falso(t));
}
function falso(t){var ta=doc.createElement('textarea');ta.value=t;ta.setAttribute('readonly','');ta.style.position='fixed';ta.style.opacity='0';doc.body.appendChild(ta);ta.select();var ok=false;try{ok=doc.execCommand('copy')}catch(e){}ta.remove();return ok}
form.addEventListener('submit',function(e){e.preventDefault();if(!valida())return;
  var w=window.open('about:blank','_blank');
  copia(mensagem()).then(function(ok){
    nota.textContent=ok?'Mensagem copiada. No Direct, cola e envia.':'Não deu para copiar sozinho. Copia o texto do pedido à mão.';
    if(w){w.location.href='https://ig.me/m/diogo_irezumi'}else{location.href='https://ig.me/m/diogo_irezumi'}
  });
});
$('#fCopiar').addEventListener('click',function(){if(!valida())return;copia(mensagem()).then(function(ok){nota.textContent=ok?'Mensagem copiada. Agora é só colar no Direct do @diogo_irezumi.':'Não deu para copiar sozinho. Tenta outra vez.'})});

/* ---------- entradas ao rolar ---------- */
var barra=$('#pokeBarra');
if('IntersectionObserver' in window&&!reduz){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  $$('.rev').forEach(function(el){io.observe(el)});
  new IntersectionObserver(function(es,o){if(es[0].isIntersecting){barra.style.width=(D.poke.length/151*100)+'%';o.disconnect()}}).observe(barra);
}else{$$('.rev').forEach(function(el){el.classList.add('vis')});barra.style.width=(D.poke.length/151*100)+'%'}
})();
