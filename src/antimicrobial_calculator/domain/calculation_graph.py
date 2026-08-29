"""Immutable traceability graph for already-calculated scientific results."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CalculationStep:
    operation_id: str
    classification: str
    equation_id: str | None
    inputs: tuple[str, ...]
    result: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CalculationGraph:
    steps: tuple[CalculationStep, ...] = ()

    def with_step(self, step: CalculationStep) -> "CalculationGraph":
        return CalculationGraph((*self.steps, step))
