from django import template


register = template.Library()

@register.filter("progress_css")
def progress_css(progress, project_no) -> str:

	status = progress[str(project_no)]

	if status == "open":
		return "bg-white"
	if status == "done":
		return "bg-green-400"

	return "bg-gray-800"
