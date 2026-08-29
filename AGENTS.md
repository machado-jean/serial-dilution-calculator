# AGENTS.md

## 1. Project Purpose

This project is a scientific calculation application for antimicrobial
solution preparation, broth microdilution planning, dilution series,
inoculation correction, plate concentration mapping, and laboratory
protocol generation.

The project MUST prioritize:

1. scientific traceability;
2. mathematical correctness;
3. laboratory feasibility;
4. reproducibility;
5. explicit units;
6. separation between normative rules and laboratory-specific choices;
7. testability;
8. explainability of every calculated result.

The initial target is a desktop scientific calculator written in Python.

The application MUST NOT behave as a generic "MIC calculator".

The scientific core must instead model the complete preparation chain:

Powder
→ Stock Solution
→ Intermediate Solution, if needed
→ Working Solution
→ Well Preparation
→ Dilution Series
→ Inoculation
→ Final Well Concentration
→ Plate Map
→ Technical / Scientific Report

MIC interpretation and MIC-position analysis are later layers built on
top of this calculation engine.


---

# 2. Fundamental Development Principle

Scientific correctness takes precedence over interface convenience.

No formula, protocol assumption, default value, or laboratory practice
may be embedded in the calculation engine without being explicitly
classified and documented.

Every scientific behavior MUST belong to one of the following classes:

## NORMATIVE

A rule or procedure directly supported by a published standard,
official guideline, or validated methodological reference.

Examples:

- antimicrobial potency correction;
- preparation principles described by ISO / CLSI;
- standardized dilution concepts;
- broth microdilution principles.

## DERIVED

A mathematical result derived from normative principles or fundamental
mass-balance mathematics.

Examples:

- C1 × V1 = C2 × V2;
- concentration correction after adding inoculum;
- calculation of required working concentration;
- calculation of dilution factors.

All DERIVED equations MUST include a documented derivation.

## LAB-CONSTRAINT

A laboratory-specific operational restriction.

Examples:

- minimum reliable pipetting volume;
- available pipette ranges;
- preferred working volumes;
- preferred plate arrangement;
- preferred stock volume.

LAB-CONSTRAINT values MUST NEVER be presented as universal scientific
requirements.

## EXPERIMENTAL

A method, model, hypothesis, optimization, or mathematical treatment
created for this project but not directly established by the adopted
references.

Examples:

- predicting which well should correspond to an expected MIC;
- optimized plate reuse;
- novel dilution planning algorithms;
- custom uncertainty strategies not yet validated.

EXPERIMENTAL functionality MUST remain clearly isolated from normative
calculations until independently validated.


---

# 3. Scientific Sources

The scientific model must be documented against authoritative sources.

Current project references include:

- ISO 20776-1:2019
- CLSI M100, 35th Edition, 2025
- CLSI M07-A10, 2015
- peer-reviewed anaerobic susceptibility literature

Important:

ISO 20776-1 and CLSI M07 primarily describe susceptibility testing for
rapidly growing aerobic bacteria.

They may support general dilution mathematics, solution preparation,
potency handling, broth microdilution concepts, and concentration
calculations.

They MUST NOT automatically be treated as organism-specific procedural
standards for Fusobacterium or anaerobic bacteria.

CLSI M100 references M11 as the dilution methodology for anaerobic
bacteria.

Therefore:

> Full claims of CLSI-compliant anaerobic susceptibility testing MUST NOT
> be made until the applicable current CLSI M11 methodology has been
> reviewed and incorporated.

The software may state that a calculation is based on dilution,
mass-balance, or microdilution principles described by a reference.

It MUST distinguish this from claiming that an entire laboratory assay
is performed "according to CLSI" or "according to ISO".


---

# 4. Scientific Traceability

Every implemented scientific equation MUST have a unique identifier.

Suggested format:

EQ-XXX-NNN

Examples:

EQ-DIL-001
EQ-STOCK-001
EQ-INOC-001
EQ-POT-001

Each equation MUST be documented in:

docs/scientific-model.md

The documentation for every equation SHOULD include:

- equation identifier;
- equation;
- variables;
- variable units;
- physical meaning;
- assumptions;
- derivation;
- applicable limitations;
- source classification;
- supporting reference;
- examples;
- test cases.


