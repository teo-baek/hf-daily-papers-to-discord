def classify_field(title, summary):
    text = (title + " " + summary).lower()
    if any(k in text for k in ["language model", "llm", "gpt", "bert", "nlp"]):
        return "🧠"
    elif any(k in text for k in ["image", "vision", "diffusion", "object detection"]):
        return "🖼️"
    elif any(k in text for k in ["audio", "speech", "sound", "voice"]):
        return "🔊"
    elif any(k in text for k in ["robot", "motion", "navigation"]):
        return "🤖"
    elif any(k in text for k in ["reinforcement", "policy", "agent"]):
        return "🎮"
    elif any(k in text for k in ["graph", "gnn", "network"]):
        return "🕸️"
    else:
        return "📘"
