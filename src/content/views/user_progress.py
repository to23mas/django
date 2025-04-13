from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.tests.TestData import TestData
from domain.data.tests.TestStorage import TestStorage

@login_required
def admin_users_overview(request: HttpRequest) -> HttpResponse:
    students_group = Group.objects.get(name='students')
    users = User.objects.filter(groups=students_group)

    # Handle search queries
    username_query = request.GET.get('q', '')
    email_query = request.GET.get('email', '')

    if username_query:
        users = users.filter(username__icontains=username_query)
    if email_query:
        users = users.filter(email__icontains=email_query)

    breadcrumbs = [{'Home': '/admin/'}, {'User progress': '#'}]
    return render(request, "content/progress/user_progress.html", {
      'users': users,
      'breadcrumbs': breadcrumbs,
    })

@login_required
def course_progress_overview(request: HttpRequest) -> HttpResponse:
    course_storage = CourseStorage()
    courses = course_storage.find_courses()


    breadcrumbs = [{'Home': '/admin/'}, {'Course progress': '#'}]
    return render(request, "content/progress/course_progress.html", {
      'courses': courses,
      'breadcrumbs': breadcrumbs,
    })

@login_required
def course_progress_detail(request: HttpRequest, course_id: str) -> HttpResponse:
    course_storage = CourseStorage()
    progress_storage = ProgressStorage()
    test_storage = TestStorage()
    course = course_storage.get_course_by_id(course_id)
    
    students_group = Group.objects.get(name='students')
    total_students = User.objects.filter(groups=students_group).count()
    
    enrolled_students = progress_storage.find_users_by_course(course.database)
    enrolled_students_count = len(enrolled_students)

    enrollment_stats = {
        'total_students': total_students,
        'enrolled_count': enrolled_students_count,
        'enrolled_students': enrolled_students,
        'enrollment_rate': (enrolled_students_count / total_students * 100) if total_students > 0 else 0
    }


    tests = test_storage.find_tests(course.database)
    breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/course_progress'}, {'Courses': '#'}]
    context = {
        'tests': tests,
        'course': course,
        'breadcrumbs': breadcrumbs,
        'enrollment_stats': enrollment_stats,
    }
    return render(request, "content/progress/course_progress_detail.html", context)


@login_required
def admin_user_progress_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    course_storage = CourseStorage()
    courses = course_storage.find_courses()

    progress_storage = ProgressStorage()
    user_progress = []

    if courses is not None:
        for course in courses:
            progress = progress_storage.get_user_progress_by_course(username, course.database)
            if progress:
                progress['course_id'] = course.id
                progress['course_title'] = course.title
                progress['course_database'] = course.database
                done = 0
                all = 0
                for _, chapters in progress['chapters'].items():
                  for _, ch in chapters.items():
                    if ch == 'done':
                      done += 1
                    all += 1
                progress['percentage'] = (done/all) * 100
                user_progress.append(progress)


    breadcrumbs = [{'Home': '/admin/'}, {'Users': '/admin/content/users_progress'}, {'Courses': '#'}]
    context = {
        'user': user,
        'breadcrumbs': breadcrumbs,
        'user_progress': user_progress,
    }
    return render(request, "content/progress/user_progress_detail.html", context)


@login_required
def admin_user_progress_course_detail(request: HttpRequest, username: str, course: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    progress_storage = ProgressStorage()
    course_storage = CourseStorage()
    chapter_storage = ChapterStorage()
    test_storage = TestStorage()

    course_data = course_storage.get_course_by_id(course)
    if not course_data:
        raise Http404("Course not found")

    progress = progress_storage.get_user_progress_by_course(username, course_data.database)
    if not progress:
        progress = {'chapters': {}, 'tests': []}

    # Add lesson_id information to chapters
    for project_id, chapters in progress['chapters'].items():
        project = ProjectStorage().get_project(course_data.database, {'_id': int(project_id)})
        if project:
            new_chapters = {}
            for chapter_id, status in chapters.items():
                chapter = chapter_storage.get_chapter_by_id(int(chapter_id), course_data.database, project.database)
                if chapter:
                    new_chapters[chapter_id] = {
                        'status': status,
                        'lesson_id': chapter.lesson_id,
                        'unlock_type': chapter.unlock_type,
                    }
            progress['chapters'][project_id] = new_chapters

    # Load test metadata and combine with progress
    tests = test_storage.find_tests(course_data.database)

    breadcrumbs = [{'Home': '/admin/'}, {'Users': '/admin/content/users_progress'}, {f'{username}': f'/admin/content/users_progress/{username}'}, {'View': '#'}]
    context = {
        'user': user,
        'c': course_data,
        'progress': progress,
        'tests': tests,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, "content/progress/user_progress_course_detail.html", context)