---

# 5. Core Mathematical Principles

## 5.1 Dilution Equation

The general volumetric dilution relationship is:

C1 × V1 = C2 × V2

Therefore:

V1 = (C2 × V2) / C1

C2 = (C1 × V1) / V2

All dilution calculations MUST use dimensional quantities.

Bare numerical values representing concentration, volume, mass, or
potency MUST NOT be passed through the scientific domain without units.


---

# 6. Units

The initial project SHOULD implement its own small dimensional model.

Do not initially depend on external unit libraries for the scientific
core.

Initial supported mass units:

- µg
- mg
- g

Initial supported volume units:

- µL
- mL
- L

Initial supported concentration units:

- µg/mL
- mg/mL
- mg/L

Important conversion:

1 µg/mL = 1 mg/L

Unit conversions MUST have dedicated automated tests.

The system MUST prevent invalid operations such as:

Mass + Volume

or:

Volume interpreted silently as Concentration.


---

# 7. Numeric Representation

Scientific calculations SHOULD use:

decimal.Decimal

instead of relying exclusively on binary floating-point arithmetic.

The engine MUST avoid premature rounding.

Internal calculations should preserve sufficient precision.

Rounding MUST occur only at defined presentation or operational
boundaries.

Examples:

- pipette resolution;
- balance resolution;
- displayed protocol;
- reported significant figures.

Rounding rules MUST eventually be documented.


---

# 8. Domain Model

The scientific core SHOULD include explicit domain concepts.

Initial concepts may include:

Mass
Volume
Concentration
Potency
DilutionFactor
StockSolution
IntermediateSolution
WorkingSolution
Inoculum
Well
Plate96
PipetteConstraint
ProtocolConfiguration
CalculationResult
CalculationStep
CalculationGraph

Values representing physical quantities MUST NOT be represented as
untyped bare numbers when crossing domain boundaries.


---

# 9. Stock Solution

Stock solution calculation must consider:

- target concentration;
- target final volume;
- antimicrobial powder mass;
- antimicrobial potency or active-content correction when applicable.

The simple relationship:

mass = concentration × volume

is valid only when the concentration basis and active-material content
are compatible.

The engine MUST NOT automatically assume that antimicrobial powder is
100% active.

If potency is unknown, the system SHOULD clearly indicate this rather
than silently assume perfect potency.

Relevant metadata SHOULD eventually include:

- antimicrobial name;
- manufacturer;
- lot;
- potency;
- expiry;
- solvent;
- target stock concentration;
- target stock volume.


---

# 10. Intermediate Solutions

Intermediate solutions are a first-class scientific concept.

They MUST NOT be treated as an interface workaround.

The engine MUST distinguish:

mathematically possible dilution

from:

laboratorially executable dilution.


---

# 11. Minimum Reliable Pipetting Volume

The laboratory currently considers:

minimum reliable pipetting volume = 20 µL

This value is a LAB-CONSTRAINT.

It MUST be configurable.

It MUST NOT be hardcoded into scientific equations.

The engine MUST calculate the required source volume:

Vsource = (Ctarget × Vtarget) / Csource

If:

Vsource >= configured minimum reliable volume

the direct dilution MAY be considered feasible.

If:

Vsource < configured minimum reliable volume

the engine MUST NOT silently recommend that transfer.

Instead, it SHOULD determine whether an intermediate solution can be
prepared that allows subsequent pipetting operations to remain within
the configured laboratory limits.


---

# 12. Intermediate Solution Planning

When direct preparation is not feasible, the calculation engine SHOULD
attempt to generate an intermediate solution.

Example conceptual flow:

Stock Solution
→ Intermediate Solution
→ Working Solution
→ Plate

The algorithm SHOULD prefer solutions that:

1. respect minimum pipetting volume;
2. respect maximum pipette capacity;
3. reduce number of intermediate steps;
4. minimize unnecessary material consumption;
5. use practical preparation volumes;
6. avoid operating exactly at equipment limits when a better solution
   exists.

The first implementation does NOT need advanced optimization.

A deterministic and well-tested rule is preferable to premature
optimization.


---

# 13. Laboratory Configuration

Laboratory defaults MUST remain separate from scientific equations.

Initial laboratory defaults may include:

