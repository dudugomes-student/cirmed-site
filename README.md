# Site da Cirmed

Site estático (HTML, CSS e JavaScript, sem dependências no navegador) da CIRMED Serviços Médicos LTDA, publicado pelo GitHub Pages.

## Páginas

| Arquivo | Conteúdo |
| --- | --- |
| `index.html` | Início: as duas portas, números, busca rápida de plantões, serviços, integridade |
| `plantoes.html` | Busca de plantões (texto, estado, especialidade, tipo de unidade) e cadastro de médicos |
| `para-hospitais.html` | Montar equipe: escolhe especialidades e turnos e envia o pedido; serviços e etapas |
| `para-medicos.html` | Redireciona para `plantoes.html` |
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

## Plantões abertos

Lista em `tools/plantoes.json`, tirada da página Vagas Médicas do site antigo (63 unidades). Cada item: `[unidade, cidade, UF, tipo, [especialidades]]`, com tipo `hospital`, `ubs` ou `upa`. Para abrir ou fechar um plantão, edite o arquivo e rode `python3 build.py`. Os números da página inicial (unidades, estados, especialidades) saem daí.

## Ilustrações 3D

Ícones 3D desenhados do Fluent Emoji, da Microsoft (licença MIT, ver `assets/3d/LICENSE.txt`), em `assets/3d/*.webp`. Os que tinham vermelho ou rosa foram recoloridos para o azul da marca com `tools/recolor.py`. Só o logo não é 3D.

## Movimento

`js/motion.js`: transição entre páginas (cortina azul com o logo), títulos que sobem palavra por palavra, números que contam, ícones que flutuam e seguem o mouse e a rolagem, cartões que inclinam com brilho, botões magnéticos, barra de progresso da rolagem e entrada em cascata dos resultados da busca. A órbita da página inicial e a faixa de especialidades são CSS. `js/paths-bg.js` faz as curvas do fundo. Com "reduzir movimento" ligado no sistema, tudo fica parado.

## Visual

Ver `DESIGN.md`. Contorno do Brasil gerado de dados reais (world-atlas, Natural Earth) por `tools/brasil.cjs`, salvo em `tools/brasil.json`.

## Pendências antes do domínio oficial

- Nome e CRM do diretor técnico (exigência da Resolução CFM 2.336/2023 para publicidade de empresa médica). Entram no rodapé.
- Confirmar os WhatsApps: instituições em (11) 99124-3655 e plantões em (11) 95153-1000 (o número do "Quero Plantão" do site antigo).
- Confirmar que as unidades podem continuar aparecendo pelo nome (o site antigo já as lista) e manter `tools/plantoes.json` atualizado.
- Confirmar o texto do serviço "Terceirização da escala" (monta a escala, acompanha as trocas e repõe quem não pode ir).
- Revisão jurídica da política de privacidade.
