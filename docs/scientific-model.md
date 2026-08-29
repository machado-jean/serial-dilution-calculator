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

## EQ-STOCK-001 — Massa de pó para solução estoque

**Classificação:** DERIVED

```text
M_pó = (C_alvo × V_final) / P
```

| Variável | Unidade dimensional | Significado |
| --- | --- | --- |
| `M_pó` | massa | massa teórica de pó a pesar |
| `C_alvo` | concentração | concentração ativa desejada |
| `V_final` | volume | volume final total da solução |
| `P` | fração adimensional | fração ativa declarada para o material |

**Derivação:** a massa ativa necessária é `M_ativa = C_alvo × V_final`. Com a
fração ativa `P`, a massa ativa presente no pó é `M_pó × P`. Logo,
`M_pó × P = C_alvo × V_final`; isolando `M_pó`, obtém-se a equação acima.

**Premissas:** concentração baseada em material ativo, mistura homogênea e
fração ativa documentada. Não há correção para solubilidade, estabilidade,
legibilidade de balança ou base de potência específica do fornecedor.

**Limitação de segurança:** potência ausente não é interpretada como 100%; o
cálculo é interrompido até que uma fração ativa válida seja fornecida.

**Exemplo e teste analítico:** `1000 µg/mL × 1 mL / 0,80 = 1250 µg`. Ver
`tests/analytical/test_stock_solution.py`.

## Restrições laboratoriais de pipetagem

**Classificação:** LAB-CONSTRAINT

O volume mínimo confiável e a capacidade máxima de uma pipeta não pertencem às
equações `EQ-DIL-001` ou `EQ-STOCK-001`. Eles são valores configuráveis usados
para avaliar a viabilidade operacional de um volume já calculado. A avaliação
produz os estados `INFO`, `CAUTION` ou `INVALID`; o estado no limite mínimo
gera aviso, enquanto volumes abaixo do mínimo ou acima do máximo configurado
são inválidos para aquela configuração.

Consulte `specs/005-lab-constraints.md` para o modelo, as limitações e os casos
de aceitação.

## EQ-DIL-002 — Volume de origem necessário para uma diluição

**Classificação:** DERIVED

```text
V₁ = (C₂ × V₂) / C₁
```

**Derivação:** partindo de `C₁ × V₁ = C₂ × V₂`, divide-se ambos os lados por
`C₁`, obtendo-se o volume de origem `V₁` necessário para alcançar a
concentração-alvo `C₂` no volume final `V₂`.

**Premissas:** conservação do soluto, mistura homogênea e `C₁ ≥ C₂`. A equação
não avalia a viabilidade de pipetagem; essa avaliação pertence às restrições
laboratoriais configuráveis.

**Uso no planejamento intermediário:** a regra experimental de uma única etapa
está documentada em `specs/004-intermediate-solution.md`. Ela usa
`EQ-DIL-002` e `PipetteConstraint`, sem alegar otimização ou conformidade
metodológica.

## EQ-INOC-001 e EQ-INOC-002 — Correção por inoculação

**Classificação:** DERIVED

```text
C_final = C_pre × V_pre / (V_pre + V_inóculo)
C_pre = C_final × (V_pre + V_inóculo) / V_pre
```

**Derivação:** a massa de antimicrobiano antes da inoculação é
`C_pre × V_pre`. Como o inóculo não contém antimicrobiano, essa massa se
distribui pelo volume total `V_pre + V_inóculo`, resultando em `EQ-INOC-001`.
O isolamento de `C_pre` resulta em `EQ-INOC-002`.

**Premissas:** inóculo isento de antimicrobiano, conservação do antimicrobiano
e aditividade de volumes. Não há uma hipótese de volumes iguais. A relação de
redução à metade somente ocorre quando os volumes fornecidos são iguais.

**Exemplo e teste analítico:** `8 µg/mL × 100 µL / (100 µL + 100 µL) =
4 µg/mL`. Ver `tests/analytical/test_inoculation.py`.

## EQ-SER-001 — Concentrações em série de diluição

**Classificação:** DERIVED

```text
Cₙ = C₀ / fatorⁿ
```

**Derivação:** cada etapa divide a concentração anterior pelo fator configurado.
Após `n` etapas, a divisão é aplicada `n` vezes, resultando em
`C₀ / fatorⁿ`.

**Premissas:** concentração inicial maior que zero, fator maior que um e índice
inteiro iniciado em zero. A equação gera uma série matemática; não especifica
volumes, transferências físicas, descarte ou disposição em placa.

**Exemplo e teste analítico:** `64 µg/mL` com fator `2` e quatro posições gera
`64`, `32`, `16` e `8 µg/mL`. Ver `tests/analytical/test_serial_dilution.py`.