minimum reliable pipetting volume = 20 µL

These values MUST be editable.

Future laboratory configuration may also contain:

- available pipettes;
- pipette minimum volumes;
- pipette maximum volumes;
- pipette resolutions;
- balance readability;
- preferred preparation volumes;
- available vessel capacities.


---

# 14. Protocol Configuration

The user's current laboratory protocol SHOULD be represented as a
configurable preset.

It MUST NOT define the scientific engine itself.

Initial preset:

Protocol name:
Default Laboratory Microdilution

Plate:
96 wells

Plate dimensions:
8 rows × 12 columns

Current initial series:
up to 12 columns

Initial well preparation:

20 µL antimicrobial solution
+
180 µL medium
=
200 µL total pre-dilution preparation volume

Typical inoculum:

100 µL

Typical dilution series:

2-fold

Typical stock final volume:

1.00 mL

Minimum reliable pipetting volume:

20 µL

All of these values MUST remain configurable.


---

# 15. 20 µL + 180 µL Concept

The 20 µL antimicrobial + 180 µL medium preparation is a protocol
configuration.

It MUST NOT be embedded as a universal scientific equation.

General relationship:

Vpreparation =
Vantimicrobial + Vmedium

For the current preset:

20 µL + 180 µL = 200 µL

The required antimicrobial working concentration can be calculated
generally as:

Cworking =
Cpre-inoculum ×
Vpreparation / Vantimicrobial

For the current laboratory preset:

Vpreparation / Vantimicrobial
=
200 / 20
=
10

Therefore the antimicrobial solution added during this preparation step
must be 10 times the desired concentration in the 200 µL prepared
volume.

This factor MUST be calculated from configuration values.

It MUST NOT be hardcoded as 10.


---

# 16. Inoculation

Inoculation MUST be modeled using the general conservation relationship.

Never hardcode:

"adding inoculum divides concentration by 2"

The correct general equation is:

Cfinal =
Cpre ×
Vpre / (Vpre + Vinoculum)

Therefore:

Cpre =
Cfinal ×
(Vpre + Vinoculum) / Vpre

Equal-volume inoculation is only a special case.

Example:

100 µL antimicrobial-containing solution
+
100 µL inoculum

results in:

Cfinal = Cpre / 2

But this relationship changes whenever inoculum and pre-inoculum
volumes change.


---

# 17. Dilution Series

The calculation engine MUST support twofold concentration series.

General relationship:

Cn = C0 / 2^n

where n represents the number of dilution steps.

The model SHOULD eventually support arbitrary dilution factors.

Example:

Cn = C0 / factor^n

Important distinction:

A mathematical serial dilution model is not necessarily identical to a
specific normative preparation procedure.

The software MUST therefore distinguish between:

- concentration-series mathematics;
- physical transfer procedure;
- reference-method preparation procedure.


---

# 18. Plate Model

The physical plate and the experimental layout MUST be separate
concepts.

The initial physical plate model:

Plate96

rows = 8
columns = 12
total wells = 96

The calculation engine MUST NOT assume that all 12 columns always belong
to one dilution series.

A protocol layout may currently use:

12 columns

but future layouts may use:

6 columns

multiple independent series

controls in selected columns

replicates

different antimicrobials

The initial version does NOT need to implement all of these layouts.

However, architecture MUST NOT make future layouts impossible.


---

# 19. Plate Layout

Initial implementation MAY support one linear dilution series with a
configurable number of columns.

Suggested concept:

SerialDilutionLayout

start_column
number_of_columns
dilution_factor

Do NOT encode:

number_of_columns = 12

inside the scientific formula layer.


---

# 20. Calculation Graph

All important scientific calculations SHOULD produce a structured
calculation graph.

Example:

Target Final Concentration
↓
Correction for Inoculation
↓
Required Pre-Inoculum Concentration
↓
Required Working Concentration
↓
Direct Dilution Feasibility
↓
Intermediate Solution if Required
↓
Stock Preparation
↓
Dilution Series
↓
Final Concentrations per Well

Each step SHOULD contain:

- operation ID;
- input quantities;
- equation ID;
- equation;
- substituted values;
- result;
- units;
- source classification;
- reference identifier;
- warnings;
- laboratory constraints involved.

