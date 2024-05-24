from django.contrib import admin

from schooling.models import Student, Teacher, Subject, StudyClass, Lesson


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Управление преподавателями."""

    list_display = ('name', 'surname', 'get_competences')

    def get_competences(self, obj):
        """Return competences."""
        return '\n'.join([c.competence for c in obj.competence.all()])


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление студентами."""

    list_display = ('name', 'surname', 'paid_lessons')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Управление школьными предметами."""

    list_display = ('name',)
    exclude = ('subject_key',)


@admin.register(StudyClass)
class StudyClassAdmin(admin.ModelAdmin):
    """Управление учебными классами."""

    list_display = ('study_class_name', 'study_class_number')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Управление занятиями."""

    list_display = (
        'name', 'subject', 'teacher_id', 'student_id',
        'datetime_start', 'datetime_end', 'is_passed', 'test_lesson',
    )
    list_filter = (
        'subject', 'teacher_id', 'student_id',
        'datetime_start', 'is_passed', 'test_lesson',
    )
    search_fields = (
        'name', 'subject__name',
        'teacher_id__name', 'student_id__name',
    )
