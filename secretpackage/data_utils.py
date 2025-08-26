def process_list(data):
    """Process a list of numbers by sorting and removing duplicates"""
    if not data:
        return []
    return sorted(set(data))

def find_max_min(data):
    """Find maximum and minimum values in a list"""
    if not data:
        return None, None
    return max(data), min(data)

def calculate_average(data):
    """Calculate the average of a list of numbers"""
    if not data:
        return 0
    return sum(data) / len(data)