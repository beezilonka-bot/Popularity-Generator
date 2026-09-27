from pathlib import Path

from src.context.worldbook_resolver import load_entries, resolve_worldbook


ROOT = Path(__file__).resolve().parents[1]


def test_exact_keyword_activation():
    entries = load_entries(ROOT / "worldbook" / "registry.yaml")
    result = resolve_worldbook("写一条 X 推文，需要数据和来源")
    ids = {entry.entry_id for entry in result.entries}
    assert "WB-X-001" in ids
    assert "WB-X-005" in ids


def test_unmatched_task_returns_empty_context():
    entries = load_entries(ROOT / "worldbook" / "registry.yaml")
    result = resolve_worldbook("做一个完全无关的任务")
    assert result.entries == []
    assert result.skills == []
    assert result.resources == []


def test_budget_and_deduplication():
    entries = load_entries(ROOT / "worldbook" / "registry.yaml")
    result = resolve_worldbook(
        "推文 tweet thread 文风 style 研究 research 数据 引用",
        token_budget=200,
        max_entries=3,
    )
    assert len(result.entries) <= 3
    assert result.estimated_tokens <= 200
    assert len(result.skills) == len(set(result.skills))
    assert len(result.resources) == len(set(result.resources))
