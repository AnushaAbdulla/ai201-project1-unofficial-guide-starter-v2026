def judge(question: str, expects: str, answer: str | None, results) -> bool:
    """
    Judge whether an answer contains enough of what the question expects.

    Parameters:
    - question: The question that was asked.
    - expects: Expected pieces of a correct answer, joined with "+",
      e.g. "railway + busses + driving".
    - answer: The generated answer, or None if no answer was produced.
    - results: The retrieved chunks (not used yet).

    Returns:
    - True if at least half of the expected pieces appear in the answer
      (case-insensitive), False otherwise.
    """
    
    if answer is None:
        return False

    pieces = [p.strip().lower() for p in expects.split("+") if p.strip()]
    if not pieces:
        return False

    text = answer.lower()
    hits = sum(1 for p in pieces if p in text)
    return hits / len(pieces) >= 0.5
