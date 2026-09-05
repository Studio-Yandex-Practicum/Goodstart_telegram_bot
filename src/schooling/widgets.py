from django import forms


class MarkdownEditorWidget(forms.Textarea):
    """
    Textarea с подключённым EasyMDE — даёт менеджеру панель форматирования
    и превью прямо в админке при редактировании текста рассылки.

    Превью показывает обычный Markdown (библиотека EasyMDE его не знает
    про диалект Telegram), итоговая конвертация в Telegram MarkdownV2
    происходит на сервере перед отправкой — см.
    schooling/services/telegram_markdown.py.
    """

    def __init__(self, attrs=None):
        default_attrs = {'class': 'markdown-editor', 'rows': 12}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    class Media:
        css = {
            'all': ('vendor/easymde/easymde.min.css',),
        }
        js = (
            'vendor/easymde/easymde.min.js',
            'scripts/markdown_broadcast_editor.js',
        )
