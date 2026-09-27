from pathlib import Path

from src.context.types import WorldBookEntry
from src.context.worldbook_resolver import load_entries, resolve_worldbook


ROOT = Path(__file__).resolve().parents[1]


def entries():
    return load_entries(ROOT / "worldbook" / "registry.yaml")


def test_exact_keyword_activation():
    result = resolve_worldbook("写一条 X 推文，需要数据和来源", entries())
    ids = {entry.entry_id for entry in result.entries}
    assert "WB-X-001" in ids
    assert "WB-X-005" in ids


def test_unmatched_task_returns_empty_context():
    result = resolve_worldbook("做一个完全无关的任务", entries())
    assert result.entries == []
    assert result.skills == []
    assert result.resources == []


def test_budget_and_deduplication():
    result = resolve_worldbook(
        "推文 tweet thread 文风 style 研究 research 数据 引用",
        entries(),
        token_budget=200,
        max_entries=3,
    )
    assert len(result.entries) <= 3
    assert result.estimated_tokens <= 200
    assert len(result.skills) == len(set(result.skills))
    assert len(result.resources) == len(set(result.resources))


def test_scope_blocks_nonmatching_entry():
    scoped = [WorldBookEntry(
        entry_id="SCOPE-ONLY",
        name="SCOPE-ONLY",
        keys=["写推文"],
        scope=["x"],
        content="scope-only",
    )]
    result = resolve_worldbook("写推文", scoped, scope="other")
    assert result.entries == []


def test_trace_contains_match_type():
    result = resolve_worldbook("写一条 X 推文", entries())
    assert result.matches
    assert result.matches[0].match_type == "direct"
