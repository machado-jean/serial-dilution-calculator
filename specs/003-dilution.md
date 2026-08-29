# 003 — Diluição Volumétrica

## Objetivo

Calcular a concentração final obtida ao transferir um volume de uma solução de
origem para um volume final total conhecido.

## Classificação científica

**DERIVED** — a operação decorre da conservação de massa do soluto durante uma
diluição, expressa pela equação `C₁ × V₁ = C₂ × V₂`.

## Equação implementada

**Identificador:** `EQ-DIL-001`

```text
C₂ = (C₁ × V₁) / V₂
```

Onde:

| Símbolo | Significado | Tipo dimensional |
| --- | --- | --- |
| `C₁` | concentração da solução de origem | `Concentration` |
| `V₁` | volume transferido da solução de origem | `Volume` |
| `V₂` | volume final total após o preparo | `Volume` |
| `C₂` | concentração final calculada | `Concentration` |

## Premissas e limitações

1. O soluto é conservado entre a transferência e o volume final.
2. O volume final `V₂` inclui o volume transferido `V₁`.
3. Não há correção de potência, degradação, adsorção, evaporação ou incerteza
   metrológica nesta operação.
4. A função modela o resultado matemático da diluição, não uma instrução
   laboratorial completa.
5. A viabilidade de pipetagem e o planejamento de soluções intermediárias são
   responsabilidades de etapas posteriores.

## Validações

- `V₁` deve ser maior que zero para representar uma transferência.
- `V₂` deve ser maior que zero para evitar divisão por zero.
- `V₁` não pode exceder `V₂`, pois isso não representa uma diluição para um
  volume final total.
- Entradas devem ser objetos `Concentration` e `Volume`; números sem unidade
  não são aceitos.

## Exemplo analítico

```text
C₁ = 1000 µg/mL
V₁ = 20 µL
V₂ = 200 µL

C₂ = (1000 × 20) / 200 = 100 µg/mL
```

## Critérios de aceitação

- O exemplo analítico produz `100 µg/mL`.
- Volumes em unidades diferentes são normalizados corretamente.
- O resultado mantém a unidade informada para `C₁`.
- Volumes inválidos e entradas sem dimensão geram erros explícitos.

