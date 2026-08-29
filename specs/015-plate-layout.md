# 015 — Layout Linear de Série em Placa

## Classificação

**LAB-CONSTRAINT** — coluna inicial, quantidade de colunas e linha escolhida
são decisões de disposição experimental.

## Modelo

`SerialDilutionLayout` define coluna inicial e quantidade de colunas. O mapa
associa uma sequência de concentrações já calculada a poços de uma linha de
`Plate96`, em ordem crescente de coluna.

O layout não cria a série, não muda as concentrações e não pressupõe uso das 12
colunas. A sequência deve ter exatamente a quantidade configurada de posições
e caber fisicamente na placa.

No protocolo canônico, o primeiro poço recebe o volume inicial completo; os
poços seguintes são pré-carregados com meio. Após cada transferência, inclusive
no último poço com descarte, cada poço de teste deve conter o mesmo volume
pré-inoculação antes da adição de inóculo.
