from ..docker_runner import run_in_docker

def validate_python_code_function(code: str, username: str, expected_result: str) -> str:
    lines = expected_result.strip().split('\n')
    function_name = lines[0].strip()

    test_cases = []
    for line in lines[1:]:
        if ':' in line:
            params, expected = line.split(':')
            params = [int(p.strip()) for p in params.split(',')]
            expected = int(expected.strip().rstrip(';'))
            test_cases.append((params, expected))

    test_code = code + "\n\n# Test cases\n"
    test_code += "test_results = True\n"
    for params, expected in test_cases:
        params_str = ", ".join(str(p) for p in params)
        test_code += f"test_results = test_results and {function_name}({params_str}) == {expected}\n"
    test_code += "print(test_results)"

    return run_in_docker(test_code, username) 