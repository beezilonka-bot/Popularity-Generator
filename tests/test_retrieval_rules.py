from src.context.types import WorldBookEntry
from src.context.worldbook_resolver import resolve_worldbook


def test_conditions_and_scope():
    entries = [
        WorldBookEntry(
            "A", "A", keys=["研究"], scope=["x"],
            conditions={"all": ["数据"], "not_any": ["娱乐"]},
            content="A",
        )
    ]
    assert resolve_worldbook("研究 数据", entries, scope="x").entries
    assert not resolve_worldbook("研究", entries, scope="x").entries
    assert not resolve_worldbook("研究 数据 娱乐", entries, scope="x").entries
    assert not resolve_worldbook("研究 数据", entries, scope="other").entries


def test_bounded_recursive_activation():
    entries = [
        WorldBookEntry(
            "A", "A", keys=["入口"], recursive_activation=True,
            content="触发 B",
        ),
        WorldBookEntry(
            "B", "B", keys=["B"], recursive_activation=True,
            content="触发 C",
        ),
        WorldBookEntry(
            "C", "C", keys=["C"], recursive_activation=True,
            content="触发 A",
        ),
    ]
    result = resolve_worldbook(
        "入口", entries, max_recursive_depth=3, max_recursive_steps=10
    )
    ids = [x.entry_id for x in result.entries]
    assert ids == ["A", "B", "C"]
    assert all(x.depth <= 3 for x in result.matches)
