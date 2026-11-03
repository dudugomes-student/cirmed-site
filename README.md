# Site da Cirmed

Site estático (HTML, CSS e JavaScript, sem dependências no navegador) da CIRMED Serviços Médicos LTDA, publicado pelo GitHub Pages.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Início: as duas portas (hospitais e médicos), serviços, especialidades, etapas, integridade |
| `para-hospitais.html` | Situações, serviços, etapas e o pedido que monta a mensagem do WhatsApp |
| `para-medicos.html` | Como funciona e o cadastro (CRM, UF, especialidade, estado, turnos) pelo WhatsApp |
| `sobre.html` | Quem é a Cirmed e os dados da empresa |
| `contato.html` | Canais e atalhos para os dois formulários |
| `programa-de-integridade.html` | Texto do programa, organizado em seções |
| `privacidade.html` | Política de privacidade deste site |
| `404.html` | Página não encontrada |

## Como editar

As páginas são geradas por `build.py` (cabeçalho, rodapé, traço do mapa e textos ficam lá). Edite o `build.py` e rode:

```bash
python3 build.py
```

Não edite os `.html` direto: o próximo build sobrescreve.

**Domínio próprio:** quando apontar o domínio para o GitHub Pages, troque `SITE_URL` no topo do `build.py`, rode o build e adicione o arquivo `CNAME` com o domínio. Canonical, og:url, og:image, sitemap e robots passam a usar o endereço novo.

**Contato:** número do WhatsApp em `build.py` (`WA_NUMBER`, `WA_SHOW`) e em `js/forms.js` (`WHATSAPP`).

## Visual

Ver `DESIGN.md`. Contorno do Brasil gerado de dados reais (world-atlas, Natural Earth) por `tools/brasil.cjs`, salvo em `tools/brasil.json`.

## Pendências antes do domínio oficial

- Nome e CRM do diretor técnico (exigência da Resolução CFM 2.336/2023 para publicidade de empresa médica). Entram no rodapé.
- Confirmar o WhatsApp oficial: o site usa (11) 99124-3655; o site antigo mostra 95153-1000, 94715-0484 e (11) 5197-8823.
- Confirmar o texto do serviço "Terceirização da escala" (monta a escala, acompanha as trocas e repõe quem não pode ir).
- Revisão jurídica da política de privacidade.
