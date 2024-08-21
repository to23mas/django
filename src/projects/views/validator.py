from RestrictedPython.PrintCollector import PrintCollector
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

from domain.data.blockly.BlocklyStorage import get_blockly
from domain.data.blockly.enum.ExpectedTaskTypes import ExpectedTaskTypes


@login_required
def validate_python(request: HttpRequest) -> HttpResponse:
	"""list all projects"""
	code = str(request.POST.get('code', ''))
	blockly_id = str(request.POST.get('blockly_id', ''))
	course_db = str(request.POST.get('course_db', ''))
	blockly = get_blockly(course_db, int(blockly_id))

	if blockly == None:
		return JsonResponse({'status': 'error', 'message': 'Blockly not found'})

	match (blockly.expected_task):
		case ExpectedTaskTypes.PRINT.value:
			code_result = validate_python_code_print_safe(code)
			if code_result.endswith("\n"):
				code_result = code_result[:-1]
		case _:
			code_result = ''

	if blockly.expected_result == code_result:
		print('success')
		return JsonResponse({'status': 'success'})

	return JsonResponse({'status': 'error'})


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
