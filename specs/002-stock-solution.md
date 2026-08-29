# 002 — Solução Estoque

## Objetivo

Calcular a massa de pó necessária para preparar um volume final de solução
estoque com uma concentração-alvo, considerando a fração ativa informada para
o material.

## Classificação científica

**DERIVED** — o cálculo decorre do balanço de massa entre a quantidade ativa
necessária na solução e a fração ativa presente no pó.

## Equação implementada

**Identificador:** `EQ-STOCK-001`

```text
M_pó = (C_alvo × V_final) / P
```

Onde:

| Símbolo | Significado | Tipo dimensional |
| --- | --- | --- |
| `M_pó` | massa de pó a pesar | `Mass` |
| `C_alvo` | concentração ativa desejada na solução estoque | `Concentration` |
| `V_final` | volume final total da solução estoque | `Volume` |
| `P` | fração mássica ativa do material, entre 0 e 1 | `Potency` |

## Derivação

A massa ativa necessária na solução é `M_ativa = C_alvo × V_final`. Se cada
unidade de massa do pó contém a fração ativa `P`, então `M_ativa = M_pó × P`.
Isolando `M_pó`, obtém-se `M_pó = (C_alvo × V_final) / P`.

## Premissas e limitações

1. A concentração-alvo é expressa na mesma base de massa do material ativo.
2. `P` representa exclusivamente a fração de material ativo, e não substitui
   a análise documental do lote, do sal ou da base de potência do fornecedor.
3. A massa retornada é teórica; legibilidade de balança, solubilidade, solvente
   e estabilidade não são avaliados nesta etapa.
4. A ausência de uma potência válida deve interromper o cálculo. O software não
   deve assumir automaticamente `P = 1`.

## Modelo de potência

`Potency` é uma quantidade adimensional representada por `Decimal` no intervalo
aberto-fechado `(0, 1]`. Por exemplo, uma fração ativa de `0,80` representa 80%
de material ativo. A conversão de valores fornecidos em outras bases de potência
será especificada futuramente, quando os dados de entrada do fornecedor forem
definidos.

## Validações

- Concentração-alvo e volume final devem ser maiores que zero.
- A potência é obrigatória e deve ser um objeto `Potency` válido.
- Entradas sem unidade não são aceitas para concentração, volume ou massa.

## Exemplos analíticos

```text
C_alvo = 1000 µg/mL
V_final = 1 mL
P = 0,80

M_pó = (1000 µg/mL × 1 mL) / 0,80 = 1250 µg
```

```text
C_alvo = 2 mg/mL
V_final = 0,5 mL
P = 0,50

M_pó = (2 mg/mL × 0,5 mL) / 0,50 = 2 mg
```

## Critérios de aceitação

- Os exemplos analíticos produzem `1250 µg` e `2 mg`, respectivamente.
- A ausência de potência resulta em erro explícito.
- Unidades mistas são normalizadas sem arredondamento interno.
- A massa retornada pode ser convertida pelas unidades do modelo dimensional.

