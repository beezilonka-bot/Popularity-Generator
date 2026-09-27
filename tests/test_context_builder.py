from pathlib import Path

from src.context.context_builder import build_context


ROOT = Path(__file__).resolve().parents[1]


def test_builder_reads_repository_policy_and_builds_prompt():
    result = build_context(
        project_root=ROOT,
        current_task="写一条 X 推文，需要数据和来源",
        project_context="Project: PG",
        model_preset="PRESET",
    )
    assert result["MODEL_PRESET"] == "PRESET"
    assert "WB-X-001" in {x["id"] for x in result["RELEVANT_WORLD_BOOK"]["entries"]}
    assert result["PROMPT"].index("=== MODEL_PRESET ===") < result["PROMPT"].index("=== CURRENT_TASK ===")


def test_builder_scans_configured_project_context():
    result = build_context(
        project_root=ROOT,
        current_task="完全无关的任务",
        project_context="本轮需要研究 Github 资料并引用来源",
        model_preset="PRESET",
    )
    ids = {x["id"] for x in result["RELEVANT_WORLD_BOOK"]["entries"]}
    assert "WB-X-004" in ids


def test_builder_scans_recent_context_with_bounded_depth():
    result = build_context(
        project_root=ROOT,
        current_task="完全无关的任务",
        project_context="Project: PG",
        model_preset="PRESET",
        recent_context=["无关内容", "这里讨论线程 thread 写作"],
        scan_depth=1,
    )
    ids = {x["id"] for x in result["RELEVANT_WORLD_BOOK"]["entries"]}
    assert "WB-X-002" in ids
