const P=process.argv[2];
const topo=require(P+'/topojson-client-3.1.0/package/dist/topojson-client.js');
const w=require(P+'/world-atlas-2.0.2/package/countries-50m.json');
const fc=topo.feature(w,w.objects.countries);
const br=fc.features.find(f=>f.id==='076');
let polys=br.geometry.type==='Polygon'?[br.geometry.coordinates]:br.geometry.coordinates;
// largest ring
let ring=polys.map(p=>p[0]).sort((a,b)=>b.length-a.length)[0];
const lat0=-14*Math.PI/180, k=Math.cos(lat0);
let pts=ring.map(([lo,la])=>[lo*k,-la]);
// RDP
function rdp(p,e){if(p.length<3)return p;let d=0,i=0;const[a,b]=[p[0],p[p.length-1]];for(let j=1;j<p.length-1;j++){const[x,y]=p[j];const num=Math.abs((b[1]-a[1])*x-(b[0]-a[0])*y+b[0]*a[1]-b[1]*a[0]);const den=Math.hypot(b[1]-a[1],b[0]-a[0])||1;const dd=num/den;if(dd>d){d=dd;i=j}}if(d>e){return rdp(p.slice(0,i+1),e).slice(0,-1).concat(rdp(p.slice(i),e))}return[a,b]}
pts.pop();const m=Math.floor(pts.length/2);pts=rdp(pts.slice(0,m+1),0.12).slice(0,-1).concat(rdp(pts.slice(m),0.12));
const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);const minx=Math.min(...xs),miny=Math.min(...ys),maxx=Math.max(...xs),maxy=Math.max(...ys);
const W=400,s=W/(maxx-minx),H=(maxy-miny)*s;
const f=n=>Math.round(n*10)/10;
const proj=([x,y])=>[f((x-minx)*s),f((y-miny)*s)];
const d='M'+pts.map(proj).map(p=>p.join(' ')).join('L')+'Z';
// São Paulo capital and Bauru for dots
const pt=(lo,la)=>proj([lo*k,-la]);
console.log(JSON.stringify({w:W,h:f(H),n:pts.length,d,sp:pt(-46.63,-23.55),bauru:pt(-49.07,-22.33)}));
