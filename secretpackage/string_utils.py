def reverse_string(text):
    """Reverse a string"""
    return text[::-1]

def capitalize_words(text):
    """Capitalize first letter of each word"""
    return ' '.join(word.capitalize() for word in text.split())

def remove_spaces(text):
    """Remove all spaces from a string"""
    return text.replace(' ', '')