# Validação

Exemplos analíticos, verificações independentes e casos de regressão serão registrados aqui.

## UNIT-AN-001 — Concentration identity

**Resultado conhecido:** `1 µg/mL = 1 mg/L`

**Classificação:** conversão dimensional DERIVED

**Teste automatizado:** `tests/analytical/test_unit_conversions.py`

Este caso valida as duas representações de concentração suportadas que têm a
mesma razão massa por volume. Ele não valida um procedimento de diluição.
