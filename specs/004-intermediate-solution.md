# 004 — Planejamento de Solução Intermediária

## Objetivo

Determinar uma preparação intermediária de uma etapa quando a transferência
direta para uma solução-alvo fica abaixo do volume mínimo confiável configurado
pelo laboratório.

## Classificação científica

- `EQ-DIL-002`: **DERIVED**, por rearranjo de `C₁ × V₁ = C₂ × V₂`.
- Critérios de aceitação de volume: **LAB-CONSTRAINT**, definidos por
  `PipetteConstraint`.
- Regra de escolha de uma única etapa: **EXPERIMENTAL**. Ela é determinística e
  transparente, mas não é apresentada como procedimento normativo otimizado.

## Equação de volume de origem

**Identificador:** `EQ-DIL-002`

```text
V₁ = (C₂ × V₂) / C₁
```

Onde `C₁` é a concentração de origem, `C₂` a concentração-alvo e `V₂` o volume
final total desejado. A equação é válida para uma diluição quando `C₁ ≥ C₂`.

## Regra determinística de uma etapa intermediária

Se a transferência direta calculada por `EQ-DIL-002` estiver abaixo do mínimo
confiável `V_min`, o planejador define:

```text
C_intermediária = (C_alvo × V_final) / V_min
V_intermediária = (V_min × C_origem) / C_intermediária
```

Consequências diretas:

- a transferência da solução intermediária para a solução final é `V_min`;
- a transferência da solução de origem para preparar a intermediária também é
  `V_min`;
- o volume de diluente de cada preparo é a diferença entre o volume total e a
  alíquota transferida.

## Premissas e limites

1. A concentração de origem deve ser maior que a concentração-alvo quando uma
   etapa intermediária for necessária.
2. O volume final inclui a alíquota antimicrobiana transferida.
3. A regra só tenta uma etapa intermediária e não otimiza consumo, recipiente,
   resolução de pipeta ou múltiplas pipetas.
4. Se a transferência direta exceder o máximo configurado, a regra não propõe
   automaticamente uma solução intermediária; essa situação requer uma
   estratégia diferente.
5. Volumes e concentrações são normalizados internamente sem arredondamento.

## Exemplo analítico

```text
C_origem = 10000 µg/mL
C_alvo = 100 µg/mL
V_final = 200 µL
V_min = 20 µL

V_direto = (100 × 200) / 10000 = 2 µL  → inválido
C_intermediária = (100 × 200) / 20 = 1000 µg/mL
V_intermediária = (20 × 10000) / 1000 = 200 µL
```

Assim, preparar `200 µL` a `1000 µg/mL` com `20 µL` de origem e `180 µL` de
diluente permite transferir `20 µL` da intermediária para o preparo final.

