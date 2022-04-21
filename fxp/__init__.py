"""VST2.x FXP preset parser.

Example:
    >>> import fxp
    >>> preset = fxp.FXP("path/to/preset.fxp")
    >>> preset.plugin_id
    "XfsX"
    >>> preset.name
    "LD Saw Bass"
    >>> preset.is_opaque()
    True
"""

import enum
import os

import construct as c

__all__ = ["FXP", "InvalidAttribute"]


class PresetType(enum.Enum):
    """Representation used for the preset data.

    VST plugins have 2 options to save the preset data:

    1. Regular: Stored as a list of floats. These values correspond to
        the plugin parameters shown as faders, knobs etc. in the GUI.
        There is no way to store a slider name or any string in this type
        of representation hence very few plugins use this option.
    2. Opaque: Stored as a plugin specific blob of binary data. This
        gives plugin devs flexibility to use any data type and/or encrypt
        and compress it. Most plugins use this.
    """

    OPAQUE = "FPCh"
    REGULAR = "FxCk"


class InvalidAttribute(AttributeError):
    """Raised when an instance of `FXP` tries to get/set an invalid attribute."""

    def __init__(self, attr: "str", preset_type: "PresetType") -> "None":
        """Constructor.

        Args:
            attr (str): Name of the invalid attribute of class `FXP`.
            preset_type (str): Type of the preset for which accessing `attr`
                is not permitted. This includes get and/or set actions.
        """
        self.__attr = attr
        self.__type = preset_type
        super().__init__()

    def __repr__(self) -> "str":  # noqa: D105
        return f"{self.__type.name!r} presets don't have access to {self.__attr!r}"

    __str__ = __repr__


class FXP:
    """VST2.x plugin preset parser.

    Caution:
        Use this for parsing only presets (.fxp) and not soundbanks (.fxb).
    """

    _fxp = c.Struct(
        "chunkMagic" / c.Const(b"CcnK"),
        "byteSize" / c.Int32ub,
        "fxMagic" / c.Enum(c.PaddedString(4, "ascii"), PresetType),  # type: ignore
        "version" / c.Const(1, c.Int32ub),
        "fxID" / c.PaddedString(4, "ascii"),
        "fxVersion" / c.Int32ub,
        "numParams" / c.Int32ub,
        "prgName" / c.PaddedString(28, "ascii"),
        "content"
        / c.IfThenElse(
            c.this["fxMagic"] == PresetType.REGULAR,
            c.Float32b[c.this["numParams"]],
            c.Struct(
                "size" / c.Int32ub,
                "data" / c.Int8ub[c.this["size"]],
            ),
        ),
    )

    def __init__(self, path: "str | os.PathLike") -> "None":
        """Create a new parser instance.

        Preset files using this format generally have .fxp extension although
        some plugins have their own file name extensions.

        Args:
            path (str | os.PathLike): The path of the preset file.
        """
        self._path = path
        self._struct = self._fxp.parse_file(path)  # type: ignore

    def is_opaque(self) -> "bool":
        """Whether preset data is stored in opaque chunks."""
        return self.preset_type == PresetType.OPAQUE

    def is_regular(self) -> "bool":
        """Whether preset data is stored in regular chunks."""
        return self.preset_type == PresetType.REGULAR

    def save(self, path: "str | os.PathLike | None" = None) -> "None":
        """Save the preset back into a file.

        Args:
            path (str | os.PathLike, optional): Defaults to None.
                The name or path of the file to be used for saving the preset.
                If None, the original file is overwritten.
        """
        self._fxp.build_file(self._struct, path or self._path)  # type: ignore

    def to_bytes(self) -> "bytes":
        """Dumps this object back as a stream of bytes."""
        return self._fxp.build(self._struct)

    @property
    def preset_type(self) -> "PresetType":
        """You most likely need `is_opaque` and `is_regular` instead of this."""
        return PresetType[self._struct["fxMagic"]]

    @preset_type.setter
    def preset_type(self, value: "PresetType") -> "None":
        self._struct["fxMagic"] = value

    @property
    def plugin_id(self) -> "str":
        """A four character unique ID identifying the plugin e.g. "XfsX".

        This is used by DAWs and plugins to verify the preset's integrity.

        Raises:
            ValueError: When set to a string whose length in ASCII
                representation is not equal to 4.
        """
        return self._struct["fxID"]

    @plugin_id.setter
    def plugin_id(self, value: "str") -> "None":
        if len(value.encode("ascii")) != 4:
            raise ValueError("Expected a string of size 4")
        self._struct["fxID"] = value

    @property
    def plugin_version(self) -> "int":
        """Plugin preset format version.

        This could be used by devs to create a backward incompatible preset
        format for future versions of a plugin, while still allowing newer
        versions to handle the legacy formats differently.
        """
        return self._struct["fxVersion"]

    @plugin_version.setter
    def plugin_version(self, value: "int") -> "None":
        self._struct["fxVersion"] = value

    @property
    def param_count(self) -> "int":
        """Number of parameters for which preset data is stored.

        Used only by regular presets.

        Raises:
            InvalidAttribute: When an opaque preset tries to set a value.
        """
        return self._struct["numParams"]

    @param_count.setter
    def param_count(self, value: "int") -> "None":
        if not self.is_regular():
            raise InvalidAttribute("param_count", PresetType.OPAQUE)
        self._struct["numParams"] = value

    @property
    def name(self) -> "str":
        """Name of the preset as saved by the plugin (in ASCII).

        This is not always the same as the name of the preset file.

        Raises:
            OverflowError: When it is set to a string whose length in ASCII
                representation exceeds 28 characters / bytes.
        """
        return self._struct["prgName"]

    @name.setter
    def name(self, value: "str") -> "None":
        if len(value.encode("ascii")) > 28:
            raise OverflowError("Length of encodeded string exceeds 28")
        self._struct["prgName"] = value

    @property
    def params(self) -> "list[float]":
        """Return the preset data used by presets using regular data chunks.

        Raises:
            InvalidAttribute: When preset doesn't use regular data chunks.

        Returns:
            list[float]: The list of parameter values (knobs, sliders etc.).
        """
        if not self.is_regular():
            raise InvalidAttribute("params", PresetType.OPAQUE)
        return list(self._struct["content"])  # TODO Test return type

    @params.setter
    def params(self, values: "list[float]") -> "None":
        if not self.is_regular():
            raise InvalidAttribute("params", PresetType.OPAQUE)
        if len(values) != self.param_count:
            raise ValueError(f"Expected a list of length {self.param_count}")
        self._struct["content"] = values

    @property
    def data(self) -> "bytes":
        """Return the preset data used by presets using opaque data chunks.

        Raises:
            InvalidAttribute: When preset doesn't use opaque data chunks.

        Returns:
            bytes: Plugin-specific representation of the preset data.
        """
        if not self.is_opaque():
            raise InvalidAttribute("data", PresetType.REGULAR)
        return bytes(self._struct["content"]["data"])

    @data.setter
    def data(self, value: "bytes") -> "None":
        if not self.is_opaque():
            raise InvalidAttribute("data", PresetType.REGULAR)
        content = self._struct["content"]
        content["size"] = len(value)
        content["data"] = value
