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

	habit_ct = ContentType.objects.get_or_create(app_label='demos', model='habit')[0]
	category_ct = ContentType.objects.get_or_create(app_label='demos', model='category')[0]
	post_ct = ContentType.objects.get_or_create(app_label='demos', model='post')[0]

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

	view_habit = Permission.objects.get_or_create(
		codename='view_habit',
		name='Can view habit',
		content_type=habit_ct
	)[0]

	view_category = Permission.objects.get_or_create(
		codename='view_category',
		name='Can view category',
		content_type=category_ct
	)[0]

	view_post = Permission.objects.get_or_create(
		codename='view_post',
		name='Can view post',
		content_type=post_ct
	)[0]

	maintainers.permissions.add(p1, p2)
	visitors.permissions.add(p2)
	students.permissions.add(view_habit, view_category, view_post)

	student, _ = User.objects.get_or_create(
		username='student',
		defaults={
			'email': 'student@example.com',
			'password': make_password('password'),
			'is_staff': True,
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
		username='visitor',
		defaults={
			'email': 'visitor@example.com',
			'password': make_password('password'),
		}
	)

	student.groups.add(students)
	visitor.groups.add(visitors)
	maintainer.groups.add(maintainers, students)

class Migration(migrations.Migration):
	dependencies = [
		('auth', '0001_initial'),
		('contenttypes', '0001_initial'),
		('demos', '0001_initial'),
	]

	operations = [
		migrations.RunPython(create),
	]