The calculation graph becomes the single source of truth for:

- GUI;
- reports;
- protocol instructions;
- debugging;
- tests;
- scientific audit.


---

# 21. Reporting

The application MUST NOT return only numerical results.

Reporting is part of the project architecture from the beginning.

For every completed calculation, the system SHOULD eventually generate:

## Technical Summary

A concise description of the relevant inputs and final results.

Example:

Target concentration in the first well: 4 µg/mL.

Pre-inoculum concentration required: 8 µg/mL.

Working antimicrobial concentration required: 80 µg/mL.

## Calculation Trace

A complete step-by-step explanation showing:

equation
→ substitution
→ result
→ unit

## Laboratory Preparation Instructions

Example style:

Prepare X mL of intermediate antimicrobial solution at Y µg/mL by
combining A µL of stock solution with B µL of diluent.

Add 20 µL of the working solution to 180 µL of medium.

## Scientific Methods Narrative

The program SHOULD be capable of creating a draft methodology paragraph
for reports or manuscripts.

The narrative MUST be generated from the actual protocol configuration
and calculation graph.

It MUST NOT contain hardcoded procedural text that becomes false when a
configuration changes.

## Scientific References

The report SHOULD list:

- equations used;
- equation identifiers;
- scientific source identifiers;
- normative / derived / laboratory / experimental classification.


---

# 22. Reporting Rule

The reporting layer MUST NOT recalculate scientific values.

It may format values.

It may select terminology.

It may generate explanatory text.

But every reported numerical result MUST originate from the validated
scientific calculation engine.

There MUST be one calculation source of truth.


---

# 23. Scientific Narrative Safety

Generated scientific text MUST distinguish:

"calculated using a relationship described by..."

from:

"performed according to..."

The second statement requires full methodological compliance.

Do NOT automatically generate phrases such as:

"according to CLSI"

"CLSI-compliant"

"according to ISO"

unless the relevant protocol requirements have actually been validated.


---

# 24. MIC

MIC is not part of the initial calculation core.

The initial system should calculate the concentration present in every
well.

Once the concentration map is validated, a later module may relate:

well
↔ concentration
↔ observed MIC

The future feature of predicting or calculating the expected MIC well
from prior biological information MUST initially be classified as:

EXPERIMENTAL

The project's previous mathematical expressions involving terms such as:

2^(MIC - n)

must NOT be incorporated directly into the validated core.

They may later be reviewed, derived, tested, and compared against the
validated plate model.


---

# 25. Uncertainty

Metrological uncertainty is important but outside the first scientific
core.

The architecture MUST allow future uncertainty contributions from:

- analytical balance;
- pipettes;
- volumetric devices;
- antimicrobial potency;
- concentration preparation;
- serial transfer;
- dilution operations.

Do NOT implement uncertainty propagation until the mathematical and
metrological model has been explicitly defined.

Potential future approaches include:

- analytical propagation;
- GUM-style uncertainty propagation;
- Monte Carlo simulation.

No approach should be selected solely because a library provides it.


---

# 26. External Scientific Libraries

The first scientific implementation SHOULD be internally implemented.

Third-party scientific calculation libraries MUST NOT initially define
the scientific model.

Initial core preference:

Python Standard Library

decimal.Decimal
dataclasses
enum
typing

Testing:

pytest

GUI later:

PySide6

Libraries such as:

NumPy
SciPy
Pint
uncertainties

may later be introduced for:

- independent verification;
- performance;
- comparison;
- validation;
- optional features.

They MUST NOT silently redefine the project's scientific equations.


---

# 27. Independent Validation Strategy

Scientific validation SHOULD occur at three levels.

Level 1:

Analytically known result

↓

Level 2:

Internal calculation engine

↓

Level 3:

Independent external implementation or scientific library

Example:

Analytical value
↔ Internal engine
↔ Pint / NumPy / independent script

Agreement between implementations increases confidence.

External libraries are validation tools, not unquestioned authorities.


---

# 28. Tests

Tests are mandatory for scientific code.

No scientific equation should be considered implemented without tests.

Tests SHOULD include:

## Unit Tests

Individual equation behavior.

## Dimensional Tests

Correct unit conversions.

## Analytical Tests

Known manually calculated results.

## Conservation Tests

