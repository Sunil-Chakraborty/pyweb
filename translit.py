def custom_transliterate(text):
    transliteration_map = {
        "আমি": "ami",
        "বাংলায়": "banglai",
        "গান": "gan",
        "গাই": "gai",
        # Add more mappings as needed
    }
    
    for bangla, english in transliteration_map.items():
        text = text.replace(bangla, english)
    
    return text

text = "আমি বাংলায় গান গাই"
transliterated_text = custom_transliterate(text)
print(transliterated_text)  # Output: ami banglai gan gai
