from ..docker_runner import run_in_docker

def validate_python_code_print(code: str, username: str) -> str:
    return run_in_docker(code, username) 