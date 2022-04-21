import pathlib

import pytest

from fxp import FXP

ASSETS_DIR = pathlib.Path(__file__).parent / "assets"


@pytest.fixture
def serum_init() -> FXP:
    return FXP(ASSETS_DIR / "serum_init.fxp")
