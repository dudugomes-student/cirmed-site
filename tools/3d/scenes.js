// Cenas 3D da Cirmed, renderizadas uma vez (tools/3d/render.py) e salvas como imagem.
// Material: plástico branco brilhante com detalhes no azul da marca. Sem vermelho.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';

const C = { blue: 0x2475A3, deep: 0x155E89, navy: 0x0D1B36, sky: 0xE6F1F8, mist: 0x8DBBD9, white: 0xFFFFFF };
const mat = (color, o = {}) => new THREE.MeshPhysicalMaterial({ color, roughness: 0.32, clearcoat: 0.6, clearcoatRoughness: 0.25, ...o });
const M = {
  white: () => mat(0xF7FAFC),
  sky: () => mat(0xDCEBF5),
  mist: () => mat(C.mist),
  blue: () => mat(C.blue, { roughness: 0.28 }),
  deep: () => mat(C.deep),
  glass: () => new THREE.MeshPhysicalMaterial({ color: 0xBFDCEE, roughness: 0.08, transmission: 0.6, thickness: 4, clearcoat: 1, transparent: true }),
  metal: () => new THREE.MeshPhysicalMaterial({ color: 0xD9E4EC, metalness: 0.85, roughness: 0.25 }),
};
const rbox = (w, h, d, r, m) => new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 5, r), m);
const cyl = (rt, rb, h, m, seg = 48) => new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), m);
const sph = (r, m) => new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), m);

function cross(size, depth, m) {
  const s = size, t = size / 3;
  const shape = new THREE.Shape();
  shape.moveTo(-t / 2, -s / 2); shape.lineTo(t / 2, -s / 2); shape.lineTo(t / 2, -t / 2); shape.lineTo(s / 2, -t / 2);
  shape.lineTo(s / 2, t / 2); shape.lineTo(t / 2, t / 2); shape.lineTo(t / 2, s / 2); shape.lineTo(-t / 2, s / 2);
  shape.lineTo(-t / 2, t / 2); shape.lineTo(-s / 2, t / 2); shape.lineTo(-s / 2, -t / 2); shape.lineTo(-t / 2, -t / 2); shape.closePath();
  const g = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelSize: s * 0.04, bevelThickness: s * 0.04, bevelSegments: 4 });
  g.center();
  return new THREE.Mesh(g, m);
}

// Estetoscópio: tubo, olivas, haste dupla e auscultador.
function stethoscope({ scale = 1, tubeColor = M.blue(), points } = {}) {
  const g = new THREE.Group();
  const pts = points || [
    [-1.1, 0, -2.2], [-1.3, 0, -1.2], [-0.6, 0, -0.3], [0, 0, 0.3],
    [0.6, 0, -0.3], [1.3, 0, -1.2], [1.1, 0, -2.2]
  ].map(p => new THREE.Vector3(...p));
  // binaural (formato de Y)
  const yCurve = new THREE.CatmullRomCurve3(pts);
  g.add(new THREE.Mesh(new THREE.TubeGeometry(yCurve, 120, 0.11, 24), M.metal()));
  [pts[0], pts[pts.length - 1]].forEach(p => { const o = sph(0.2, M.deep()); o.position.copy(p); g.add(o); });
  // tubo até o auscultador
  const tube = new THREE.CatmullRomCurve3([
    new THREE.Vector3(0, 0, 0.3), new THREE.Vector3(0, 0, 1.4), new THREE.Vector3(-0.9, 0, 2.4),
    new THREE.Vector3(-0.4, 0, 3.6), new THREE.Vector3(1.0, 0, 3.7), new THREE.Vector3(1.6, 0, 2.9)
  ]);
  g.add(new THREE.Mesh(new THREE.TubeGeometry(tube, 160, 0.17, 28), tubeColor));
  // auscultador
  const head = new THREE.Group();
  const disc = cyl(0.62, 0.62, 0.28, M.metal()); head.add(disc);
  const membrane = cyl(0.5, 0.5, 0.3, M.white()); membrane.position.y = 0.02; head.add(membrane);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.58, 0.09, 24, 64), M.blue()); ring.rotation.x = Math.PI / 2; ring.position.y = 0.15; head.add(ring);
  const stem = cyl(0.12, 0.12, 0.6, M.metal()); stem.rotation.z = Math.PI / 2; stem.position.set(-0.6, 0, 0); head.add(stem);
  head.position.set(2.2, 0.05, 2.9);
  g.add(head);
  g.scale.setScalar(scale);
  return g;
}

