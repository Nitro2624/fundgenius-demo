import random

def get_fund_manager_notes():
    """
    Retrieves a list of recent fund manager insights.
    In a real application, this would come from an internal CMS,
    a database, or an RSS feed of official SBI MF insights.
    """
    notes = [
        "Equity markets continue to show resilience, with a focus on earnings growth in specific sectors.",
        "We are cautiously optimistic about mid-cap segment performance in the coming quarter.",
        "Inflationary pressures are being closely monitored; portfolio adjustments reflect defensive positioning where necessary.",
        "Debt market yields are stabilizing, presenting opportunities in short to medium duration instruments.",
        "Global economic factors remain a key watch point, influencing foreign institutional investment flows.",
        "Technology and healthcare sectors are showing strong fundamentals for long-term growth.",
        "Our strategic asset allocation remains consistent with long-term wealth creation objectives.",
        "New regulatory changes are being analyzed for their impact on mutual fund operations and investor returns."
    ]
    # Return a random subset or all notes for demonstration
    return random.sample(notes, k=min(len(notes), 5)) # Get up to 5 random notes
