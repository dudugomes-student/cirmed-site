// Fundo de linhas que fluem: "Floating Paths" (21st.dev, por bundui; desenho do Background Paths da Kokonut UI, MIT),
// reescrito sem React nem framer-motion e nas cores da Cirmed.
// Duas camadas de curvas fixas e suaves; sobre cada uma, um trecho mais forte corre devagar pelo traço.
const NS = 'http://www.w3.org/2000/svg';
const reduce = matchMedia('(prefers-reduced-motion: reduce)');

function layer(position, count) {
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 696 316');
  svg.setAttribute('preserveAspectRatio', 'xMidYMid slice');
  svg.setAttribute('fill', 'none');
  const p = position;
  const anims = [];
  for (let i = 0; i < count; i++) {
    const path = document.createElementNS(NS, 'path');
    path.setAttribute('d',
      `M-${380 - i * 5 * p} -${189 + i * 6}C-${380 - i * 5 * p} -${189 + i * 6} -${312 - i * 5 * p} ${216 - i * 6} ${152 - i * 5 * p} ${343 - i * 6}` +
      `C${616 - i * 5 * p} ${470 - i * 6} ${684 - i * 5 * p} ${875 - i * 6} ${684 - i * 5 * p} ${875 - i * 6}`);
    path.setAttribute('stroke', 'currentColor');
    path.setAttribute('stroke-width', (0.6 + i * 0.03).toFixed(2));
    path.setAttribute('stroke-opacity', (0.08 + i * 0.012).toFixed(3));
    svg.appendChild(path);
    // Por cima da curva fixa, um trecho mais forte corre pelo traço, como um sinal.
    const pulse = path.cloneNode();
    pulse.setAttribute('stroke-width', (1 + i * 0.04).toFixed(2));
    pulse.setAttribute('stroke-opacity', (0.25 + i * 0.015).toFixed(3));
    pulse.setAttribute('pathLength', '1');
    pulse.setAttribute('stroke-linecap', 'round');
    pulse.setAttribute('stroke-dasharray', '0.18 0.82');
    pulse.setAttribute('stroke-dashoffset', String(Math.random()));
    svg.appendChild(pulse);
    if (!reduce.matches && pulse.animate) {
      const start = Math.random();
      anims.push(pulse.animate(
        [{ strokeDashoffset: start }, { strokeDashoffset: start - 1 }],
        { duration: 14000 + Math.random() * 12000, iterations: Infinity }
      ));
    }
  }
  return { svg, anims };
}

document.querySelectorAll('[data-paths]').forEach(box => {
  // Menos curvas em telas pequenas: mesmo desenho, menos trabalho para o celular.
  const count = matchMedia('(max-width: 760px)').matches ? 22 : 36;
  const layers = [layer(1, count), layer(-1, count)];
  layers.forEach(l => box.appendChild(l.svg));
  const anims = layers.flatMap(l => l.anims);
  if (!anims.length) return;
  // Pausa quando o fundo sai da tela ou a aba fica oculta.
  let visible = true;
  const sync = () => anims.forEach(a => (visible && !document.hidden ? a.play() : a.pause()));
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; sync(); }).observe(box);
  document.addEventListener('visibilitychange', sync);
});
