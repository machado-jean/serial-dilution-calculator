# Architecture

The intended dependency direction is:

`domain / units → calculations → planning → reporting → ui`

Scientific formulas are implemented in the calculation layer, documented with equation identifiers, and tested independently of the user interface.

