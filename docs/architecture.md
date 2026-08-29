# Arquitetura

A direção planejada de dependências é:

`domain / units → calculations → planning → reporting → ui`

As fórmulas científicas são implementadas na camada de cálculos, documentadas com identificadores de equação e testadas independentemente da interface de usuário.

O modelo físico de placa pertence a `plates/` e não conhece concentrações ou
layouts. A associação entre posições físicas e uma série experimental pertence
a uma camada de layout/protocolo posterior.
