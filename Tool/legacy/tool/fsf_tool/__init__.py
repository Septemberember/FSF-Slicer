"""FSF-guided Java slicing and testing-based formal verification."""

import warnings

# Z3 4.12.2 (the paper's implementation version) imports pkg_resources. The
# dependency is intentionally pinned and present; hide only its noisy lifecycle warning.
warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API.*", category=UserWarning)

from .models import AnalysisConfig, FunctionalScenario, FSFSpec

__all__ = ["AnalysisConfig", "FunctionalScenario", "FSFSpec"]
__version__ = "1.0.0"
