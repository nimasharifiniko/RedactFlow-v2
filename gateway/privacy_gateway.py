import json
from core.redactor import redact_text, restore_text
from core.merger import scan_document


def secure_prompt(user_prompt: str) -> tuple[str, dict]:

    findings = scan_document(user_prompt, use_llm=False)

    masked_prompt, mapping = redact_text(
        user_prompt, findings, generate_mapping=True
    )

    return masked_prompt, mapping


def restore_response(ai_response: str, mapping: dict) -> str:
    return restore_text(ai_response, mapping)
