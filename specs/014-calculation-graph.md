# 014 — Grafo de Cálculo

## Classificação

**ARQUITETURAL** — o grafo não cria uma nova regra científica; ele registra a
origem, as entradas e os resultados de operações já validadas.

## Modelo

Cada `CalculationStep` contém identificador de operação, classificação,
identificador de equação quando aplicável, entradas formatadas, resultado
formatado e avisos. `CalculationGraph` preserva a ordem dos passos e é imutável.

Camadas de relatório recebem um grafo pronto e não podem recalcular valores.

