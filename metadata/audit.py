import hashlib
import json
import time
import os

def generate_file_hash(filepath: str) -> str:
    # sha256 is used to prove the file existed without storing the file itself
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def create_audit_log(filepath: str, entities: list, log_dir: str = "audit_logs") -> dict:
    os.makedirs(log_dir, exist_ok=True)
    
    file_hash = generate_file_hash(filepath)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    # only log the counts and types, never the actual PII text
    breakdown = {}
    for item in entities:
        pii_type = item["type"]
        breakdown[pii_type] = breakdown.get(pii_type, 0) + 1
        
    log_entry = {
        "timestamp": timestamp,
        "file_hash": file_hash,
        "filename": os.path.basename(filepath),
        "total_entities_redacted": len(entities),
        "breakdown": breakdown
    }
    
    # write to a daily jsonl (json-lines) file for easy appending
    date_str = time.strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"audit_{date_str}.jsonl")
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
    return log_entry