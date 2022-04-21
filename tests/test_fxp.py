import construct
import pytest

from fxp import FXP, InvalidAttribute, PresetType


def test_is_opaque(serum_init: FXP):
    assert serum_init.is_opaque()


def test_is_regular(serum_init: FXP):
    assert not serum_init.is_regular()


def test_preset_type(serum_init: FXP, monkeypatch: pytest.MonkeyPatch):
    assert serum_init.preset_type == PresetType.OPAQUE
    monkeypatch.setattr(serum_init, "preset_type", "MISSING_TYPE")
    with pytest.raises(construct.ConstructError):
        serum_init.to_bytes()


def test_plugin_id(serum_init: FXP):
    assert serum_init.plugin_id == "XfsX"
    with pytest.raises(ValueError):
        serum_init.plugin_id = "size_not_4"


def test_plugin_version(serum_init: FXP):
    assert serum_init.plugin_version == 1


def test_param_count(serum_init: FXP):
    assert serum_init.param_count == 1
    with pytest.raises(InvalidAttribute):
        serum_init.param_count = 0


def test_name(serum_init: FXP):
    assert serum_init.name == "serum_init"
    with pytest.raises(OverflowError):
        serum_init.name = "S" * 29


def test_params(serum_init: FXP):
    with pytest.raises(InvalidAttribute):
        getattr(serum_init, "params")
    with pytest.raises(InvalidAttribute):
        setattr(serum_init, "params", None)


def test_data(serum_init: FXP):
    assert len(serum_init.data) == 6299
