// Menu do celular, cabeçalho ao rolar, entradas e o traço que se desenha. Sem dependências.
const toggle = document.querySelector('.menu-toggle');
const nav = document.getElementById('menu-principal');
const compact = matchMedia('(max-width: 1020px)');

if (toggle && nav) {
  let open = false;
  const setOpen = (value, restoreFocus = false) => {
    if (open === value) return;
    open = value;
    toggle.setAttribute('aria-expanded', String(value));
    toggle.setAttribute('aria-label', value ? 'Fechar menu' : 'Abrir menu');
    nav.classList.toggle('is-open', value);
    document.documentElement.classList.toggle('menu-open', value);
    if (value) nav.querySelector('a[href]')?.focus();
    else if (restoreFocus) toggle.focus();
  };
  toggle.addEventListener('click', () => setOpen(!open, true));
  nav.addEventListener('click', e => { if (e.target.closest('a[href]')) setOpen(false); });
  document.addEventListener('keydown', e => {
    if (!open) return;
    if (e.key === 'Escape') { e.preventDefault(); setOpen(false, true); return; }
    if (e.key !== 'Tab') return;
    const items = [toggle, ...nav.querySelectorAll('a[href]')];
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  compact.addEventListener('change', () => { if (!compact.matches) setOpen(false); });
  addEventListener('pageshow', () => setOpen(false));
}

// Sombra no cabeçalho depois de rolar.
let ticking = false;
const onScroll = () => {
  ticking = false;
  document.documentElement.classList.toggle('header-scrolled', scrollY > 8);
};
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
onScroll();

// Entradas (.reveal) e desenhos do traço ([data-draw], .steps) quando entram na tela.
const reveal = el => el.classList.add(el.matches('.reveal') ? 'is-in' : 'is-drawn');
const targets = document.querySelectorAll('.reveal, [data-draw], .steps');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      reveal(entry.target);
      io.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.15 });
  targets.forEach(el => io.observe(el));
} else {
  targets.forEach(reveal);
}

// Ano no rodapé.
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
