# Calculadora de Diluição Seriadas

Calculadora científica para preparo de soluções antimicrobianas, planejamento de microdiluição em caldo, séries de diluição, correção por inoculação, mapeamento de concentrações em placas e relatórios técnicos de cálculo.

O projeto prioriza rastreabilidade científica, unidades explícitas, aritmética baseada em `Decimal`, viabilidade laboratorial, reprodutibilidade e validação automatizada.

## Ambiente de desenvolvimento

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Nesta fase inicial, o núcleo científico não possui dependências de execução de terceiros. `pytest` é a única dependência de desenvolvimento.

## Estado atual

Núcleo científico em desenvolvimento: unidades, diluição, solução estoque,
restrições laboratoriais, intermediárias, inoculação, séries, placa, protocolo,
mapa e relatório técnico inicial.

Os requisitos científicos e as regras arquiteturais estão definidos em [AGENTS.md](AGENTS.md).
