from django.contrib.auth.hashers import make_password
from django.db import migrations

def create(apps, schema_editor):
	Group = apps.get_model("auth", "Group")
	Permission = apps.get_model("auth", "Permission")
	ContentType = apps.get_model("contenttypes", "ContentType")
	User = apps.get_model('auth', 'User')

	maintainers, _ = Group.objects.get_or_create(name="Maintainers - Django")
	students, _ = Group.objects.get_or_create(name="Students")

	content_type, _ = ContentType.objects.get_or_create(
		app_label="users",
		model="django"
	)

	p1, _  = Permission.objects.get_or_create(
		codename="write",
		name="write",
		content_type=content_type
	)

	Permission.objects.get_or_create(
		codename="read",
		name="read",
		content_type=content_type
	)
	maintainers.permissions.add(p1)

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
	maintainer.is_staff

	student.groups.add(students)
	maintainer.groups.add(maintainers)

class Migration(migrations.Migration):
	operations = [
		migrations.RunPython(create),
	]
