const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1312,height:740}});
const errs=[];p.on('pageerror',e=>errs.push('PE '+e.message));
await p.goto('http://localhost:8765/index.html');await p.evaluate(()=>{localStorage.clear();localStorage.setItem('lyap_v5',JSON.stringify({lang:'uk',tutSlaps:3}))});await p.reload();await p.waitForTimeout(800);
await p.evaluate(()=>document.querySelectorAll('.overlay').forEach(o=>o.remove()));
await p.evaluate(()=>document.querySelector('[data-a="record"]').click());await p.waitForTimeout(1500);
const slap=async(d,dx=0)=>{const c=await p.$eval('#table .tcard:last-child',e=>{const r=e.getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2,h:r.height}});const sx=c.x+dx,sy=c.y+c.h/2+12;await p.mouse.move(sx,sy);await p.mouse.down();await p.mouse.move(sx,sy+d,{steps:5});await p.waitForTimeout(80);await p.mouse.up();await p.waitForTimeout(2500)};
let got=0;for(let i=0;i<12&&!got;i++){await slap([110,140,90,160][i%4]);const m=await p.$('.overlay');const s=await p.$eval('#serie',e=>e.textContent).catch(()=>'');console.log('try',i,s,!!m);if(m){await p.evaluate(()=>{const b=document.querySelector('#sA')||document.querySelector('#rvN');b&&b.click()});await p.waitForTimeout(1500)}else if(s.includes('1'))got=1}
await slap(60,300);
console.log('after miss modal:',!!await p.$('#rvY'), await p.$eval('.overlay',e=>e.innerText.slice(0,200)).catch(()=>'none'));
await p.screenshot({path:'rv1.png'});
if(await p.$('#rvY')){await p.evaluate(()=>document.querySelector('#rvY').click());await p.waitForTimeout(4200);await p.screenshot({path:'rv2.png'});
 await slap(60,300);console.log('second:',!!await p.$('#rvY'), await p.$eval('.overlay',e=>e.innerText.slice(0,120)).catch(()=>'none'));await p.screenshot({path:'rv3.png'})}
console.log('ERR',JSON.stringify(errs));await b.close()})();
