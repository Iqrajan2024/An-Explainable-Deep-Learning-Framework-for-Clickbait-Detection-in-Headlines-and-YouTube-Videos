def join_words(words: list, max_items: int = 10) -> str:
    """Formats a raw list of strings into a human-readable comma-separated phrase."""
    if not words:
        return ""
        
    seen = set()
    unique_words = []
    
    for word in words:
        if word not in seen:
            unique_words.append(word)
            seen.add(word)
            
    sliced_words = [f"'{w}'" for w in unique_words[:max_items]]
    
    if len(sliced_words) == 1:
        return sliced_words[0]
    if len(sliced_words) == 2:
        return f"{sliced_words[0]} and {sliced_words[1]}"
        
    return ", ".join(sliced_words[:-1]) + " and " + sliced_words[-1]