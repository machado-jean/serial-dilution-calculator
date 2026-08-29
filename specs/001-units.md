# 001 — Unidades Dimensionais

## Objetivo

Disponibilizar quantidades físicas imutáveis e explicitamente tipadas para
massa, volume e concentração. Esta especificação é a base obrigatória para
qualquer cálculo científico posterior.

## Classificação científica

As conversões desta especificação são **DERIVED** a partir das definições dos
prefixos SI e das unidades de concentração selecionadas pelo projeto. Não há
uma equação de preparo, diluição ou protocolo nesta etapa.

## Escopo

### Massa

- micrograma (`µg`)
- miligrama (`mg`)
- grama (`g`)

Relações de conversão:

- `1 g = 1 000 mg`
- `1 mg = 1 000 µg`

### Volume

- microlitro (`µL`)
- mililitro (`mL`)
- litro (`L`)

Relações de conversão:

- `1 L = 1 000 mL`
- `1 mL = 1 000 µL`

### Concentração de massa por volume

- micrograma por mililitro (`µg/mL`)
- miligrama por mililitro (`mg/mL`)
- miligrama por litro (`mg/L`)

Relações de conversão:

- `1 mg/mL = 1 000 µg/mL`
- `1 µg/mL = 1 mg/L`

## Requisitos de implementação

1. Toda quantidade deve guardar um `Decimal` e uma unidade pertencente à sua
   dimensão.
2. A API científica não deve aceitar `float`, `int` ou `str` como valor de
   quantidade; o chamador deve fornecer `Decimal`.
3. Valores negativos devem gerar erro explícito.
4. Conversões não devem arredondar valores internamente.
5. Um objeto de uma dimensão não pode ser usado como se fosse outra dimensão.
6. Não implementar nesta etapa operações de preparo, diluição ou adição de
   quantidades.

## Limitações

- Somente as unidades listadas acima são suportadas.
- Zero é uma quantidade dimensional válida; operações futuras decidirão se
  zero é admissível para cada cálculo específico.
- Regras de arredondamento e incerteza metrológica estão fora do escopo.

## Critérios de aceitação

- Conversões de massa, volume e concentração são cobertas por testes.
- A equivalência `1 µg/mL = 1 mg/L` possui teste analítico explícito.
- `float`, valores negativos e unidades incompatíveis produzem erros claros.
- A suíte de testes roda sem dependências científicas de terceiros.