Conservation of antimicrobial mass through dilution operations when
appropriate.

## Boundary Tests

Examples:

volume = minimum reliable pipetting volume

volume slightly below minimum

volume slightly above minimum

## Configuration Tests

Changing:

20 + 180

to:

50 + 150

must change calculations without requiring scientific code changes.

## Regression Tests

Validated calculations should be preserved as fixtures to prevent
future changes from altering results silently.


---

# 29. Example Fundamental Test

Given:

C1 = 1000 µg/mL
V1 = 20 µL
V2 = 200 µL

Expected:

C2 = 100 µg/mL

because:

1000 × 20 / 200 = 100

This should exist as an explicit analytical unit test.


---

# 30. Pipetting Feasibility Tests

Given:

minimum reliable volume = 20 µL

If calculated source volume is:

25 µL

direct preparation may be accepted.

If calculated source volume is:

20 µL

direct preparation may be accepted.

If calculated source volume is:

19.9 µL

direct preparation must be considered operationally invalid under the
current laboratory configuration.

The planner should then evaluate an intermediate solution.


---

# 31. Error Handling

Scientific errors must be explicit.

Never silently correct invalid scientific input.

Examples:

- negative volume;
- zero concentration where division requires nonzero concentration;
- impossible dilution;
- unsupported unit;
- unknown potency when potency is required;
- source volume below laboratory limit;
- volume above configured pipette capacity;
- inconsistent protocol volume totals.

Errors SHOULD include:

error code;
human-readable description;
affected quantity;
possible corrective action.


---

# 32. Warnings

Some conditions may be mathematically valid but experimentally
questionable.

These SHOULD produce warnings rather than incorrect calculations.

Example:

"Calculated transfer volume is exactly equal to the configured minimum
reliable pipetting volume."

Future warning levels MAY include:

INFO
CAUTION
INVALID


---

# 33. GUI Separation

The scientific engine MUST work without a GUI.

The GUI MUST NOT contain scientific formulas.

Expected architecture:

scientific/domain
↓
scientific/calculations
↓
protocol/planning
↓
reporting
↓
ui

PySide6 may be used later.

The same calculation engine MUST support:

- GUI;
- command-line tests;
- scripted validation;
- report generation.


---

# 34. Suggested Project Structure

project-root/
│
├── AGENTS.md
├── README.md
├── pyproject.toml
│
├── docs/
│   ├── scientific-model.md
│   ├── references.md
│   ├── terminology.md
│   ├── validation.md
│   └── architecture.md
│
├── specs/
│   ├── 001-units.md
│   ├── 002-stock-solution.md
│   ├── 003-dilution.md
│   ├── 004-intermediate-solution.md
│   ├── 005-lab-constraints.md
│   ├── 006-inoculation.md
│   ├── 007-serial-dilution.md
│   ├── 008-plate-model.md
│   ├── 009-reporting.md
│   ├── 010-uncertainty.md
│   └── 011-mic-analysis.md
│
├── src/
│   └── antimicrobial_calculator/
│       │
│       ├── domain/
│       ├── units/
│       ├── calculations/
│       ├── planning/
│       ├── protocols/
│       ├── plates/
│       ├── reporting/
│       └── ui/
│
└── tests/
    ├── unit/
    ├── analytical/
    ├── integration/
    ├── regression/
    └── validation/


---

# 35. Initial Development Scope — v0.1

Version 0.1 SHOULD focus on the scientific foundation.

Included:

- Python project structure;
- internal dimensional quantities;
- Decimal-based arithmetic;
- mass;
- volume;
- concentration;
- basic unit conversion;
- dilution equation;
- stock solution calculation;
- potency-aware stock calculation;
- working solution calculation;
- intermediate solution calculation;
- configurable minimum reliable pipetting volume;
- basic dilution feasibility check;
- inoculation correction;
- twofold concentration series;
- basic 96-well plate model;
- configurable number of dilution columns;
- calculation graph;
- technical calculation trace;
- automated analytical tests;
- scientific documentation framework.

Not required in v0.1:

- complete GUI;
- advanced plate layout editor;
- 6-column plate reuse workflow;
- automatic MIC prediction;
- uncertainty propagation;
- statistical analysis;
- database;
- cloud synchronization;
- machine learning.


