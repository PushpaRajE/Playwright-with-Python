def get_credentials(scenario: str):
    valid_username = "tomsmith"
    valid_password = "SuperSecretPassword!"

    mapping = {
        "valid": {"username": valid_username, "password": valid_password},
        "invalid_username": {"username": "wrong_user", "password": valid_password},
        "invalid_password": {"username": valid_username, "password": "wrong_pass"},
        "empty_username": {"username": "", "password": valid_password},
        "empty_password": {"username": valid_username, "password": ""}
    }

    return mapping[scenario]
