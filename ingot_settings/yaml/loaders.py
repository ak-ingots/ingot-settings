"""The file loader of the defaults with YAML files: the only module importing PyYAML."""

__all__ = ("YamlFileLoader", "YamlFormat")

import typing as t

from ingots.defaults.settings.loaders import BaseFormat, FileLoader
from ingots.puer import Slot

try:
    import yaml
except ImportError:
    raise ImportError(
        'ingot_settings.yaml needs PyYAML: pip install "ingot-settings[yaml]"'
    ) from None


class YamlFormat(BaseFormat):
    """
    A YAML file: a mapping of config names to YAML values, read by
    :class:`PlainLoader`. It resolves no types: a scalar is a string,
    converted by its config as an environment variable is, so the booleans,
    octals and dates of YAML 1.1 do not apply; a sequence is a list and a
    mapping a dict, which a config rejects unless it converts them. An empty
    file has no overrides.
    """

    EXTENSIONS = frozenset({".yaml", ".yml"})

    @t.override
    def parse(self, text: str) -> dict[str, object]:
        try:
            data = yaml.load(text, Loader=PlainLoader)
        except yaml.YAMLError as error:
            raise ValueError(str(error)) from None
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ValueError(f"not a YAML mapping but {type(data).__qualname__}")
        return data


class YamlFileLoader(FileLoader):
    """
    The file loader of the defaults reading YAML files (``.yaml``, ``.yml``)
    next to INI and JSON. Joined with another addon's file loader, it takes a
    class extending both: ``class AppFileLoader(YamlFileLoader, TomlFileLoader)``.
    """

    yaml_format = Slot(YamlFormat)


class PlainLoader(yaml.BaseLoader):
    """
    The base loader of PyYAML failing on a tag, which it would ignore, on a
    key given twice in a mapping, and on an alias of a sequence or a mapping:
    those nest into data exponentially larger than the text (billion laughs).
    The aliases of scalars may repeat at most as many characters as the text
    holds, so the data is at most twice as large.
    """

    PLAIN_TAGS: t.ClassVar[dict[type[yaml.Node], str]] = {
        yaml.ScalarNode: yaml.BaseLoader.DEFAULT_SCALAR_TAG,
        yaml.SequenceNode: yaml.BaseLoader.DEFAULT_SEQUENCE_TAG,
        yaml.MappingNode: yaml.BaseLoader.DEFAULT_MAPPING_TAG,
    }

    def __init__(self, stream: str) -> None:
        super().__init__(stream)
        self.alias_budget = len(stream)

    @t.override
    def compose_node(self, parent: yaml.Node | None, index: t.Any) -> yaml.Node | None:
        if self.check_event(yaml.AliasEvent):
            event = self.peek_event()  # type: ignore[no-untyped-call]
            node = self.anchors.get(event.anchor)  # undefined: the base fails
            if isinstance(node, yaml.ScalarNode):
                self.alias_budget -= len(node.value)
                if self.alias_budget < 0:
                    raise yaml.composer.ComposerError(
                        None, None, "the aliases repeat too much", event.start_mark
                    )
            elif node is not None:
                raise yaml.composer.ComposerError(
                    "found an alias",
                    event.start_mark,
                    "of a sequence or a mapping",
                    node.start_mark,
                )
        return super().compose_node(parent, index)

    @t.override
    def construct_object(self, node: yaml.Node, deep: bool = False) -> t.Any:
        if node.tag != self.PLAIN_TAGS[type(node)]:
            raise yaml.constructor.ConstructorError(
                None, None, f"found the tag {node.tag!r}", node.start_mark
            )
        return super().construct_object(node, deep=deep)

    @t.override
    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[t.Hashable, t.Any]:
        keys = set()
        for key_node, _ in node.value:
            if not isinstance(key_node, yaml.ScalarNode):
                continue  # unhashable: the base loader rejects it
            key = self.construct_scalar(key_node)
            if key in keys:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found the key {key!r} twice",
                    key_node.start_mark,
                )
            keys.add(key)
        return super().construct_mapping(node, deep=deep)
