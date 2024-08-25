def ValidateRegistrationPayload(username, password):
    if not username or not password:
        return False
    if len(username) < 3 or len(password) < 6:
        return False
    return True