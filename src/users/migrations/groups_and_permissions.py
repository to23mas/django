from django.contrib.auth.hashers import make_password
from django.db import migrations

def create(apps, schema_editor):
	Group = apps.get_model("auth", "Group")
	Permission = apps.get_model("auth", "Permission")
	ContentType = apps.get_model("contenttypes", "ContentType")
	User = apps.get_model('auth', 'User')

	maintainers, _ = Group.objects.get_or_create(name="django-maintainers")
	students, _ = Group.objects.get_or_create(name="students")
	visitors, _ = Group.objects.get_or_create(name="visitors")

	content_type, _ = ContentType.objects.get_or_create(
		app_label="users",
		model="django"
	)

	p1, _  = Permission.objects.get_or_create(
		codename="write",
		name="write",
		content_type=content_type
	)

	p2, _ = Permission.objects.get_or_create(
		codename="read",
		name="read",
		content_type=content_type
	)

	maintainers.permissions.add(p1)
	maintainers.permissions.add(p1, p2)
	visitors.permissions.add(p2)

	student, _ = User.objects.get_or_create(
		username='student',
		defaults={
			'email': 'student@example.com',
			'password': make_password('password'),
		}
	)

	maintainer, _ = User.objects.get_or_create(
		username='maintainer',
		defaults={
			'email': 'maintainer@example.com',
			'password': make_password('password'),
			'is_staff': True,
		}
	)

	visitor, _ = User.objects.get_or_create(
		username='maintainer',
		defaults={
			'email': 'maintainer@example.com',
			'password': make_password('password'),
			'is_staff': True,
		}
	)

	maintainer.is_staff
	visitor.is_staff

	student.groups.add(students)
	visitor.groups.add(visitors)
	maintainer.groups.add(maintainers)
	maintainer.groups.add(students)

class Migration(migrations.Migration):
	operations = [
		migrations.RunPython(create),
	]
