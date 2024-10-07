from django import template


register = template.Library()

@register.filter("get_mongo_id")
def get_mongo_id(value):
	return str(value['_id'])
