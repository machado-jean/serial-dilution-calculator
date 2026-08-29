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

## LAB-AN-001 — Avaliação de volume no limite mínimo

**Resultado conhecido:** com mínimo confiável de `20 µL`, uma transferência de
`20 µL` é aceita com o estado `CAUTION`.

**Classificação:** LAB-CONSTRAINT

**Teste automatizado:** `tests/unit/test_pipette_constraints.py`

Este caso valida a interpretação da configuração laboratorial. Ele não afirma
que `20 µL` seja um limite científico universal.

## INT-AN-001 — Intermediária para transferência direta inviável

**Resultado conhecido:** uma origem de `10000 µg/mL` para alvo de `100 µg/mL`
em `200 µL`, com mínimo de `20 µL`, requer intermediária de `1000 µg/mL` e
volume de `200 µL`.

**Classificação:** `EQ-DIL-002` é DERIVED; a regra de uma etapa é EXPERIMENTAL;
o mínimo de `20 µL` é LAB-CONSTRAINT.

**Teste automatizado:** `tests/analytical/test_intermediate_solution.py`

Este caso valida a regra determinística proposta, não um procedimento
laboratorial normativo completo.

## INOC-AN-001 — Concentração após inoculação de igual volume

**Resultado conhecido:** `8 µg/mL × 100 µL / (100 µL + 100 µL) = 4 µg/mL`

**Classificação:** operação DERIVED, `EQ-INOC-001`

**Teste automatizado:** `tests/analytical/test_inoculation.py`

Este caso valida a conservação de massa para os volumes fornecidos. A redução
por dois é consequência de volumes iguais, não uma regra fixa do programa.

## SER-AN-001 — Série de duas dobras conhecida

**Resultado conhecido:** concentração inicial `64 µg/mL`, fator `2`, quatro
posições → `64`, `32`, `16`, `8 µg/mL`.

**Classificação:** operação DERIVED, `EQ-SER-001`

**Teste automatizado:** `tests/analytical/test_serial_dilution.py`

Este caso valida a sequência matemática. Ele não representa por si só um
procedimento de diluição seriada em placa.
