// ===== i18n: Ukrainian source text is translated on screen through a dictionary (exact phrases + phrases with {} slots)
const LANGS=[['uk','Українська'],['en','English'],['es','Español'],['pt','Português (Brasil)'],['de','Deutsch'],['fr','Français'],['pl','Polski'],['cs','Čeština'],['tr','Türkçe'],['id','Bahasa Indonesia'],['hi','हिन्दी']];
const LANG=(()=>{let l='';try{l=(JSON.parse(localStorage.getItem('lyap_v5'))||{}).lang||''}catch(e){}
  if(!l){const n=(navigator.languages&&navigator.languages[0]||navigator.language||'en').toLowerCase().slice(0,2);l=n==='ru'||n==='be'?'uk':n;}
  return LANGS.some(x=>x[0]===l)?l:'en'})();
function curLang(){return LANG}
document.documentElement.lang=LANG;
const I18N_DATA=__I18N__;
const TD=LANG==='uk'?null:(I18N_DATA[LANG]||null);
const TP=[];// patterns
if(TD){Object.keys(TD).forEach(k=>{if(k.includes('{}')){const parts=k.split('{}').map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));TP.push({re:new RegExp('^'+parts.join('(.+?)')+'$'),out:TD[k],n:parts.length-1,len:k.length})}});TP.sort((a,b)=>b.len-a.len)}
const CYR=/[Ѐ-ӿ]/;
function tr(s){if(!TD||!s||!CYR.test(s))return s;const m=s.match(/^(\s*)([\s\S]*?)(\s*)$/);const core=m[2];if(!core)return s;
  const c2=core.replace(/\s+/g,' ');let r=TD[core];if(r===undefined)r=TD[c2];let part;
  if(r===undefined){for(const p of TP){const mm=c2.match(p.re);if(mm){let i=0;const o=p.out.replace(/\{(\d?)\}/g,(x,d)=>{const v=mm[1+(d!==''?+d:i++)];return v===undefined?'':tr(v)});if(!CYR.test(o)){r=o;break}if(part===undefined)part=o}}}
  if(r===undefined){const st=c2.match(/^(.*?)(\s*★+)$/);if(st&&CYR.test(st[1])){const t=tr(st[1]);if(t!==st[1])r=t+st[2]}}
  if(r===undefined){for(const sep of [', ',' · ']){if(c2.includes(sep)){const parts=c2.split(sep);const tt=parts.map(tr);if(tt.some((x,k)=>x!==parts[k])){const o=tt.join(sep);if(!CYR.test(o)){r=o;break}if(part===undefined)part=o}}}}
  if(r===undefined){const ss=c2.split(/(?<=[.!?…])\s+/);if(ss.length>1){const tt=ss.map(tr);const o=tt.join(' ');if(!CYR.test(o))r=o;else if(part===undefined&&tt.some((x,k)=>x!==ss[k]))part=o}}
  if(r===undefined)r=part;
  return r===undefined?s:m[1]+r+m[3]}
function trNode(n){if(n.nodeType===3){const v=n.nodeValue;if(CYR.test(v)){const t=tr(v);if(t!==v)n.nodeValue=t}return}
  if(n.nodeType!==1)return;if(n.tagName==='SCRIPT'||n.tagName==='STYLE')return;
  for(const a of ['alt','title','aria-label','placeholder']){const v=n.getAttribute&&n.getAttribute(a);if(v&&CYR.test(v))n.setAttribute(a,tr(v))}
  for(let c=n.firstChild;c;c=c.nextSibling)trNode(c)}
if(TD){const mo=new MutationObserver(ms=>{for(const m of ms){if(m.type==='characterData')trNode(m.target);else if(m.type==='attributes')trNode(m.target);else m.addedNodes.forEach(trNode)}});
  addEventListener('DOMContentLoaded',()=>{trNode(document.body);mo.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['alt','title','aria-label']})});
  if(document.body){trNode(document.body);mo.observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['alt','title','aria-label']})}}
const NUMLOC={uk:'uk-UA',en:'en-US',es:'es-ES',pt:'pt-BR',de:'de-DE',fr:'fr-FR',pl:'pl-PL',cs:'cs-CZ',tr:'tr-TR',id:'id-ID',hi:'hi-IN'}[LANG];
