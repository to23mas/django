import subprocess
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def validate_python(request: HttpRequest) -> HttpResponse:
	"""list all projects"""
	username = request.user.username #type: ignore
	try:
		# Write the code to a temporary file
		code = str(request.POST.get('code', ''))
		expected_output = "print('Hello World')"

		# TODO
		exec(code, {});
		with open('temp_script.py', 'w') as f:
			f.write(code)
			print(code)

			# Execute the code and capture the output
			result = subprocess.run(['python3', 'temp_script.py'], capture_output=True, text=True)

			print(result.stdout);
			print(result);
			# Check if the output matches the expected output
			if result.stdout.strip() == expected_output:
				return JsonResponse({'status': 'success', 'message': 'Code is correct!'})
			else:
				return JsonResponse({'status': 'error', 'message': 'Code is incorrect!', 'output': result.stdout})
	except Exception as e:
		return JsonResponse({'status': 'error', 'message': str(e)})

	return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

