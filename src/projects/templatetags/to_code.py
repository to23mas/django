from django import template


register = template.Library()

@register.filter("to_code")
def to_code(lines):
	result = ""
	for line in lines:
		result += line + "\n"

	return result
