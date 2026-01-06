def generate_login_test_cases(requirement: str):
    """
    Generates login test cases based on a functional requirement.

    Args:
        requirement (str): Functional requirement description

    Returns:
        list[dict]: List of test case definitions
    """

    if not requirement or not isinstance(requirement, str):
        raise ValueError("Requirement must be a non-empty string")

    requirement_lower = requirement.lower()
    test_cases = []

    if "login" in requirement_lower:
        test_cases = [
            {
                "title": "Valid login",
                "scenario": "valid",
                "expected": "success",
            },
            {
                "title": "Invalid username",
                "scenario": "invalid_username",
                "expected": "failure",
            },
            {
                "title": "Invalid password",
                "scenario": "invalid_password",
                "expected": "failure",
            },
            {
                "title": "Empty username",
                "scenario": "empty_username",
                "expected": "failure",
            },
            {
                "title": "Empty password",
                "scenario": "empty_password",
                "expected": "failure",
            },
        ]

    return test_cases
