const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1312,height:740}});
const errs=[];p.on('pageerror',e=>errs.push('PE '+e.message));
const lang=process.argv[2]||'en';const left=new Set();
await p.goto('http://localhost:8765/index.html');
await p.evaluate(l=>{localStorage.clear();localStorage.setItem('lyap_v5',JSON.stringify({lang:l}))},lang);await p.reload();await p.waitForTimeout(800);
const grab=async()=>{try{const a=await p.evaluate(()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const v=n.nodeValue.trim();if(/[Ѐ-ӿ]/.test(v)&&!['SCRIPT','STYLE','OPTION'].includes(n.parentElement.tagName))out.push(v)}return out});a.forEach(x=>left.add(x))}catch(e){}};
const ev=async f=>{try{await p.evaluate(f)}catch(e){}};const W=ms=>p.waitForTimeout(ms);
const close=async()=>{await grab();await ev(()=>document.querySelectorAll('.overlay').forEach(o=>o.remove()))};
const shot=async n=>{await grab();await p.screenshot({path:'y_'+lang+'_'+n+'.png'})};
await ev(()=>{const S=JSON.parse(localStorage.getItem('lyap_v5'));S.coins=900000;S.dup={'cosmo:0':8,'kometa:0':6,'luna:0':3,'bobyk:0':5};S.album['zhar:0']=1;S.album['luna:1']=1;S.decor={bench:1,fountain:1,sakura:1};localStorage.setItem('lyap_v5',JSON.stringify(S))});
await p.reload();await W(900);await close();
await ev(()=>document.querySelector('[data-a="quests"]').click());await W(300);await close();
await ev(()=>document.querySelector('[data-a="bank"]').click());await W(300);await grab();
await ev(()=>document.querySelector('[data-a="break"]').click());await W(1500);await shot('break');await ev(()=>document.querySelector('#mQuit')&&document.querySelector('#mQuit').click());await W(500);await close();
await p.reload();await W(800);await close();
for(const t of ['gums','daily','glove','back','dust','anim','frame']){await ev(()=>document.querySelector('[data-a="shop"]').click());await W(200);await ev(t=>{const b=document.querySelector('[data-st="'+t+'"]');b&&b.click()},t);await W(300);if(t==='glove')await shot('shopglove');await close()}
await ev(()=>document.querySelector('[data-a="album"]').click());await W(300);await ev(()=>document.querySelector('.slot').click());await W(300);await shot('detail');await close();
await ev(()=>document.querySelector('[data-a="album"]').click());await W(300);await ev(()=>document.querySelector('#exch').click());await W(300);await shot('exch');
await ev(()=>document.querySelector('[data-ex]:not([disabled])')&&document.querySelector('[data-ex]:not([disabled])').click());await W(500);await close();
await ev(()=>document.querySelector('[data-a="yard"]').click());await W(800);
for(const t of ['house','fence','ground','decor','trees','flowers','slots']){await ev(()=>document.querySelector('#yEdit').click());await W(200);await ev(t=>document.querySelector('[data-yt="'+t+'"]').click(),t);await W(250);if(t==='trees')await shot('ytrees');await grab()}
await ev(()=>document.querySelector('[data-selld]').click());await W(300);await shot('sell');await close();
await p.reload();await W(800);await close();
await ev(()=>document.querySelector('#meP').click());await W(300);await shot('profile');await ev(()=>document.querySelector('#chT').click());await W(300);await close();
await ev(()=>document.querySelector('#meP').click());await W(300);await ev(()=>document.querySelector('#chA').click());await W(300);await close();
for(const t of ['coll','stack','serie','serieNH','yard']){await ev(()=>document.querySelector('[data-a="rating"]').click());await W(200);await ev(t=>document.querySelector('[data-rt="'+t+'"]').click(),t);await W(200);await close()}
await ev(()=>document.querySelector('[data-a="play"]').click());await W(400);await shot('tut');await ev(()=>document.querySelector('#tutOk').click());await W(400);await shot('hand');
await ev(()=>document.querySelector('#hGo').click());await W(500);await shot('vs');await ev(()=>document.querySelector('#gg').click());await W(800);
await ev(()=>document.querySelector('#fanP .fc').click());await W(2600);await shot('duel');
await ev(()=>document.querySelector('#mQuit').click());await W(300);await shot('quit');await ev(()=>document.querySelector('#y').click());await W(800);await shot('end');
console.log('LEFT',JSON.stringify([...left]));console.log('ERR',JSON.stringify(errs));await b.close()})();
