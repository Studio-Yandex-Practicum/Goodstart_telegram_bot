from django.core.management.base import BaseCommand
from schooling.models import Lesson, LessonGroup

class Command(BaseCommand):
    help = 'Назначает занятиям группу на основе ученика'

    def handle(self, *args, **kwargs):
        lessons_without_group = Lesson.objects.filter(group__isnull=True)

        if not lessons_without_group.exists():
            self.stdout.write(self.style.SUCCESS('Нет занятий без группы.'))
            return

        count = 0
        for lesson in lessons_without_group:
            group, created = LessonGroup.objects.get_or_create(student=lesson.student_id)
            lesson.group = group
            lesson.save(update_fields=['group'])
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно обновлено {count} занятий.'))
