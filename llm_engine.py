import ollama

SYSTEM_PROMPT = """You are the BENCHSAFE AI Workspace Safety Assistant.
Your sole job is to summarize incoming electronics bench events into a single, highly concise incident report.

STRICT RULES:
1. Maximum length: 15 to 20 words. Exactly ONE sentence.
2. Describe the technical safety event clearly. 
3. NEVER assume, extrapolate, or fabricate details.
"""

def generate_ai_report(timestamp: str, source: str, detail: str, cutoff_active: bool) -> str:
    user_prompt = (
        f"Timestamp: {timestamp}\n"
        f"Source: {source.upper()}\n"
        f"Event Detail: {detail}\n"
        f"Hardware Cutoff Active: {cutoff_active}"
    )
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception:
        # Clean fallback text if Ollama is offline
        if "Temp" in detail:
            return "Overheating temperature detected on soldering tool. Local power cutoff activated."
        elif "Current" in detail:
            return "Excessive current load detected on circuit. Local power cutoff activated."
        elif "Glasses" in detail:
            return "Operator safety violation flagged: safety glasses not detected."
        elif "Edge" in detail:
            return "Fall hazard detected: tool placed dangerously close to table edge."
        else:
            return f"Unsafe condition flagged: {detail}."