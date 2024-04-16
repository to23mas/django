from django import template


register = template.Library()

@register.filter("get_project_status")
def progress_status(progress, project) -> str:
    return progress[str(project)]
