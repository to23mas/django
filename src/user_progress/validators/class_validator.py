from ..docker_runner import run_in_docker
from django.db import models

def validate_python_code_class(code: str, username: str, expected_result: str) -> bool:
    expected_result = """
class Film(models.Model):
  length = models.IntegerField()
  name = models.CharField(max_length=255)
  date = models.DateField()
"""

    splitted_code = code.split('\n')
    splitted_expected_result = expected_result.split('\n')
    
    expected_class = [line for line in splitted_expected_result if line.startswith('class')][0]
    expected_content = [line for line in splitted_expected_result if line.startswith('  ')]
    
    class_found = expected_class in splitted_code
    
    class_content = []
    found_class = False
    for line in splitted_code:
        if line == expected_class:
            found_class = True
        elif found_class and line.startswith('  '):
            class_content.append(line)
        elif found_class and not line.startswith('  '):
            break
    
    test_results = class_found and len(class_content) == 3 and all(line in class_content for line in expected_content)
    
    return(test_results)
    