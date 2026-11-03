// Movimento do site: transição entre páginas, contadores, inclinação dos cartões,
// paralaxe dos ícones 3D, barra de progresso, botões magnéticos e títulos que sobem palavra por palavra.
// Tudo desliga com "reduzir movimento" do sistema.
(() => {
const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

/* ---------- Transição de página (cortina azul com o logo) ---------- */
const OUT_MS = 520;
function arrive() {
  if (!root.classList.contains('arriving')) return;
  requestAnimationFrame(() => requestAnimationFrame(() => {
    root.classList.add('arrived');
    setTimeout(() => root.classList.remove('arriving', 'arrived'), 900);
  }));
}
arrive();
addEventListener('pageshow', e => { if (e.persisted) root.classList.remove('leaving', 'arriving', 'arrived'); });

if (!reduce) {
  const sameSite = a => {
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return false;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/\.html$|\/$/.test(url.pathname)) return false;
    // âncora na mesma página: rola, sem cortina
    if (url.pathname === location.pathname && url.hash) return false;
    return url;
  };
  document.addEventListener('click', e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest('a[href]');
    const url = sameSite(a);
    if (!url) return;
    e.preventDefault();
    try { sessionStorage.setItem('cirmed-nav', '1'); } catch (_) {}
    root.classList.add('leaving');
    setTimeout(() => { location.href = url.href; }, OUT_MS);
  });
  // Pré-carrega a próxima página quando o mouse (ou o dedo) chega no link.
  const seen = new Set();
  const prefetch = e => {
    const url = sameSite(e.target.closest?.('a[href]'));
    if (!url || seen.has(url.pathname)) return;
    seen.add(url.pathname);
    const l = document.createElement('link'); l.rel = 'prefetch'; l.href = url.href; document.head.appendChild(l);
  };
  document.addEventListener('pointerover', prefetch, { passive: true });
  document.addEventListener('touchstart', prefetch, { passive: true });
}

/* ---------- Títulos: palavras sobem em sequência ---------- */
if (!reduce) {
  document.querySelectorAll('.display, .title').forEach(h => {
    let n = 0;
    const walk = node => {
      [...node.childNodes].forEach(child => {
        if (child.nodeType === 3) {
          const parts = child.textContent.split(/(\s+)/);
          const frag = document.createDocumentFragment();
          parts.forEach(p => {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            const w = document.createElement('span'); w.className = 'w';
            const i = document.createElement('span'); i.className = 'wi'; i.textContent = p;
            i.style.setProperty('--wd', `${(n++) * 0.06}s`);
            w.appendChild(i); frag.appendChild(w);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1 && !child.matches('svg')) walk(child);
      });
    };
    walk(h);
    h.classList.add('words');
  });
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('words-in'); io.unobserve(e.target); }
  }), { threshold: 0.2 });
  document.querySelectorAll('.words').forEach(h => io.observe(h));
}

/* ---------- Contadores ---------- */
const counters = document.querySelectorAll('[data-count-to]');
if (counters.length && !reduce) {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    io.unobserve(e.target);
    const el = e.target, to = Number(el.dataset.countTo), t0 = performance.now(), dur = 1400;
    const tick = t => {
      const k = Math.min(1, (t - t0) / dur), ease = 1 - Math.pow(1 - k, 4);
      el.textContent = Math.round(to * ease);
      if (k < 1) requestAnimationFrame(tick);
    };
    el.textContent = '0';
    requestAnimationFrame(tick);
  }), { threshold: 0.5 });
  counters.forEach(c => io.observe(c));
}

/* ---------- Barra de progresso da rolagem + paralaxe dos ícones ---------- */
const bar = document.querySelector('.progress');
const floats = [...document.querySelectorAll('[data-depth]')];
let mx = 0, my = 0, tx = 0, ty = 0, raf = 0;
const frame = () => {
  raf = 0;
  const max = root.scrollHeight - innerHeight;
  if (bar) bar.style.transform = `scaleX(${max > 0 ? scrollY / max : 0})`;
  root.classList.toggle('show-bar', scrollY > 380);
  if (reduce) return;
  tx += (mx - tx) * 0.08; ty += (my - ty) * 0.08;
  floats.forEach(el => {
    const d = Number(el.dataset.depth) || 0;
    const r = el.getBoundingClientRect();
    const fromCenter = (r.top + r.height / 2 - innerHeight / 2) / innerHeight; // -0.5 .. 0.5 na tela
    el.style.setProperty('--px', `${(tx * d * 40).toFixed(2)}px`);
    el.style.setProperty('--py', `${(ty * d * 30 - fromCenter * d * 80).toFixed(2)}px`);
  });
  if (Math.abs(mx - tx) > 0.001 || Math.abs(my - ty) > 0.001) queue();
};
const queue = () => { if (!raf) raf = requestAnimationFrame(frame); };
addEventListener('scroll', queue, { passive: true });
addEventListener('resize', queue);
if (fine && !reduce) addEventListener('pointermove', e => { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; queue(); }, { passive: true });
queue();

/* ---------- Cartões que inclinam e brilho que segue o mouse ---------- */
if (fine && !reduce) {
  document.querySelectorAll('[data-tilt]').forEach(card => {
    card.addEventListener('pointermove', e => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.style.setProperty('--rx', `${((0.5 - y) * 8).toFixed(2)}deg`);
      card.style.setProperty('--ry', `${((x - 0.5) * 10).toFixed(2)}deg`);
      card.style.setProperty('--gx', `${(x * 100).toFixed(1)}%`);
      card.style.setProperty('--gy', `${(y * 100).toFixed(1)}%`);
      card.classList.add('is-tilting');
    });
    card.addEventListener('pointerleave', () => {
      card.classList.remove('is-tilting');
      card.style.removeProperty('--rx'); card.style.removeProperty('--ry');
    });
  });

  /* ---------- Botões magnéticos ---------- */
  document.querySelectorAll('.btn').forEach(b => {
    b.addEventListener('pointermove', e => {
      const r = b.getBoundingClientRect();
      b.style.translate = `${((e.clientX - r.left) / r.width - 0.5) * 8}px ${((e.clientY - r.top) / r.height - 0.5) * 8}px`;
    });
    b.addEventListener('pointerleave', () => { b.style.translate = ''; });
  });
}

/* ---------- Busca: cartões entram em cascata quando os filtros mudam ---------- */
const units = document.querySelector('[data-units]');
if (units && !reduce) {
  new MutationObserver(() => {
    let i = 0;
    units.querySelectorAll('.unit:not([hidden])').forEach(u => {
      u.classList.remove('pop-in'); void u.offsetWidth;
      u.style.setProperty('--ud', `${Math.min(i++, 12) * 0.035}s`); u.classList.add('pop-in');
    });
  }).observe(units, { attributes: true, subtree: true, attributeFilter: ['hidden'] });
}
})();
