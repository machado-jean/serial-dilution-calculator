# 005 — Restrições Laboratoriais de Pipetagem

## Objetivo

Representar limites operacionais configuráveis para avaliar se um volume de
transferência calculado é executável com o equipamento disponível.

## Classificação científica

**LAB-CONSTRAINT** — os limites de pipetagem são escolhas e capacidades do
laboratório; não são leis científicas nem requisitos universais de um método.

## Modelo

`PipetteConstraint` contém:

| Campo | Tipo | Significado |
| --- | --- | --- |
| `minimum_reliable_volume` | `Volume` | menor volume considerado confiável pelo laboratório |
| `maximum_volume` | `Volume | None` | capacidade máxima conhecida; `None` significa que ela não foi configurada |

O volume mínimo é obrigatório e deve ser maior que zero. O limite máximo é
opcional porque nem todos os laboratórios terão esse dado configurado na fase
inicial. Quando informado, ele deve ser maior ou igual ao mínimo confiável.

## Avaliação de transferência

A função recebe um `Volume` calculado e retorna um resultado explícito:

| Condição | Estado | Significado |
| --- | --- | --- |
| `V_transferência > V_mínimo` e dentro do máximo conhecido | `INFO` | transferência aceita pela configuração |
| `V_transferência = V_mínimo` | `CAUTION` | transferência aceita, com aviso de estar no limite confiável |
| `V_transferência < V_mínimo` | `INVALID` | transferência operacionalmente inválida; avaliar solução intermediária |
| `V_transferência > V_máximo` | `INVALID` | transferência excede a capacidade configurada |

Não há equação científica nesta etapa: o volume é calculado por outra operação
e somente avaliado contra parâmetros laboratoriais.

## Limitações

1. O estado `INFO` indica compatibilidade com a configuração fornecida, não
   validação metrológica universal.
2. `maximum_volume = None` não significa capacidade ilimitada; significa que
   o limite superior não foi configurado e, portanto, não foi avaliado.
3. A seleção automática de pipeta, resolução e incerteza pertencem a etapas
   futuras.

## Exemplos de aceitação

Com mínimo confiável de `20 µL` e máximo de `200 µL`:

- `25 µL` → `INFO`;
- `20 µL` → `CAUTION`;
- `19,9 µL` → `INVALID`, abaixo do mínimo;
- `201 µL` → `INVALID`, acima do máximo.

