# Validação

Exemplos analíticos, verificações independentes e casos de regressão serão registrados aqui.

## UNIT-AN-001 — Identidade de concentração

**Resultado conhecido:** `1 µg/mL = 1 mg/L`

**Classificação:** conversão dimensional DERIVED

**Teste automatizado:** `tests/analytical/test_unit_conversions.py`

Este caso valida as duas representações de concentração suportadas que têm a
mesma razão massa por volume. Ele não valida um procedimento de diluição.

## DIL-AN-001 — Concentração após diluição conhecida

**Resultado conhecido:** `1000 µg/mL × 20 µL / 200 µL = 100 µg/mL`

**Classificação:** operação DERIVED, `EQ-DIL-001`

**Teste automatizado:** `tests/analytical/test_dilution.py` e
`tests/unit/test_dilution_validation.py`

Este caso valida a implementação da equação de diluição para volumes em uma
mesma unidade. Ele não avalia precisão de pipetagem ou procedimentos de ensaio.

## STOCK-AN-001 — Massa de pó corrigida por fração ativa

**Resultado conhecido:** `1000 µg/mL × 1 mL / 0,80 = 1250 µg`

**Classificação:** operação DERIVED, `EQ-STOCK-001`

**Teste automatizado:** `tests/analytical/test_stock_solution.py`

Este caso valida o balanço de massa com uma fração ativa conhecida. Ele não
valida a interpretação documental de potenciais expressos em outras bases.
