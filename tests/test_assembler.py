from src.context.assembler import assemble_prompt


def test_prompt_section_order():
    prompt = assemble_prompt({
        "CURRENT_TASK": "task",
        "MODEL_PRESET": "preset",
        "FRESH_PROJECT_CONTEXT": "project",
        "LONG_MEMORY": {"entries": [{"id": "M1", "content": "memory"}]},
        "RELEVANT_WORLD_BOOK": {"entries": [{"id": "W1", "content": "world"}]},
    })
    assert prompt.index("=== MODEL_PRESET ===") < prompt.index("=== CURRENT_TASK ===")
    assert prompt.index("=== LONG_MEMORY ===") < prompt.index("=== RELEVANT_WORLD_BOOK ===")


def test_global_budget_does_not_remove_task():
    prompt = assemble_prompt({
        "MODEL_PRESET": "p" * 100,
        "FRESH_PROJECT_CONTEXT": "c" * 100,
        "LONG_MEMORY": {"entries": [{"id": "M1", "content": "m" * 1000}]},
        "RELEVANT_WORLD_BOOK": {"entries": [{"id": "W1", "content": "w" * 1000}]},
        "CURRENT_TASK": "important task",
    }, max_total_tokens=100)
    assert "important task" in prompt
