// O navegador só monta a mensagem. Nada é enviado nem guardado pelo site:
// a pessoa revisa o texto e envia pelo próprio WhatsApp.
const WHATSAPP = '5511991243655';
const clean = (value, limit = 200) => String(value ?? '')
  .normalize('NFC')
  .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
  .replace(/[ \t]+/g, ' ')
  .trim()
  .slice(0, limit);

const greetings = {
  hospital: 'Olá, Cirmed. Sou de uma instituição de saúde e preciso de médicos.',
  medico: 'Olá, Cirmed. Sou médico(a) e quero receber os plantões disponíveis.',
  geral: 'Olá, Cirmed. Gostaria de conversar.'
};

document.querySelectorAll('[data-whatsapp-form]').forEach(form => {
  const kind = form.dataset.whatsappForm;
  const result = form.querySelector('[data-form-result]');
  const link = result?.querySelector('a');
  const status = result?.querySelector('[role=status]');
  const submit = form.querySelector('button[type=submit]');
  if (!result || !link || !status || !submit) return;
  submit.disabled = false;

  form.addEventListener('input', () => { result.hidden = true; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    // Montar equipe: pelo menos uma especialidade.
    const firstPick = form.querySelector('.picks input');
    if (firstPick && !form.querySelector('.picks input:checked')) {
      firstPick.setCustomValidity('Escolha pelo menos uma especialidade.');
      firstPick.reportValidity();
      form.querySelector('.picks').addEventListener('change', () => firstPick.setCustomValidity(''), { once: true });
      return;
    }
    if (!form.reportValidity()) return;

    const lines = [greetings[kind] || greetings.geral, ''];
    // Cada campo com data-label vira uma linha; caixas marcadas do mesmo grupo viram uma lista.
    const groups = new Map();
    form.querySelectorAll('[data-label]').forEach(field => {
      const label = field.dataset.label;
      if (field.type === 'checkbox' || field.type === 'radio') {
        if (!field.checked) return;
        groups.set(label, [...(groups.get(label) || []), clean(field.value, 60)]);
        return;
      }
      const limit = field.tagName === 'TEXTAREA' ? 1200 : 160;
      const value = clean(field.value, limit);
      if (value) lines.push(`${label}: ${value}`);
    });
    groups.forEach((values, label) => lines.push(`${label}: ${values.join(', ')}`));

    // encodeURIComponent: espaço vira %20 (o WhatsApp não trata "+" como espaço em todos os aparelhos).
    link.href = `https://wa.me/${form.dataset.number || WHATSAPP}?text=${encodeURIComponent(lines.join('\n'))}`;
    result.hidden = false;
    status.textContent = 'Mensagem pronta. Confira o texto e envie no WhatsApp.';
    link.focus();
  });
});

// Montar equipe: mostra quantas especialidades foram escolhidas e onde a Cirmed já tem cada uma na escala.
document.querySelectorAll('[data-team]').forEach(form => {
  const big = form.querySelector('[data-team-count]');
  const text = form.querySelector('[data-team-text]');
  const update = changed => {
    const picked = [...form.querySelectorAll('.picks input:checked')];
    big.textContent = picked.length;
    if (!picked.length) { text.textContent = 'Escolha uma ou mais especialidades.'; return; }
    const last = changed && changed.checked ? changed : picked[picked.length - 1];
    const n = Number(last.dataset.units), ufs = Number(last.dataset.ufs);
    const where = n ? `${last.value} já está na escala de ${n} ${n === 1 ? 'unidade' : 'unidades'} da Cirmed, em ${ufs} ${ufs === 1 ? 'estado' : 'estados'}.` : `${last.value}: sob consulta.`;
    text.textContent = `${picked.length === 1 ? 'especialidade escolhida' : 'especialidades escolhidas'}. ${where}`;
  };
  form.querySelector('.picks').addEventListener('change', e => update(e.target));
  update();
});
