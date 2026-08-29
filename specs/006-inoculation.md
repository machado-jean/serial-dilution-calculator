# 006 — Correção por Inoculação

## Objetivo

Calcular a concentração após adicionar um inóculo sem antimicrobiano a uma
solução pré-inoculação e calcular, no sentido inverso, a concentração prévia
necessária para atingir uma concentração final desejada.

## Classificação científica

**DERIVED** — ambas as operações decorrem da conservação de massa do
antimicrobiano durante a adição de volume isento de antimicrobiano.

## Equações implementadas

**EQ-INOC-001 — concentração final após inoculação**

```text
C_final = C_pre × V_pre / (V_pre + V_inóculo)
```

**EQ-INOC-002 — concentração pré-inoculação requerida**

```text
C_pre = C_final × (V_pre + V_inóculo) / V_pre
```

| Símbolo | Significado | Tipo dimensional |
| --- | --- | --- |
| `C_pre` | concentração antes da inoculação | `Concentration` |
| `C_final` | concentração depois da inoculação | `Concentration` |
| `V_pre` | volume contendo antimicrobiano antes da inoculação | `Volume` |
| `V_inóculo` | volume de inóculo adicionado | `Volume` |

## Premissas e limitações

1. O inóculo adicionado não contém antimicrobiano na base de concentração
   modelada.
2. O volume final é a soma de `V_pre` e `V_inóculo`.
3. Não há perdas, evaporação, adsorção ou alteração de volume por mistura.
4. A concentração pré-inoculação e o volume pré-inoculação devem ser maiores
   que zero para a operação correspondente.
5. `V_inóculo = 0` é matematicamente aceito e conserva a concentração; não
   representa uma inoculação física efetuada.

## Caso especial

Quando `V_pre = V_inóculo`, a equação resulta em `C_final = C_pre / 2`.
Essa condição é derivada dos volumes fornecidos e nunca é codificada como regra
universal.

## Exemplos analíticos

```text
C_pre = 8 µg/mL
V_pre = 100 µL
V_inóculo = 100 µL

C_final = 8 × 100 / (100 + 100) = 4 µg/mL
```

```text
C_final = 4 µg/mL
V_pre = 100 µL
V_inóculo = 100 µL

C_pre = 4 × (100 + 100) / 100 = 8 µg/mL
```

