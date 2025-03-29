from ..docker_runner import run_in_docker

def validate_python_code_variable(code: str, username: str, expected_result: str) -> bool:
    variable_name, expected_value = expected_result.split(',')
    expected_value = expected_value.strip().strip("'\"")
    
    test_code = code + "\n\n"
    test_code += "try:\n"
    test_code += f"    print(str({variable_name} == '{expected_value}'))\n"
    test_code += "except NameError:\n"
    test_code += "    print('False')\n"

    result = run_in_docker(test_code, username)
    return result.strip().lower() == 'true' 