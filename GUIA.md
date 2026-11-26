# Guia de conteúdo — Instagram @anotajuros

Este guia orienta a criação diária automática. Siga à risca.

## O que é o Anota Juros
- Sistema (app web) de **gestão de empréstimos** para quem **já trabalha emprestando dinheiro**.
- Organiza clientes, empréstimos, juros, vencimentos, atrasos, pagamentos, parcelas, relatórios e **cobranças prontas pelo WhatsApp**. Funciona no celular e no computador.
- **Não fazemos empréstimos.** Toda peça e toda legenda deixam isso claro (rodapé da arte + linha na legenda).
- Site/cadastro: link na bio (https://edison-loans-hq.lovable.app).

## Promoções vigentes (só divulgar assim, como DUAS OPÇÕES — decisão do dono em 26/11/2026)
- Opção 1: teste grátis de 7 dias; depois, R$ 19,90 por mês.
- Opção 2: começar já, sem teste, com o 1º mês por R$ 9,90; depois, R$ 19,90 por mês.
- NUNCA escrever "7 dias grátis E 1º mês por R$ 9,90" como se fossem juntos: o sistema não junta as duas.
- Forma curta aprovada: "Teste 7 dias grátis ou comece já por R$ 9,90 no 1º mês".
Se o dono avisar que mudou, atualize aqui antes de usar.

## Público
Pessoas que emprestam dinheiro (pequenos credores, quem empresta para conhecidos/clientes) e hoje controlam no caderno, planilha ou de cabeça. Dores: esquecer vencimento, juros calculados errado, cobrança constrangedora, perder o controle de quem deve quanto.

## Regras obrigatórias
- Português correto, sem erros. Revise cada legenda e cada texto da arte.
- Nunca inventar depoimentos, números de clientes, resultados ou funcionalidades.
- Nunca prometer ganhos, aprovação de crédito ou "dinheiro fácil".
- Não usar termos como "agiota". Tom profissional, direto e respeitoso.
- Demonstrações do sistema: usar dados fictícios e indicar "dados de exemplo".
- Não repetir títulos ou artes dos últimos 14 dias (consultar registro/publicados.jsonl e fila/).
- Nunca alterar, apagar ou republicar posts antigos.

## Identidade visual (aprovada pelo dono em 26/11/2026)
- Fundo preto (#050505) com pauta de caderno discreta e margem verde (classes .pauta e .margem do modelos/base.css).
- Títulos grandes em branco (#F7F4EC), destaques em dourado (#F2C14E, classe .ouro), verde (#25D366) para confirmações e "grátis".
- Fonte: Inter Display (pesos 600–900). Logo oficial: modelos/anota-juros-logo.png.
- Rodapé em toda arte: "Não fazemos empréstimos. Somos um sistema de gestão."
- Feed: 1080×1350 (4:5). Story: 1080×1920 (9:16), com conteúdo importante entre y=250 e y=1650.
- Exemplos aprovados: modelos/exemplo-feed.html e modelos/exemplo-story.html.

## Grade diária (horário de Brasília)
| Horário | Tipo | Arquivo na fila |
|---|---|---|
| 08:00 | Feed | fila/AAAA-MM-DD/0800-feed.jpg + .json |
| 19:00 | Feed | fila/AAAA-MM-DD/1900-feed.jpg + .json |

2 posts no feed por dia, sem stories (decisão do dono em 26/11/2026): com poucos seguidores, stories quase não têm alcance; o feed fica no perfil, aparece em hashtags e no Explorar. Voltar a incluir stories quando o perfil passar de ~100 seguidores (avisar o dono). Os horários 13:00 e 16:00 continuam na automação, mas só publicam se houver peça.

## Temas para variar (rodízio)
Dores do caderno/planilha; funcionalidade específica (cobrança no WhatsApp, atrasos, juros mensal/semanal/diário, parcelado, Tabela Price, relatórios, recibos, Pix); passo a passo de uso; dúvidas frequentes (é seguro? funciona no celular? preciso instalar?); promoção vigente; dica de organização para quem empresta; bastidores/novidades do sistema (só o que for real).
Stories: enquete visual (sem figurinha), "você sabia?", contagem da promoção, chamada para o link da bio, prova visual de tela com dados de exemplo.

## Legendas do feed
Gancho na 1ª linha; 3–6 linhas de valor; chamada clara ("Toque no link da bio"); linha "⚠️ Não fazemos empréstimos..."; 8–12 hashtags relevantes em português (#anotajuros sempre).

## Aprendizado
Antes de criar, leia dados/metricas.json: repita formatos/temas com mais alcance, salvamentos e interações; reduza os de pior desempenho. Registre o raciocínio em dados/aprendizado.md (curto, datado).
