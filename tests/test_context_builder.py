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