---

# 36. Development Phase 2

After the scientific core is validated:

- protocol presets;
- automatic intermediate solution planning;
- pipette-aware optimization;
- richer plate layouts;
- practical laboratory instructions;
- scientific narrative generation;
- exportable results;
- GUI prototype using PySide6.


---

# 37. Development Phase 3

Later development may include:

- metrological uncertainty;
- balance uncertainty;
- pipette uncertainty;
- uncertainty propagation;
- Monte Carlo validation;
- advanced plate layouts;
- multiple antimicrobials;
- replicate layouts;
- controls;
- alternative dilution factors;
- plate reuse with six-column series.


---

# 38. Development Phase 4

Experimental scientific extensions may include:

- MIC-position calculation;
- expected MIC well mapping;
- retrospective MIC analysis;
- breakpoint-aware plate planning;
- comparison between predicted and observed MIC;
- evaluation of previously developed MIC equations.

These features MUST remain clearly marked EXPERIMENTAL until validated.


---

# 39. Coding Rules for Agents

Any coding agent working on this repository MUST follow these rules.

1. Read AGENTS.md before modifying scientific code.

2. Read the relevant specification before implementing a feature.

3. Do not introduce a scientific equation without documenting it.

4. Do not replace Decimal with float in scientific quantities without an
   explicit architectural decision.

5. Do not hardcode laboratory defaults inside equations.

6. Do not assume 20 µL is universal.

7. Do not assume 20 + 180 µL is universal.

8. Do not assume a well always contains 200 µL.

9. Do not assume inoculation always causes a twofold dilution.

10. Do not assume every plate series contains 12 columns.

11. Do not assume all antimicrobial powders have 100% potency.

12. Do not add third-party scientific libraries merely for convenience.

13. Do not move calculations into the GUI.

14. Do not let the reporting layer calculate independent results.

15. Do not claim normative compliance without documented justification.

16. Every scientific change requires tests.

17. Preserve backwards-compatible validated calculations whenever
    possible.

18. If scientific behavior is ambiguous, STOP and document the ambiguity
    rather than guessing.


---

# 40. Scientific Change Procedure

Before changing scientific behavior:

1. Identify the scientific requirement.

2. Classify it as:

   NORMATIVE
   DERIVED
   LAB-CONSTRAINT
   EXPERIMENTAL

3. Identify or create the relevant equation ID.

4. Document the source or derivation.

5. Add analytical examples.

6. Implement tests.

7. Implement calculation logic.

8. Verify units.

9. Verify calculation trace.

10. Verify report output.

11. Run regression tests.

12. Record the change in documentation.


---

# 41. Never Guess Scientific Behavior

If a requirement cannot be established from:

- an adopted reference;
- explicit mathematics;
- laboratory configuration;
- an explicitly documented experimental model;

the agent MUST NOT invent a solution.

Instead:

- document the uncertainty;
- identify the missing information;
- create a TODO or specification question;
- keep existing validated behavior unchanged.


---

# 42. Scientific Reproducibility

Given the same:

- protocol configuration;
- laboratory configuration;
- antimicrobial properties;
- potency;
- concentration target;
- volumes;
- dilution factor;

the engine MUST produce the same scientific result.

Any intentional nondeterministic method introduced later, such as Monte
Carlo uncertainty propagation, MUST use explicit reproducibility
controls such as deterministic seeds when validation requires them.


---

# 43. Documentation Language

Code identifiers SHOULD be written in English.

Scientific documentation MAY be written in Portuguese initially.

User-facing terminology SHOULD initially prioritize Portuguese.

Examples:

stock_solution
intermediate_solution
working_solution
final_concentration

may internally correspond to:

solução mãe
solução intermediária
solução de trabalho
concentração final

Terminology mapping MUST be documented in:

docs/terminology.md


---

# 44. Final Project Principle

The program must always be able to answer:

"What was calculated?"

"Why was it calculated this way?"

"Which equation was used?"

"Which values entered the equation?"

"Which laboratory restriction affected the result?"

"Which source supports the calculation?"

"Is this normative, derived, laboratory-specific, or experimental?"

"How can another person reproduce the calculation?"

If the application cannot answer these questions, the scientific feature
is not complete.