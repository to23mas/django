from django import template
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.lessons.LessonStorage import LessonStorage

register = template.Library()

@register.simple_tag
def get_chapter_title(course_id, project_id, chapter_id):
    chapter_storage = ChapterStorage()
    course_storage = CourseStorage()
    project_storage = ProjectStorage()

    course = course_storage.get_course_by_id(str(course_id))
    if not course:
        return f"Chapter {chapter_id}"

    project = project_storage.get_project(course.database, {'_id': int(project_id)})
    if not project:
        return f"Chapter {chapter_id}"

    chapter = chapter_storage.get_chapter_by_id(int(chapter_id), course.database, project.database)
    return chapter.title if chapter else f"Chapter {chapter_id}"

@register.simple_tag
def get_project_name(course_id, project_id):
    course_storage = CourseStorage()
    project_storage = ProjectStorage()

    course = course_storage.get_course_by_id(str(course_id))
    if not course:
        return f"Project {project_id}"

    project = project_storage.get_project(course.database, {'_id': int(project_id)})
    return project.title if project else f"Project {project_id}"

@register.simple_tag
def get_lesson_title(course_id, project_id, lesson_id):
    course_storage = CourseStorage()
    project_storage = ProjectStorage()
    lesson_storage = LessonStorage()

    course = course_storage.get_course_by_id(str(course_id))
    if not course:
        return f"Lesson {lesson_id}"

    project = project_storage.get_project(course.database, {'_id': int(project_id)})
    if not project:
        return f"Lesson {lesson_id}"

    lesson = lesson_storage.get_lesson(int(lesson_id), course.database, project.database)
    return lesson.title if lesson else f"Lesson {lesson_id}"

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.filter
def max_value(value_list):
    if not value_list:
        return 0
    return max(value_list)

@register.filter
def find_test_progress(test_list, test_id):
    for test in test_list:
        if str(test.get('test_id')) == str(test_id):
            return test
    return None
