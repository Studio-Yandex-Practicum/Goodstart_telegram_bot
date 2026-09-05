from asgiref.sync import sync_to_async

from schooling.models import Student, Teacher, TeacherStudentConversation


def record_conversation_message(
    teacher: Teacher, student: Student, sender_label: str, text: str,
) -> TeacherStudentConversation:
    """Сохраняет сообщение в переписке преподавателя и ученика."""
    conversation, _ = TeacherStudentConversation.objects.get_or_create(
        teacher=teacher, student=student,
    )
    conversation.add_message(sender_label, text)
    return conversation


record_conversation_message_async = sync_to_async(record_conversation_message)
