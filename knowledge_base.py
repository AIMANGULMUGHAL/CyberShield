# Knowledge Base rules stored as simple dictionaries
RULES = [
    {
        "id": "R1",
        "symptom": "failed_logins",
        "threat": "BRUTE-FORCE ATTACK DETECTED",
        "severity": "MEDIUM",
        "diagnosis": "Multiple failed login attempts detected. Active credential stuffing suspected.",
        "actions": [
            "Enforce immediate MFA reset across affected accounts.",
            "Block originating IP subnet on edge firewall."
        ]
    },
    {
        "id": "R2",
        "symptom": "ransom_note",
        "threat": "CRITICAL RANSOMWARE THREAT",
        "severity": "HIGH",
        "diagnosis": "Unauthorized file encryption activity paired with ransom notes.",
        "actions": [
            "Isolate system from the network immediately.",
            "Preserve volatile RAM memory for forensics.",
            "Verify clean offline backups prior to system restore."
        ]
    },
    {
        "id": "R3",
        "symptom": "high_traffic",
        "threat": "DATA EXFILTRATION / C2 BEACON",
        "severity": "HIGH",
        "diagnosis": "Abnormal outbound traffic volume detected targeting untrusted external IPs.",
        "actions": [
            "Terminate active outbound socket connections.",
            "Isolate host machine via EDR agent."
        ]
    },
    {
        "id": "R4",
        "symptom": "popups",
        "threat": "LOCAL ENDPOINT MALWARE",
        "severity": "LOW",
        "diagnosis": "System resource degradation combined with unauthorized popups.",
        "actions": [
            "Run full automated EDR/Antivirus scan.",
            "Remove unknown browser extensions and startup keys."
        ]
    }
]