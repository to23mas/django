from ..docker_runner import run_in_docker

def validate_variable_pattern(code: str, username: str, expected_result: str) -> bool:
    # Rozdělíme podle středníku pokud existuje, ale zachováme celý výraz
    variable_patterns = []
    for pattern in expected_result.split(';'):
        if not pattern.strip():
            continue
        # Najdeme pozici prvního '='
        equals_pos = pattern.find('=')
        if equals_pos != -1:
            variable_name = pattern[:equals_pos].strip()
            variable_value = pattern[equals_pos + 1:].strip()
            variable_patterns.append((variable_name, variable_value))
    
    test_code = code + "\n\n"
    test_code += "try:\n"
    
    # Pro každou proměnnou přidáme kontrolu
    for variable_name, variable_value in variable_patterns:
        # Kontrola existence proměnné se správným názvem
        test_code += f"    test = {variable_name}\n"  # Vyhodí NameError pokud proměnná neexistuje
        test_code += f"    expected_value = {variable_value}\n"  # Nejdřív vyhodnotíme výraz
        test_code += f"    if str({variable_name}) != str(expected_value):\n"
        test_code += f"        print(f'False # {variable_name} has wrong value')\n"
        test_code += "        raise ValueError\n"
    
    test_code += "    print('True')\n"
    test_code += "except NameError as e:\n"
    test_code += "    print(f'False # Variable not defined: {str(e)}')\n"
    test_code += "except Exception as e:\n"
    test_code += "    print(f'False # {str(e)}')\n"

    result = run_in_docker(test_code, username)
    return result.strip().lower() == 'true' 