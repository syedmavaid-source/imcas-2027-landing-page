/* Expert sessions: each day's CMS list holds all its sessions (sorted by Order); place card 2 in the second row and card 3 in a third row, as on the coded page */
(function(){var R=document.getElementById('ev-native');if(!R)return;R.querySelectorAll('#suite .hday').forEach(function(day){var it=day.querySelector('.slot.am .w-dyn-items');if(!it)return;
var items=[].slice.call(it.children);var pm=day.querySelector('.slot.pm');var p3=document.createElement('div');p3.className='slot p3';day.appendChild(p3);
[[items[1],pm],[items[2],p3]].forEach(function(x){if(!x[0]||!x[1])return;[].slice.call(x[1].children).forEach(function(c){c.style.display='none'});var l=document.createElement('div');l.className='w-dyn-list';var li=document.createElement('div');li.className='w-dyn-items';li.appendChild(x[0]);l.appendChild(li);x[1].appendChild(l)})})})();
/* ===== event phases (native): live section + card states built from the CMS cards on the page ===== */
(function(){var R=document.getElementById('ev-native');if(!R||getComputedStyle(R).display==='none')return;
var PH=document.documentElement.dataset.phase||'before';if(PH!=='during')return;
var now=function(){return (window.parisNow?window.parisNow():'')};
var DAYS=['2027-01-28','2027-01-29','2027-01-30'],DAYL=['Thursday 28 January','Friday 29 January','Saturday 30 January'];
var T={live:'Live now',ended:'Ended',next:'Up next',until:'until',startsIn:'starts in',min:'min',onStage:'On stage now',upNext:'Up next',allDay:'All day',boothT:'Booth N214 · Level 2',boothS:'Visit and collect your exclusive gift',doneH:'That is all for today',doneT:'See you tomorrow',doneLast:'Thank you for joining us at IMCAS Paris',today:'Today',sym:'BioScience Symposium',suite:'Expert session',faculty:'All faculty'};
function mins(hm){var p=String(hm).trim().split(':');return (+p[0])*60+(+p[1])}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function txt(el,sel){var e=el.querySelector(sel);return e?e.textContent.trim():''}
function chip(s){return s==='live'?'<span class="stc live"><span class="dot"></span>'+T.live+'</span>':s==='ended'?'<span class="stc">'+T.ended+'</span>':''}
function n(){var t=now();return {d:t.slice(0,10),m:mins(t.slice(11,16))}}
/* ---- read the programme from the CMS-rendered cards ---- */
var ev=[],talks=[];
var suWhere=(function(){var b=R.querySelectorAll('#suite .bar span');return 'Hospitality Suite · '+(b.length>1?b[1].textContent.split('·')[0].trim():'')})();
R.querySelectorAll('#suite .hday').forEach(function(day,k){day.querySelectorAll('.tc:not(.sym)').forEach(function(c){var t=txt(c,'time').split(/[–-]/);if(t.length<2)return;
  var lg=txt(c,'.lgt');ev.push({k:k,a:t[0].trim(),b:t[1].trim(),title:txt(c,'h4'),where:suWhere+(lg?' · '+lg:''),who:txt(c,'.fc small'),pics:[].map.call(c.querySelectorAll('.fc img'),function(i){return i.src}),link:'#suite',el:c,tag:c.querySelector('.tct')})})});
var symBar=R.querySelectorAll('#symposium .bar span'),symDay=symBar.length?symBar[0].textContent:'',symW=symBar.length>1?symBar[1].textContent:'';
var sk=DAYL.findIndex(function(l){return symDay.indexOf(l.split(' ')[1])>=0}),sr=(symW.match(/(\d\d:\d\d)\s*[–-]\s*(\d\d:\d\d)/)||[]);
var cards=R.querySelectorAll('#symposium .lc');
cards.forEach(function(c,i){talks.push({a:txt(c,'.lhd time'),who:txt(c,'.lbd small'),title:txt(c,'.lbd b'),pic:(c.querySelector('.lph img')||c.querySelector('.lpan img')||{}).src||'',el:c})});
talks.forEach(function(t,i){t.b=i<talks.length-1?talks[i+1].a:(sr[2]||t.a)});
if(sk>=0&&sr[1])ev.push({k:sk,a:sr[1],b:sr[2],title:T.sym,where:symW.replace(/^\s*\d\d:\d\d\s*[–-]\s*\d\d:\d\d\s*·\s*/,''),who:'',pics:talks.slice(0,5).map(function(t){return t.pic}),link:'#symposium',sym:true});
/* ---- status on the cards ---- */
function st(k,a,b){var x=n(),dd=DAYS[k];if(dd<x.d)return 'ended';if(dd>x.d)return 'later';return x.m>=mins(b)?'ended':x.m>=mins(a)?'live':'later'}
function mark(){ev.forEach(function(e){if(!e.el)return;var s=st(e.k,e.a,e.b);e.el.classList.remove('st-live','st-ended');e.el.querySelectorAll('.stc').forEach(function(x){x.remove()});if(s==='live'||s==='ended'){e.el.classList.add('st-'+s);e.tag.insertAdjacentHTML('beforeend',chip(s))}});
 if(sk>=0)talks.forEach(function(t){var s=st(sk,t.a,t.b);t.el.classList.remove('st-live','st-ended');t.el.querySelectorAll('.stc').forEach(function(x){x.remove()});if(s==='live'||s==='ended'){t.el.classList.add('st-'+s);var bd=t.el.querySelector('.lbd');if(bd)bd.insertAdjacentHTML('beforeend',chip(s))}})}
/* ---- live section ---- */
function render(){var x=n(),k=DAYS.indexOf(x.d);if(k<0)k=1;
 var day=document.getElementById('nowDay');if(day)day.textContent=T.today+' · '+DAYL[k];
 var es=ev.filter(function(e){return e.k===k}).sort(function(p,q){return mins(p.a)-mins(q.a)});
 es.forEach(function(e){e.s=x.m>=mins(e.b)?'ended':x.m>=mins(e.a)?'live':'later'});
 var live=es.filter(function(e){return e.s==='live'})[0],next=es.filter(function(e){return e.s==='later'})[0],h=live||next,c='';
 if(h){c=(live?'<span class="nowb"><span class="dot"></span>'+T.live+' · '+T.until+' '+h.b+'</span>':'<span class="nowb next">'+T.upNext+' · '+(mins(h.a)-x.m<=120?T.startsIn+' '+(mins(h.a)-x.m)+' '+T.min:h.a)+'</span>')
  +'<h3>'+esc(h.title)+'</h3><p class="now-meta"><b>'+h.a+'–'+h.b+'</b> · '+esc(h.where)+'</p>'
  +'<div class="now-faces"><span>'+h.pics.map(function(p){return '<img src="'+p+'" alt="">'}).join('')+'</span><small>'+esc(h.sym?'8 experts · Genefill DX live demo':h.who)+'</small></div>';
  if(live&&live.sym){var i=-1;talks.forEach(function(t,j){if(x.m>=mins(t.a)&&x.m<mins(t.b))i=j});if(i>=0){var cur=talks[i],nx=talks[i+1];
   c+='<div class="onstage"><div><img src="'+cur.pic+'" alt=""><span><small>'+T.onStage+' · '+cur.a+'</small><b>'+esc(cur.who)+' · '+esc(cur.title)+'</b></span></div>'+(nx?'<div><img src="'+nx.pic+'" alt=""><span><small>'+T.upNext+' · '+nx.a+'</small><b>'+esc(nx.who)+' · '+esc(nx.title)+'</b></span></div>':'')+'</div>'}}
  c+='<a class="cta teal" href="'+h.link+'">'+(h.sym?T.sym:T.suite)+' →</a>'}
 else{var nd=ev.filter(function(e){return e.k===k+1}).sort(function(p,q){return mins(p.a)-mins(q.a)})[0];
  c='<span class="nowb next">'+T.doneH+'</span><h3>'+(k<2?T.doneT:T.doneLast)+'</h3><p class="now-meta">'+(nd?esc(DAYL[k+1]+' · '+nd.a+' · '+nd.title):esc(T.boothT))+'</p>'}
 var card=document.getElementById('nowCard');if(card)card.innerHTML=c;
 var row=function(t,b,s,cls,tag){return '<li class="'+cls+'"><time>'+t+'</time><div><b>'+esc(b)+'</b><span>'+esc(s)+'</span></div>'+tag+'</li>'};
 var list=document.getElementById('todayList');if(list)list.innerHTML=row(T.allDay,T.boothT,T.boothS,'','')+es.map(function(e){return row(e.a+'–'+e.b,e.title,e.where+(e.who?' · '+e.who:(e.sym?' · 8 experts · Genefill DX live demo':'')),e.s,(e===next&&!live)?'<span class="stc next">'+T.next+'</span>':chip(e.s))}).join('');
 mark()}
render();setInterval(render,60000)})();
