"""
One entry per Kick-based clipping campaign. kick_clipper.py reads these.
Campaigns are normally added by the scout. A hand-written entry here
works too: copy a block, change the Kick channel, rules and hashtags. Every active campaign then gets the
same behaviour automatically: trend research + playbook every 3 days, and
(if it needs no draft approval) auto-posting at PUBLISH_TIME_UK.
"""

CAMPAIGNS = {}   # no fixed Kick campaigns: the scout finds and activates them (see state/clips_state.json)


# ---------------- Trend research targets (research.py) ----------------
# content_rewards_id = the id at the end of the campaign's Content Rewards URL.
RESEARCH = {
    "tokyo_girl": {
        "content_rewards_id": "40046522-56d9-45ad-9198-faea8eca90c6",
        "youtube_query": "GTA 6 edit",
        "language": "en",
        "transcribe": False,   # music-only edits, nothing spoken to transcribe
        "rules": ("Silent 12-second GTA 6 edits (3 shots x 4s) with on-screen text only; the "
                  "song Tokyo Girl is added in TikTok. No talking/voiceover/dialogue. Themes: GTA 6 "
                  "news/rumors, memes & hype, Jason & Lucia couple memes, edits & Vice City views. "
                  "Caption must credit the song. Original edits only."),
        "notes": "Our editor controls: the 3 text beats, which visual each beat uses, text case/size, caption + hashtags.",
    },
}


# ---------------- Campaigns added by the scout (scout.py) ----------------
# Activated campaigns live in state/clips_state.json -> "active_campaigns", so
# the agent can add/retire them without anyone editing this file.

DYNAMIC_DEFAULTS = {
    "enabled": True,
    "clips_per_day": 1,
    "min_clip": 20.0,
    "max_clip": 55.0,
    "needs_approval": False,
    "no_currency_symbols": False,
    "skip_title": r"casino|slot|gambl|roobet|stake\b",
    "prefer_title": r"",
    "title_suffix": " #Shorts",
    "tags": [],
    "language": "en",
}


def all_campaigns(state: dict) -> dict:
    """Built-in campaigns above + scout-activated ones, with retired ones switched off."""
    out = {k: dict(v) for k, v in CAMPAIGNS.items()}
    for k, v in (state.get("active_campaigns") or {}).items():
        out[k] = {**DYNAMIC_DEFAULTS, **v}
    for k in state.get("retired", []):
        if k in out:
            out[k]["enabled"] = False
    return out


def research_targets(state: dict) -> dict:
    targets = {k: dict(v) for k, v in RESEARCH.items()}
    for k, v in (state.get("active_campaigns") or {}).items():
        targets.setdefault(k, {
            "content_rewards_id": v["content_rewards_id"],
            "youtube_query": v.get("youtube_query") or v["name"],
            "language": v.get("language", "en"),
            "notes": v.get("notes", ""),
        })
    return targets
