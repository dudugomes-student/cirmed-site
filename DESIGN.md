# Design — Cirmed

Fonte da verdade: tokens em `css/cirmed.css` (`:root`).

## Ilustrações: só 3D
Ícones 3D desenhados (Fluent Emoji, Microsoft, MIT), com vermelho e rosa trocados pelo azul da marca. Só o logo não é 3D. Uso: órbita em volta do hospital na página inicial, grupos flutuantes nos topos internos, cartões de serviço, faixa de especialidades, tipo de unidade na busca, contato e integridade. Ícones de interface (setas, busca, WhatsApp) continuam em traço.

## Pouco texto
Cada seção tem um título curto e, no máximo, uma linha de apoio. O resto é imagem, número ou interação (busca de plantões, montar equipe).

## Mundo visual: a linha médica
Fundo branco que desce até o azul claro. O traço azul (degradê #8DBBD9 → #2475A3) sublinha a palavra-chave dos títulos e liga as etapas; as curvas do fundo seguem o mesmo traço.

## Cores (nada fora disto, sem vermelho)
| Token | Valor | Uso |
| --- | --- | --- |
| `--blue` | #2475A3 | traço, botões, destaques, palavra-chave |
| `--blue-deep` | #155E89 | hover, links e texto pequeno em azul |
| `--navy` | #0D1B36 | títulos e texto, chamada final |
| `--gray` | #5B5C70 | texto de apoio |
| `--sky` | #E6F1F8 | preenchimentos, fundo de seção, rodapé |
| `--mist` | #8DBBD9 | início do degradê do traço |

## Tipografia
Nunito auto-hospedada (600, 700, 800, 900). Títulos em 900 maiúsculas, palavra-chave em azul. Apoio em 600.

## Componentes
Botões em pílula (`.btn-primary`, `.btn-outline`, `.btn-white`), portas de público (`.door`), chips de especialidade (`.chips`, borda azul, alguns cheios), cartões de serviço (`.card`), etapas ligadas pelo traço (`.steps`), situações (`.situations`), selo de integridade (`.trust`), formulários que montam a mensagem do WhatsApp (`[data-whatsapp-form]`), barra fixa de contato no celular (`.mobile-bar`).

## Fundo
No topo de cada página e na chamada final: curvas finas em azul que fluem da esquerda para a direita (`js/paths-bg.js`), adaptadas do "Floating Paths" do 21st.dev (desenho do Background Paths da Kokonut UI, licença MIT), sem React. Cada curva fica fixa e bem suave; por cima, um trecho mais forte corre pelo traço, como um sinal. Sobre o texto à esquerda as curvas ficam mais fracas (máscara), e na chamada final usam o azul claro. Menos curvas no celular; pausa fora da tela; parado com movimento reduzido.

## Movimento
Transição de página com cortina azul e o logo; títulos palavra por palavra; contadores; ícones flutuando com paralaxe; órbita girando; faixa de especialidades correndo; cartões que inclinam; botões magnéticos com reflexo; barra de progresso. Tudo desliga com movimento reduzido.
O sublinhado se desenha com `stroke-dashoffset` quando entra na tela. Seções entram com `.reveal`. Com movimento reduzido, tudo aparece pronto.

## Textos
Sem slogans genéricos. Proibido: soluções estratégicas, inteligência operacional, otimizar, excelência, inovação, garantir, "o maior", "o melhor", "líder", números sem prova, nomes de hospitais ou parceiros sem autorização, fotos de banco de imagem e logos de terceiros.
