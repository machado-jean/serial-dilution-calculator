# 008 — Modelo Físico de Placa de 96 Poços

## Objetivo

Representar a geometria física de uma placa com 96 poços e endereçar cada poço
de forma inequívoca, sem atribuir concentração, antimicrobiano, controle ou
série de diluição.

## Classificação

**LAB-CONSTRAINT** — a geometria de placa disponível é uma característica do
equipamento e do protocolo do laboratório. Este modelo representa apenas a
placa física `Plate96` inicialmente suportada.

## Modelo

| Propriedade | Valor |
| --- | --- |
| Linhas | `A` a `H` (8 linhas) |
| Colunas | `1` a `12` (12 colunas) |
| Total | `96` poços |

`WellPosition` é uma posição física imutável, formada por uma linha e uma
coluna. A identificação legível de um poço concatena esses valores, como `A1`,
`B12` ou `H8`.

## Premissas e limites

1. `Plate96` não pressupõe que todos os poços estejam em uso.
2. `Plate96` não pressupõe que as 12 colunas pertençam à mesma série.
3. O modelo não atribui volumes, concentrações, controles ou replicatas.
4. Um layout experimental futuro fará o mapeamento entre uma série e posições
   físicas da placa.

## Critérios de aceitação

- A placa expõe exatamente 8 linhas, 12 colunas e 96 posições.
- `A1` e `H12` são posições válidas.
- Linhas e colunas fora do intervalo produzem erro explícito.
- A enumeração completa é ordenada por linha e, dentro da linha, por coluna.

