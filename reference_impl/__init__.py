"""Reference implementations for the six knowledge points (KP1-KP6).

Every function implements the course conventions documented in
conventions/course_conventions.md. These implementations define ground truth;
they are validated against independent derivations in verify_dual.py before
any benchmark data is collected.
"""

from . import portfolio, capm, bond, blackscholes, var, performance  # noqa: F401
