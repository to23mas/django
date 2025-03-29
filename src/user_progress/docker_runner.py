import os
import docker
from django.conf import settings

def run_in_docker(code: str, username: str) -> str:
    os.makedirs('./tmp', exist_ok=True)
    os.chmod('./tmp', 0o777)

    file_path = os.path.join('./tmp', f'{username}.py')
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(code)
    os.chmod(file_path, 0o777)

    client = docker.from_env()

    container = client.containers.run(
        image="restricted_python",
        volumes={f'{settings.VALIDATOR_DIR}/{username}.py': {"bind": "/sandbox/file.py", "mode": "ro"}},
        stdout=True,
        stderr=True,
        remove=True,
        detach=True,
        command="python /sandbox/run_code.py",
        cpu_count=1,
        mem_limit="128m",
        memswap_limit="256m",
        cpu_shares=512
    )

    try:
        container.wait(timeout=10)
        logs = []
        for log in container.logs(stream=True):
            logs.append(log.decode('utf-8'))
    except Exception:
        container.kill()
        raise Exception('Container took too long')
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return logs[0] 