function brazil(BR, { depth = 26 } = {}) {
  const nums = BR.d.replace(/[MZ]/g, '').split('L').map(s => s.trim().split(/\s+/).map(Number));
  const shape = new THREE.Shape(nums.map(([x, y]) => new THREE.Vector2(x, -y)));
  const geo = new THREE.ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelSize: 4, bevelThickness: 4, bevelSegments: 5, curveSegments: 4 });
  geo.rotateX(-Math.PI / 2); // deita o mapa no chão (topo virado para cima)
  const sideMat = M.blue(), topMat = M.sky();
  const mesh = new THREE.Mesh(geo, [topMat, sideMat]);
  const g = new THREE.Group(); g.add(mesh);
  // centraliza: o mapa vai de x 0..400, z 0..BR.h
  mesh.position.set(-BR.w / 2, 0, -BR.h / 2);
  g.userData.top = depth + 4;
  g.userData.toWorld = ([x, y]) => new THREE.Vector3(x - BR.w / 2, depth + 4, y - BR.h / 2);
  return g;
}

function pin(m = M.blue(), h = 1) {
  const g = new THREE.Group();
  const head = sph(0.55, m); head.position.y = 1.5 * h; g.add(head);
  const cone = new THREE.Mesh(new THREE.ConeGeometry(0.42, 1.2 * h, 40), m); cone.rotation.x = Math.PI; cone.position.y = 0.75 * h; g.add(cone);
  const dot = sph(0.24, M.white()); dot.position.set(0, 1.5 * h, 0.42); g.add(dot);
  return g;
}

function building({ w = 3, h = 2.4, d = 2.4, floors = 3, cols = 4, accent = M.blue(), roof = true } = {}) {
  const g = new THREE.Group();
  const body = rbox(w, h, d, 0.16, M.white()); body.position.y = h / 2; g.add(body);
  const win = M.glass();
  for (let f = 0; f < floors; f++) for (let c = 0; c < cols; c++) {
    const wx = -w / 2 + (c + 0.5) * (w / cols), wy = 0.45 + f * ((h - 0.7) / floors) + 0.25;
    const wm = rbox(w / cols * 0.55, (h - 0.7) / floors * 0.55, 0.12, 0.05, win); wm.position.set(wx, wy, d / 2 + 0.02); g.add(wm);
  }
  if (roof) { const r = rbox(w + 0.2, 0.22, d + 0.2, 0.08, accent); r.position.y = h + 0.08; g.add(r); }
  return g;
}

