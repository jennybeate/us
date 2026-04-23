from config import ACTION_TEMPLATE_SETS, PILLAR_KEYWORD_MAP, CONTEXT_QUESTIONS


def _match_template_set(pillar_name: str) -> str:
    name_lower = pillar_name.lower()
    best_key = "default"
    best_score = 0
    for key, keywords in PILLAR_KEYWORD_MAP.items():
        score = sum(1 for kw in keywords if kw in name_lower)
        if score > best_score:
            best_score = score
            best_key = key
    return best_key


def get_actions(pillar_name: str, partner_name: str, count: int = 6) -> list[str]:
    key = _match_template_set(pillar_name)
    templates = ACTION_TEMPLATE_SETS.get(key, ACTION_TEMPLATE_SETS["default"])
    # Cycle through up to `count` templates
    selected = templates[:count]
    return [
        t.replace("{name}", partner_name).replace("{pillar}", pillar_name)
        for t in selected
    ]


def score_state(value: int) -> str:
    """Returns 'low', 'mid', or 'high' for display logic."""
    if value <= 2:
        return "low"
    if value <= 3:
        return "mid"
    return "high"


def score_label(value: int) -> str:
    labels = {1: "Needs love", 2: "Could be better", 3: "Getting there", 4: "Doing well", 5: "Thriving"}
    return labels.get(value, "")


def radar_data(partner1: dict, partner2: dict) -> tuple[list, list, list]:
    """
    Returns (categories, p1_scores, p2_scores) for a Plotly radar chart.
    Uses the union of all pillar names from both partners.
    Scores come from stored scores; missing = 3.
    """
    p1_pillars = partner1.get("pillars", [])
    p2_pillars = partner2.get("pillars", [])

    # Build merged category list: interleave to avoid clutter
    p1_names = [p["name"] for p in p1_pillars]
    p2_names = [p["name"] for p in p2_pillars]

    # Use each partner's own pillars for their own radar trace
    def _scores(pillars, scores_dict):
        result = []
        for p in pillars:
            pid = p["id"]
            result.append(scores_dict.get(pid, {}).get("value", 3))
        return result

    p1_scores_dict = partner1.get("scores", {})
    p2_scores_dict = partner2.get("scores", {})

    return (
        p1_names,
        _scores(p1_pillars, p1_scores_dict),
        p2_names,
        _scores(p2_pillars, p2_scores_dict),
    )


def generate_insights(partner1: dict, partner2: dict) -> list[str]:
    """Generate soft insight cards from Phase 0 context answers."""
    insights = []
    c1 = partner1.get("context", {})
    c2 = partner2.get("context", {})
    n1 = partner1.get("name", "Partner 1")
    n2 = partner2.get("name", "Partner 2")

    # Love language match
    ll1 = set(c1.get("c1", []))
    ll2 = set(c2.get("c1", []))
    shared_ll = ll1 & ll2
    if shared_ll:
        examples = ", ".join(list(shared_ll)[:2])
        insights.append(
            f"You both value the same things: <em>{examples}</em>. "
            "That's a real strength — you already speak each other's language here."
        )

    # Appreciation need
    a1 = c1.get("c10", 3)
    a2 = c2.get("c10", 3)
    if isinstance(a1, int) and isinstance(a2, int) and a1 >= 4 and a2 >= 4:
        insights.append(
            f"Both {n1} and {n2} rate feeling appreciated as very important. "
            "Make it a practice to name what you're grateful for in each other — often and specifically."
        )
    elif isinstance(a1, int) and isinstance(a2, int) and abs(a1 - a2) >= 2:
        more_name = n1 if a1 > a2 else n2
        insights.append(
            f"{more_name} needs more recognition and appreciation than their partner may realise. "
            "Small, specific acknowledgements go a long way."
        )

    # Attachment styles
    att1 = c1.get("c6", 3)
    att2 = c2.get("c6", 3)
    if isinstance(att1, int) and isinstance(att2, int):
        if att1 <= 2 and att2 >= 4:
            insights.append(
                f"{n1} tends to seek closeness when disconnected, while {n2} tends to need space. "
                "When things feel off, try saying: 'I need a bit of time, but I'm not going anywhere.'"
            )
        elif att1 >= 4 and att2 <= 2:
            insights.append(
                f"{n2} tends to seek closeness when disconnected, while {n1} tends to need space. "
                "When things feel off, try saying: 'I need a bit of time, but I'm not going anywhere.'"
            )

    # Overall satisfaction
    s1 = c1.get("c12", 3)
    s2 = c2.get("c12", 3)
    if isinstance(s1, int) and isinstance(s2, int):
        if s1 >= 4 and s2 >= 4:
            insights.append(
                "You both feel genuinely satisfied with your relationship. "
                "Use this app to deepen that, not fix what's broken."
            )
        elif s1 <= 2 or s2 <= 2:
            low_name = n1 if (isinstance(s1, int) and s1 <= 2) else n2
            insights.append(
                f"{low_name} is finding the relationship hard right now. "
                "The pillars and actions below are a place to start — small, consistent effort matters."
            )

    return insights[:4]  # Cap at 4 insights
