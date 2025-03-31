from ..docker_runner import run_in_docker

def validate_variable_pattern(code: str, username: str, expected_result: str) -> bool:
    # Získáme název proměnné z expected_result
    variable_name = expected_result.split('=')[0].strip()
    variable_value = expected_result.split('=')[1].strip()

    test_code = code + "\n\n"
    test_code += "try:\n"
    # Kontrola existence proměnné se správným názvem
    test_code += f"    test = {variable_name}\n"  # Vyhodí NameError pokud proměnná neexistuje
    test_code += f"    user_str = str({variable_name})\n"
    test_code += f"    expected_str = str({variable_value})\n"
    test_code += "    print(user_str == expected_str)\n"
    test_code += "except NameError:\n"
    test_code += f"    print('False # {variable_name} not defined')\n"
    test_code += "except Exception as e:\n"
    test_code += "    print(f'False # {str(e)}')\n"

    result = run_in_docker(test_code, username)
    return result.strip().lower() == 'true' 