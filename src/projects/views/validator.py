from RestrictedPython.PrintCollector import PrintCollector
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

from domain.data.blockly.BlocklyStorage import get_blockly



@login_required
def validate_python(request: HttpRequest) -> HttpResponse:
	"""list all projects"""
	username = request.user.username #type: ignore

	code = str(request.POST.get('code', ''))
	blockly_id = str(request.POST.get('blockly_id', ''))
	course_db = str(request.POST.get('course_db', ''))

	print(request.POST)
	blockly = get_blockly(course_db, int(blockly_id))

	if blockly == None:
		pass # sent error

	print(course_db)
	print(blockly_id)
	print(blockly)
	# TODO add valid result to blockly definition
	code_print_result = validate_python_code_print_safe(code)

	return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def validate_python_code_print_safe(code):
	print_result = 'printed_result_validation_string_collection_grabber'
	code += f'\n{print_result} = printed'
	restricted_locals = {}
	restricted_globals = {
		"__builtins__": safe_builtins,
		"_print_": PrintCollector,
		"_getattr_":  getattr,
	}

	byte_code = compile_restricted(code, '<string>', 'exec')
	exec(byte_code, restricted_globals, restricted_locals)
	output = restricted_locals[print_result]

	return output
