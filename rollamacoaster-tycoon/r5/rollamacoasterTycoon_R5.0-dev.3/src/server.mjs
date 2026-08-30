import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const PORT=Number(process.env.PORT||8765), HOST=process.env.HOST||'0.0.0.0', DATA=process.env.DATA_DIR||path.resolve('data');
fs.mkdirSync(DATA,{recursive:true});
const codex=JSON.parse(fs.readFileSync(new URL('../codex.json',import.meta.url),'utf8'));
const verse={id:'Psalm.119.24',reference:'Psalm 119:24',text:codex['Psalm']['119']['24'],wisdom:'God’s testimonies can serve as counsel; wisdom is perceived from the verse itself.'};
const initial={version:'R5.0-dev.3',tick:0,simulationRunning:true,codexAvailable:true,entity:{timeline:0,happiness:55,wisdom:0,lastPerception:null},events:[]};
const file=path.join(DATA,'world.json');
let loaded=fs.existsSync(file)?JSON.parse(fs.readFileSync(file,'utf8')):null;
let world=loaded?.version===initial.version?loaded:structuredClone(initial);
function perceive(){
  if(!world.codexAvailable){world.entity.lastPerception=null;return;}
  world.entity.lastPerception={unitId:verse.id,reference:verse.reference,text:verse.text,wisdom:verse.wisdom};
  world.entity.wisdom=Math.min(100,world.entity.wisdom+0.12);
}
function applyRules(){
  if(!world.simulationRunning)return;
  world.tick++;
  world.entity.timeline=(world.entity.timeline+0.006)%1;
  if(world.codexAvailable){perceive();world.entity.happiness=Math.min(100,world.entity.happiness+0.08);}else{world.entity.happiness=Math.max(0,world.entity.happiness-0.06);}
}
setInterval(applyRules,100);
const page=`<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>R5 dev.3</title><style>html,body{margin:0;min-height:100%;background:#101419;color:#e9eef5;font:14px system-ui}#bar{position:fixed;z-index:2;padding:12px;background:#151c24ee;border-radius:0 0 12px 0;max-width:min(520px,calc(100% - 24px))}button{margin:3px;padding:9px 12px}canvas{width:100%;height:100%;position:fixed;inset:0;display:block}.wisdom{white-space:pre-wrap;color:#d7e4cf;max-width:500px}</style></head><body><div id=bar><b>R5 miniature world • Codex perception proof</b><br><button id=sim>Simulation</button><button id=codex>Codex</button><button onclick="cmd('save')">Save</button><button onclick="cmd('reset')">Reset</button><pre id=s></pre><div class=wisdom id=w></div></div><canvas id=c></canvas><script>
const c=document.querySelector('#c'),x=c.getContext('2d'),s=document.querySelector('#s'),wis=document.querySelector('#w'),sim=document.querySelector('#sim'),cod=document.querySelector('#codex');function resize(){c.width=innerWidth*devicePixelRatio;c.height=innerHeight*devicePixelRatio}onresize=resize;resize();async function cmd(a){await fetch('/api/command',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({action:a})})}sim.onclick=()=>cmd('simulation');cod.onclick=()=>cmd('codex');async function frame(){let q=await fetch('/api/world'),v=await q.json();sim.textContent=v.simulationRunning?'Stop simulation':'Start simulation';cod.textContent=v.codexAvailable?'Codex available':'Codex unavailable';s.textContent='tick: '+v.tick+' | happiness: '+v.entity.happiness.toFixed(0)+' | wisdom: '+v.entity.wisdom.toFixed(0);wis.textContent=v.entity.lastPerception?'Perceived '+v.entity.lastPerception.reference+'\n“'+v.entity.lastPerception.text+'”\nWisdom: '+v.entity.lastPerception.wisdom:'No Codex perception.';x.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);x.clearRect(0,0,innerWidth,innerHeight);x.fillStyle='#172b20';x.fillRect(0,0,innerWidth,innerHeight);let cx=innerWidth/2,cy=innerHeight/2;x.strokeStyle='#8d989e';x.lineWidth=18;x.beginPath();x.arc(cx,cy,150,0,Math.PI*2);x.stroke();let a=v.entity.timeline*Math.PI*2-Math.PI/2,px=cx+Math.cos(a)*150,py=cy+Math.sin(a)*150;x.fillStyle=v.entity.happiness>60?'#f5d46f':'#d3a46b';x.beginPath();x.arc(px,py,12,0,Math.PI*2);x.fill();x.fillStyle=v.codexAvailable?'#d7e4cf':'#59616a';x.fillRect(cx-28,cy-22,56,44);x.fillStyle='#101419';x.font='12px system-ui';x.textAlign='center';x.fillText('CODEX',cx,cy+4);requestAnimationFrame(frame)}frame();</script></body></html>`;
const server=http.createServer(async(req,res)=>{if(req.url==='/api/world'){res.setHeader('content-type','application/json');return res.end(JSON.stringify(world))}if(req.url==='/api/codex'){res.setHeader('content-type','application/json');return res.end(JSON.stringify(codex))}if(req.url==='/health')return res.end('ok');if(req.url==='/api/command'&&req.method==='POST'){let b='';for await(const ch of req)b+=ch;let {action}=JSON.parse(b||'{}');if(action==='simulation')world.simulationRunning=!world.simulationRunning;if(action==='codex'){world.codexAvailable=!world.codexAvailable;if(world.codexAvailable)perceive();else world.entity.lastPerception=null;}if(action==='save')fs.writeFileSync(file,JSON.stringify(world,null,2));if(action==='reset'){world=structuredClone(initial);perceive();fs.writeFileSync(file,JSON.stringify(world,null,2));}world.events.push({tick:world.tick,action});res.setHeader('content-type','application/json');return res.end(JSON.stringify({ok:true,world}))}res.setHeader('content-type','text/html');res.end(page)});
server.listen(PORT,HOST,()=>console.log(`R5 dev.2 listening on http://${HOST}:${PORT}`));
