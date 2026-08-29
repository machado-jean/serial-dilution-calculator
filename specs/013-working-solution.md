# 013 — Concentração de Solução de Trabalho

## Classificação

**DERIVED** — a concentração de trabalho é derivada da concentração necessária
antes da inoculação e dos volumes do protocolo configurado.

## Equação

**Identificador:** `EQ-WORK-001`

```text
C_trabalho = C_pre × V_pre / V_antimicrobiano
```

`V_pre` é a soma de volume antimicrobiano e volume de meio. A equação vem da
conservação de massa no preparo pré-inoculação: a massa adicionada por
`C_trabalho × V_antimicrobiano` é igual a `C_pre × V_pre`.

`C_pre` é obtida por `EQ-INOC-002` quando o alvo é concentração final após
inoculação. No preset canônico, a mistura de `20 µL` de solução de trabalho com
`180 µL` de meio prepara os `200 µL` iniciais no primeiro poço; portanto,
`EQ-WORK-001` é aplicada a essa etapa. Os três volumes são configuráveis.