const BUILD = {
  hero(ctx) {
    const g = new THREE.Group();
    const map = brazil(ctx.BR); map.scale.setScalar(0.024); g.add(map);
    const s = 0.024;
    const p = pin(M.blue(), 1); const b = map.userData.toWorld(ctx.BR.bauru).multiplyScalar(s); p.position.copy(b); p.scale.setScalar(0.62); g.add(p);
    // anéis de "sinal" ao redor do pino
    [0.55, 0.85].forEach((r, i) => { const t = new THREE.Mesh(new THREE.TorusGeometry(r, 0.035, 16, 80), M.mist()); t.rotation.x = Math.PI / 2; t.position.set(b.x, b.y + 0.02, b.z); t.material.transparent = true; t.material.opacity = 0.9 - i * 0.35; g.add(t); });
    const st = stethoscope({ scale: 0.95 }); st.position.set(-6.2, 0.12, -0.6); st.rotation.y = 0.55; g.add(st);
    return { group: g, cam: [-0.6, 13.5, 12.5], look: [-0.9, 0, 0.6], fov: 34, shadow: true };
  },
  mapPins(ctx) {
    const g = new THREE.Group();
    const map = brazil(ctx.BR); map.scale.setScalar(0.024); g.add(map);
    ctx.pins.forEach(([x, y], i) => {
      const p = pin(i === 0 ? M.blue() : M.deep(), 1); p.position.copy(map.userData.toWorld([x, y]).multiplyScalar(0.024)); p.scale.setScalar(0.38); g.add(p);
    });
    return { group: g, cam: [0, 13.5, 11.5], look: [0, 0, 0.5], fov: 34, shadow: true };
  },
  stethoscope() {
    const g = stethoscope({ scale: 1 }); g.rotation.y = -0.35; g.position.set(-0.2, 0.2, -0.8);
    return { group: g, cam: [0.6, 8.5, 5.6], look: [0.2, 0, 0.6], fov: 34, shadow: true };
  },
  calendar() {
    const g = new THREE.Group();
    const base = rbox(4, 0.5, 3.6, 0.22, M.white()); base.position.y = 0.25; g.add(base);
    const top = rbox(4, 0.62, 0.9, 0.22, M.blue()); top.position.set(0, 0.36, -1.35); g.add(top);
    [-1.1, 1.1].forEach(x => { const r = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.07, 16, 40), M.metal()); r.position.set(x, 0.75, -1.35); g.add(r); });
    const on = new Set(['0,1', '2,0', '1,2', '3,1', '4,2', '2,2']);
    for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) {
      const filled = on.has(`${c},${r}`);
      const cell = rbox(0.56, filled ? 0.3 : 0.14, 0.56, 0.1, filled ? (r === 2 ? M.deep() : M.blue()) : M.sky());
      cell.position.set(-1.44 + c * 0.72, 0.5 + (filled ? 0.15 : 0.07), -0.45 + r * 0.72); g.add(cell);
    }
    g.rotation.y = 0.35;
    return { group: g, cam: [0, 5.6, 5.4], look: [0, 0.3, 0], fov: 36, shadow: true };
  },
  hospital() {
    const g = new THREE.Group();
    const main = building({ w: 3.4, h: 2.8, d: 2.2, floors: 3, cols: 4 }); g.add(main);
    const wingL = building({ w: 1.6, h: 1.7, d: 2, floors: 2, cols: 2 }); wingL.position.x = -2.5; g.add(wingL);
    const wingR = building({ w: 1.6, h: 1.7, d: 2, floors: 2, cols: 2 }); wingR.position.x = 2.5; g.add(wingR);
    const sign = rbox(1.1, 1.1, 0.3, 0.2, M.blue()); sign.position.set(0, 3.55, 0); g.add(sign);
    const cr = cross(0.72, 0.12, M.white()); cr.position.set(0, 3.55, 0.2); g.add(cr);
    const door = rbox(0.9, 0.9, 0.16, 0.08, M.glass()); door.position.set(0, 0.45, 1.12); g.add(door);
    g.rotation.y = -0.42;
    return { group: g, cam: [1.2, 3.8, 8.6], look: [0, 1.4, 0], fov: 34, shadow: true };
  },
  ubs() {
    const g = new THREE.Group();
    const body = rbox(3, 1.6, 2.2, 0.16, M.white()); body.position.y = 0.8; g.add(body);
    // telhado de duas águas
    const roofShape = new THREE.Shape([new THREE.Vector2(-1.75, 0), new THREE.Vector2(1.75, 0), new THREE.Vector2(0, 1.05)]);
    const rg = new THREE.ExtrudeGeometry(roofShape, { depth: 2.5, bevelEnabled: true, bevelSize: 0.06, bevelThickness: 0.06, bevelSegments: 3 }); rg.translate(0, 0, -1.25);
    const roof = new THREE.Mesh(rg, M.blue()); roof.position.y = 1.6; g.add(roof);
    const plate = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.12, 48), M.white()); plate.rotation.x = Math.PI / 2; plate.position.set(0, 2.0, 1.36); g.add(plate);
    const cr = cross(0.5, 0.08, M.blue()); cr.position.set(0, 2.0, 1.45); g.add(cr);
    const door = rbox(0.7, 1, 0.14, 0.08, M.glass()); door.position.set(0, 0.5, 1.12); g.add(door);
    [-0.95, 0.95].forEach(x => { const w = rbox(0.6, 0.5, 0.12, 0.06, M.glass()); w.position.set(x, 0.95, 1.12); g.add(w); });
    g.rotation.y = -0.45;
    return { group: g, cam: [1, 3.6, 7], look: [0, 1.1, 0], fov: 34, shadow: true };
  },
  upa() {
    const g = new THREE.Group();
    const b = building({ w: 3.6, h: 1.9, d: 2.4, floors: 2, cols: 4 }); g.add(b);
    const canopy = rbox(2.2, 0.16, 1.2, 0.06, M.blue()); canopy.position.set(0.6, 1.1, 1.75); g.add(canopy);
    [-0.35, 1.55].forEach(x => { const p = cyl(0.06, 0.06, 1.05, M.metal()); p.position.set(x, 0.52, 2.25); g.add(p); });
    const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.62, 0.18, 48), M.white()); disc.rotation.x = Math.PI / 2; disc.position.set(-1, 2.55, 0.2); g.add(disc);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.07, 16, 64), M.blue()); ring.position.set(-1, 2.55, 0.29); g.add(ring);
    const h1 = rbox(0.08, 0.42, 0.06, 0.03, M.navy ? M.deep() : M.deep()); h1.position.set(-1, 2.68, 0.33); g.add(h1);
    const h2 = rbox(0.3, 0.08, 0.06, 0.03, M.deep()); h2.position.set(-0.88, 2.55, 0.33); g.add(h2);
    const st = rbox(0.18, 0.7, 0.18, 0.05, M.white()); st.position.set(-1, 2.2, 0.2); g.add(st);
    const cr = cross(0.6, 0.1, M.blue()); cr.position.set(1.05, 1.45, 1.22); g.add(cr);
    g.rotation.y = -0.45;
    return { group: g, cam: [1.2, 3.8, 8], look: [0, 1.2, 0.3], fov: 34, shadow: true };
  },
  ambulance() {
    const g = new THREE.Group();
    const box = rbox(2.6, 1.7, 1.8, 0.2, M.white()); box.position.set(-0.5, 1.15, 0); g.add(box);
    const cab = rbox(1.3, 1.25, 1.75, 0.25, M.white()); cab.position.set(1.4, 0.92, 0); g.add(cab);
    const ws = rbox(0.12, 0.55, 1.4, 0.06, M.glass()); ws.position.set(2.04, 1.2, 0); ws.rotation.z = -0.25; g.add(ws);
    const side = rbox(0.6, 0.45, 0.1, 0.05, M.glass()); side.position.set(1.4, 1.2, 0.88); g.add(side);
    const stripe = rbox(3.95, 0.22, 1.84, 0.05, M.blue()); stripe.position.set(0.15, 0.62, 0); g.add(stripe);
    const cr = cross(0.75, 0.08, M.blue()); cr.position.set(-0.5, 1.35, 0.92); g.add(cr);
    const light = rbox(0.7, 0.18, 0.5, 0.08, M.mist()); light.position.set(1.4, 1.65, 0); g.add(light);
    [[-1.2, 0.85], [-1.2, -0.85], [1.35, 0.85], [1.35, -0.85]].forEach(([x, z]) => {
      const w = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.14, 20, 40), M.deep()); w.position.set(x, 0.35, z); g.add(w);
      const hub = cyl(0.2, 0.2, 0.2, M.metal()); hub.rotation.x = Math.PI / 2; hub.position.set(x, 0.35, z); g.add(hub);
    });
    g.rotation.y = -0.5;
    return { group: g, cam: [1.4, 3.4, 7.2], look: [0, 0.9, 0], fov: 34, shadow: true };
  },
  shield() {
    const g = new THREE.Group();
    const s = new THREE.Shape();
    s.moveTo(0, 1.6); s.bezierCurveTo(0.7, 1.25, 1.2, 1.25, 1.35, 1.2); s.lineTo(1.35, 0.2);
    s.bezierCurveTo(1.35, -0.9, 0.6, -1.5, 0, -1.8); s.bezierCurveTo(-0.6, -1.5, -1.35, -0.9, -1.35, 0.2);
    s.lineTo(-1.35, 1.2); s.bezierCurveTo(-1.2, 1.25, -0.7, 1.25, 0, 1.6);
    const geo = new THREE.ExtrudeGeometry(s, { depth: 0.45, bevelEnabled: true, bevelSize: 0.12, bevelThickness: 0.12, bevelSegments: 8, curveSegments: 32 }); geo.center();
    const sh = new THREE.Mesh(geo, M.blue()); g.add(sh);
    const check = new THREE.CatmullRomCurve3([new THREE.Vector3(-0.6, 0.05, 0), new THREE.Vector3(-0.15, -0.4, 0), new THREE.Vector3(0.7, 0.55, 0)], false, 'catmullrom', 0);
    const cm = new THREE.Mesh(new THREE.TubeGeometry(check, 60, 0.15, 20), M.white()); cm.position.z = 0.4; g.add(cm);
    g.rotation.set(-0.15, 0.4, 0); g.position.y = 1.9;
    return { group: g, cam: [0, 2.6, 6], look: [0, 1.8, 0], fov: 34, shadow: true };
  },
  team() {
    // equipe: três "pessoas" estilizadas com crachá azul
    const g = new THREE.Group();
    [[-1.3, 0.85, M.mist()], [1.3, 0.85, M.mist()], [0, 1, M.blue()]].forEach(([x, s, coat], i) => {
      const p = new THREE.Group();
      const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.62, 0.9, 12, 32), M.white()); body.position.y = 0.95; p.add(body);
      const head = sph(0.5, mat(0xF2D7C4)); head.position.y = 2.25; p.add(head);
      const band = rbox(0.5, 0.5, 0.1, 0.08, coat); band.position.set(0.18, 1.25, 0.6); p.add(band);
      const cr = cross(0.28, 0.05, M.white()); cr.position.set(0.18, 1.25, 0.67); p.add(cr);
      const neck = new THREE.Mesh(new THREE.TorusGeometry(0.38, 0.06, 12, 40, Math.PI), M.blue()); neck.position.set(0, 1.55, 0.22); neck.rotation.set(0.3, 0, Math.PI); p.add(neck);
      p.position.set(x, 0, i === 2 ? 0.5 : -0.3); p.scale.setScalar(s); g.add(p);
    });
    return { group: g, cam: [0, 3.2, 7.4], look: [0, 1.2, 0], fov: 34, shadow: true };
  },
};

export async function render(name, ctx, { width = 1200, height = 900 } = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(width, height);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x000000, 0);
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

  const spec = BUILD[name](ctx);
  spec.group.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  scene.add(spec.group);

  const hemi = new THREE.HemisphereLight(0xffffff, 0xBFD6E6, 0.6); scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffffff, 1.6); key.position.set(-6, 12, 8); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 8; key.shadow.bias = -0.0004;
  Object.assign(key.shadow.camera, { left: -10, right: 10, top: 10, bottom: -10, near: 1, far: 40 });
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xDCEBF5, 0.5); fill.position.set(8, 4, -4); scene.add(fill);

  // sombra macia no chão transparente
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.ShadowMaterial({ color: 0x0D1B36, opacity: 0.16 }));
  ground.rotation.x = -Math.PI / 2; ground.position.y = -0.001; ground.receiveShadow = true; scene.add(ground);

  const cam = new THREE.PerspectiveCamera(spec.fov, width / height, 0.1, 200);
  cam.position.set(...spec.cam); cam.lookAt(...spec.look);
  renderer.render(scene, cam);
  return renderer.domElement.toDataURL('image/png');
}
