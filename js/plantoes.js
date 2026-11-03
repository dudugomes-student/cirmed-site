// Busca de plantões: filtra os cartões já presentes na página (sem servidor, sem guardar nada).
const form = document.querySelector('[data-filters]');
const list = document.querySelector('[data-units]');
if (form && list) {
  const units = [...list.querySelectorAll('.unit')];
  const count = document.querySelector('[data-count]');
  const empty = document.querySelector('[data-empty]');
  const norm = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
  const WA = 'https://wa.me/5511951531000?text=';

  // Filtros vindos do endereço (ex.: plantoes.html?esp=Pediatria ou ?q=bauru)
  const params = new URLSearchParams(location.search);
  if (params.get('q')) form.q.value = params.get('q');
  if (params.get('uf')) form.uf.value = params.get('uf').toUpperCase();
  if (params.get('esp')) {
    const wanted = norm(params.get('esp'));
    const opt = [...form.esp.options].find(o => norm(o.value) === wanted);
    if (opt) form.esp.value = opt.value; else form.q.value = params.get('esp');
  }

  const apply = () => {
    const words = norm(form.q.value).split(/\s+/).filter(Boolean);
    const uf = form.uf.value;
    const esp = form.esp.value;
    const tipo = form.querySelector('input[name=tipo]:checked')?.value || '';
    let shown = 0;
    units.forEach(card => {
      const esps = card.dataset.esps.split('|');
      const ok = (!uf || card.dataset.uf === uf) && (!tipo || card.dataset.tipo === tipo) &&
        (!esp || esps.includes(esp)) && words.every(w => card.dataset.busca.includes(w));
      card.hidden = !ok;
      if (!ok) return;
      shown++;
      // Destaca a especialidade buscada e já leva ela na mensagem do WhatsApp.
      const hit = esp || esps.find(e => words.length && words.some(w => norm(e).includes(w))) || '';
      card.querySelectorAll('[data-esp]').forEach(li => li.classList.toggle('is-hit', li.dataset.esp === hit));
      const what = hit ? `de ${hit} ` : '';
      card.querySelector('.unit-cta').href = WA + encodeURIComponent(`Olá, Cirmed. Tenho interesse no plantão ${what}em ${card.dataset.nome} (${card.dataset.lugar}).`);
    });
    count.textContent = shown === 1 ? '1 unidade' : `${shown} unidades`;
    empty.hidden = shown > 0;
    const filtered = Boolean(form.q.value.trim() || uf || esp || tipo);
    const top = document.querySelector('.results-bar [data-clear]'); if (top) top.hidden = !filtered;
    // Mantém o endereço compartilhável com os filtros atuais.
    const p = new URLSearchParams();
    if (form.q.value.trim()) p.set('q', form.q.value.trim());
    if (uf) p.set('uf', uf);
    if (esp) p.set('esp', esp);
    history.replaceState(null, '', p.toString() ? `?${p}` : location.pathname);
  };

  // Limpar filtros (barra de resultados e estado vazio)
  const clears = document.querySelectorAll('[data-clear]');
  clears.forEach(b => b.addEventListener('click', () => {
    form.reset(); apply(); form.q.focus();
  }));
  form.addEventListener('input', apply);
  form.addEventListener('change', apply);
  apply();
}
