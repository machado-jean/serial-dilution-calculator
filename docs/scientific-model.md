# Modelo Científico

A documentação de cada equação será adicionada antes da implementação do respectivo comportamento científico.

## Definições de conversão dimensional — v0.1

**Classificação:** DERIVED

O modelo dimensional inicial usa fatores exatos de conversão decimal definidos
pelos prefixos do SI. Essas definições permitem normalizar unidades, mas não
constituem uma equação de preparo de solução nem um protocolo laboratorial.

| Dimensão | Unidades suportadas | Relações exatas |
| --- | --- | --- |
| Massa | `µg`, `mg`, `g` | `1 g = 1 000 mg`; `1 mg = 1 000 µg` |
| Volume | `µL`, `mL`, `L` | `1 L = 1 000 mL`; `1 mL = 1 000 µL` |
| Concentração | `µg/mL`, `mg/mL`, `mg/L` | `1 mg/mL = 1 000 µg/mL`; `1 µg/mL = 1 mg/L` |

Todos os fatores são representados com `decimal.Decimal` e nenhum arredondamento
é aplicado durante a conversão. Consulte `specs/001-units.md` para escopo,
limitações e critérios de teste.

## EQ-DIL-001 — Concentração após diluição volumétrica

**Classificação:** DERIVED

```text
C₂ = (C₁ × V₁) / V₂
```

| Variável | Unidade dimensional | Significado |
| --- | --- | --- |
| `C₁` | concentração | concentração da solução de origem |
| `V₁` | volume | volume transferido da solução de origem |
| `V₂` | volume | volume final total, incluindo `V₁` |
| `C₂` | concentração | concentração calculada no volume final |

**Derivação:** pela conservação de massa do soluto, a quantidade de soluto da
alíquota transferida é igual à quantidade presente na solução final:
`C₁ × V₁ = C₂ × V₂`. Isolando `C₂`, obtém-se `C₂ = (C₁ × V₁) / V₂`.

**Premissas:** mistura homogênea, conservação do soluto, ausência de perdas ou
correções de potência e volume final total conhecido. A equação não define
viabilidade de pipetagem nem conformidade com um protocolo específico.

**Referência de base:** princípio fundamental de balanço de massa; relação de
diluição descrita como princípio geral no `AGENTS.md` do projeto.

**Exemplo e teste analítico:** `1000 µg/mL × 20 µL / 200 µL = 100 µg/mL`.
Ver `tests/analytical/test_dilution.py`.
