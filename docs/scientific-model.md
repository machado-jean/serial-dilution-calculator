# Modelo Científico

A documentação de cada equação será adicionada antes da implementação do respectivo comportamento científico.

## Definições de conversão dimensional — v0.1

**Classificação:** DERIVED

O modelo dimensional inicial usa fatores exatos de conversão decimal definidos
pelos prefixos do SI. Essas definições permitem normalizar unidades, mas não
constituem uma equação de preparo de solução nem um protocolo laboratorial.

| Dimensão | Unidades suportadas | Relações exatas |
| --- | --- | --- |
| Mass | `µg`, `mg`, `g` | `1 g = 1 000 mg`; `1 mg = 1 000 µg` |
| Volume | `µL`, `mL`, `L` | `1 L = 1 000 mL`; `1 mL = 1 000 µL` |
| Concentration | `µg/mL`, `mg/mL`, `mg/L` | `1 mg/mL = 1 000 µg/mL`; `1 µg/mL = 1 mg/L` |

Todos os fatores são representados com `decimal.Decimal` e nenhum arredondamento
é aplicado durante a conversão. Consulte `specs/001-units.md` para escopo,
limitações e critérios de teste.
