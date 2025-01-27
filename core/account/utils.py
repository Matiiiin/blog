import uuid

def make_random_string():
    return uuid.uuid4().hex[:20].upper()