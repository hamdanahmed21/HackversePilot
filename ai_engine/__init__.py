"""
ai_engine
AI Meeting Watchdog — AI/ML layer

Public surface used by the backend:

    from ai_engine.policy_parser import extract_text
    from ai_engine.rule_extractor import extract_rules
    from ai_engine.contradiction_checker import check_contradiction

Internals (groq_client.py, config.py) are implementation details shared
across the two pipelines and not meant to be imported directly by the
backend layer.
"""
