# 012 — Configuração de Protocolo de Microdiluição

## Classificação

**LAB-CONSTRAINT** — volumes e nome do protocolo são parâmetros do laboratório,
não constantes científicas universais.

## Modelo

`SerialPlateProtocol` contém o volume de solução antimicrobiana e o volume de
meio que preparam o primeiro poço, o volume inicial resultante, o volume de
meio pré-carregado nos poços seguintes, o volume de transferência seriada e o
volume de inóculo.

Todos os volumes devem ser maiores que zero. O volume que permanece em cada
poço antes da inoculação é `volume inicial - transferência`; ele deve ser igual
ao volume de meio pré-carregado nos poços seguintes para que a série seja
volumetricamente consistente.

## Preset inicial

O preset `Default Laboratory Serial Plate` é disponibilizado explicitamente com
`20 µL` de solução antimicrobiana de trabalho + `180 µL` de meio no primeiro
poço (`200 µL` iniciais), `100 µL` de meio nos poços seguintes, transferência
de `100 µL` e `100 µL` de inóculo. Cada valor é editável; a soma dos dois
componentes iniciais deve permanecer igual ao volume inicial do primeiro poço.
Ele é uma conveniência editável, não uma regra científica.

Assim, o preparo `20 + 180 µL` integra o preset canônico atual da série física,
mas não é um valor embutido nas equações.
