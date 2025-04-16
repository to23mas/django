from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.tests.TestStorage import TestStorage
from tests.models import TestResult
from collections import defaultdict

@login_required
def test_results_detail(request, course_id, test_id):
    course_storage = CourseStorage()
    test_storage = TestStorage()
    course = course_storage.get_course_by_id(course_id)
    if not course:
        raise Http404("Course not found")
    
    # Get all test results for this test
    test_results = TestResult.objects.filter(test_id=test_id).order_by('timestamp')
    test_data = test_storage.get_test(course.database, int(test_id))
    
    # Group results by attempt
    attempt_results = defaultdict(list)
    for result in test_results:
        attempt_results[result.attempt_number].append(result)
    
    # Process attempt statistics
    attempts = []
    for attempt_number, results in sorted(attempt_results.items()):
        total_questions = len(results)
        correct_answers = sum(1 for r in results if r.is_correct)
        correct_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Process question statistics for this attempt
        question_stats = defaultdict(lambda: {
            'total_attempts': 0,
            'correct_attempts': 0,
            'partially_correct_attempts': 0,
            'answer_distribution': defaultdict(int),
            'has_multiple_correct': False,
            'answer_status': defaultdict(lambda: {'count': 0, 'is_partial': False}),
            'question_type': None,
            'correct_answers': set(),
            'selected_answers': [],
            'is_partially_correct': False
        })
        
        for result in results:
            question_id = str(result.question_id)
            question_stats[question_id]['total_attempts'] += 1
            question_stats[question_id]['question_type'] = result.question_type
            question_stats[question_id]['correct_answers'].update(result.correct_answers)
            question_stats[question_id]['selected_answers'] = result.selected_answers
            
            # Check if this question has multiple correct answers
            if len(result.correct_answers) > 1:
                question_stats[question_id]['has_multiple_correct'] = True
                
                # For multiple correct answers, check if the answer is partially correct
                selected_set = set(result.selected_answers)
                correct_set = set(result.correct_answers)
                question_stats[question_id]['is_partially_correct'] = len(selected_set & correct_set) > 0 and not result.is_correct
            
            # Track correct answers
            if result.is_correct:
                question_stats[question_id]['correct_attempts'] += 1

            if result.is_partially_correct:
                question_stats[question_id]['partially_correct_attempts'] += 1
            
            # Track answer distribution
            if not result.selected_answers:
                question_stats[question_id]['answer_distribution']['did not answered'] = question_stats[question_id]['answer_distribution'].get('no_answer', 0) + 1
            else:
                for answer in result.selected_answers:
                    question_stats[question_id]['answer_distribution'][str(answer)] += 1
        
        # Convert question stats to list
        question_stats_list = []
        for question_id, stats in question_stats.items():
            question_stats_list.append({
                'question_id': question_id,
                'total_attempts': stats['total_attempts'],
                'correct_attempts': stats['correct_attempts'],
                'correct_percentage': (stats['correct_attempts'] / stats['total_attempts'] * 100) if stats['total_attempts'] > 0 else 0,
                'partially_correct_percentage': (stats['partially_correct_attempts'] / stats['total_attempts'] * 100) if stats['total_attempts'] > 0 else 0,
                'answer_distribution': dict(stats['answer_distribution']),
                'has_multiple_correct': stats['has_multiple_correct'],
                'question_type': stats['question_type'],
                'correct_answers': list(stats['correct_answers']),
                'selected_answers': stats['selected_answers'],
                'is_correct': stats['correct_attempts'] > 0,
                'is_partially_correct': stats['is_partially_correct']
            })
        
        attempts.append({
            'attempt_number': attempt_number,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'correct_percentage': correct_percentage,
            'results': results,
            'question_stats': question_stats_list,
        })
    
    breadcrumbs = [
        {'Home': '/admin/'},
        {'Courses': '/admin/content/course_progress'},
        {course.title: f'/admin/content/course_progress/{course_id}'},
        {'Test Results': '#'}
    ]
    
    context = {
        'test_data': test_data,
        'course': course,
        'test_id': test_id,
        'attempts': attempts,
        'breadcrumbs': breadcrumbs
    }
    
    return render(request, 'content/progress/test_results_detail.html', context) 