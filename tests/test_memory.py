from pathlib import Path

from src.context.memory import load_memories


ROOT = Path(__file__).resolve().parents[1]


def test_long_memory_is_separate_source():
    result = load_memories(ROOT / "memory" / "registry.yaml")
    assert result == []
