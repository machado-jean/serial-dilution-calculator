# 007 — Série de Diluição

## Objetivo

Gerar uma sequência matemática de concentrações a partir de uma concentração
inicial e de um fator de diluição configurável.

## Classificação científica

**DERIVED** — a concentração de cada posição é obtida por aplicações sucessivas
do fator de diluição. Esta especificação descreve a matemática da série, não o
procedimento físico de transferência entre recipientes.

## Equação implementada

**Identificador:** `EQ-SER-001`

```text
Cₙ = C₀ / fatorⁿ
```

Onde:

| Símbolo | Significado | Tipo dimensional |
| --- | --- | --- |
| `C₀` | concentração inicial, no índice `0` | `Concentration` |
| `Cₙ` | concentração no índice `n` | `Concentration` |
| `fator` | divisor aplicado por etapa, maior que `1` | `DilutionFactor` |
| `n` | índice inteiro da série, iniciado em `0` | inteiro |

## Modelo de fator

`DilutionFactor` é uma quantidade adimensional representada por `Decimal` e
deve ser estritamente maior que `1`. O valor `2` representa uma série de duas
dobras. O programa não fixa esse valor como padrão científico.

## Definição de tamanho

`number_of_concentrations` representa a quantidade total de concentrações
retornadas, incluindo `C₀`. Portanto, o valor `4` retorna os índices `0`, `1`,
`2` e `3`.

## Premissas e limitações

1. A concentração inicial deve ser maior que zero.
2. Não há arredondamento interno.
3. A série não modela volumes de transferência, descarte, mistura, controles,
   poços ou conformidade com procedimento de referência.
4. A relação entre uma posição da série e uma coluna de placa será definida na
   especificação do modelo de placa.

## Exemplo analítico

```text
C₀ = 64 µg/mL
fator = 2
quantidade = 4

(C₀, C₁, C₂, C₃) = (64, 32, 16, 8) µg/mL
```

