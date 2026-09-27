from src.context.engine import Candidate, rank_candidates, select_budgeted


def test_required_candidate_ranks_first():
    candidates = [
        Candidate("normal", "worldbook", "a" * 20, priority=100),
        Candidate("required", "worldbook", "b" * 20, priority=1, required=True),
    ]
    assert rank_candidates(candidates)[0].candidate_id == "required"


def test_budget_is_hard():
    candidates = [
        Candidate("a", "worldbook", "a" * 40),
        Candidate("b", "worldbook", "b" * 40),
    ]
    result = select_budgeted(candidates, max_items=8, token_budget=10)
    assert result.estimated_tokens <= 10
    assert len(result.selected) <= 1


def test_same_inputs_are_deterministic():
    candidates = [
        Candidate("b", "worldbook", "b", priority=2),
        Candidate("a", "worldbook", "a", priority=2),
    ]
    assert [x.candidate_id for x in rank_candidates(candidates)] == ["a", "b"]
