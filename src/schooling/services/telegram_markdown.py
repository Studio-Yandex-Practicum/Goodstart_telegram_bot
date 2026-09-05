# Конвертация текста, набранного в обычном Markdown (**жирный**,
# *курсив*, `код`, [текст](ссылка)), в Telegram MarkdownV2.
#
# Зачем это нужно: у Telegram свой диалект Markdown — экранировать
# нужно почти все спецсимволы (. ! - ( ) и т.д.), а разметка вроде
# **жирный** там не поддерживается (жирный — это *жирный*, один символ
# с каждой стороны). Если просто отправить сырой Markdown с
# parse_mode='MarkdownV2', Telegram либо не отформатирует текст, либо
# вернёт ошибку из-за неэкранированных символов. Поэтому админ пишет
# в привычном Markdown, а перед отправкой мы сами находим разметку и
# конвертируем её в формат Telegram, экранируя всё остальное.

import re

# Символы, которые Telegram MarkdownV2 требует экранировать вне разметки.
_SPECIAL_CHARS = r'_*[]()~`>#+-=|{}.!\\'
_ESCAPE_RE = re.compile('([%s])' % re.escape(_SPECIAL_CHARS))

_ENTITY_RE = re.compile(
    r'(?P<bold>\*\*(?P<bold_text>.+?)\*\*)'
    r'|(?P<italic>(?<!\*)\*(?P<italic_text>[^*\n]+?)\*(?!\*))'
    r'|(?P<code>`(?P<code_text>[^`\n]+?)`)'
    r'|(?P<link>\[(?P<link_text>[^\]\n]+?)\]\((?P<link_url>[^()\s]+)\))',
    re.DOTALL,
)


def _escape(text):
    """Экранирует спецсимволы MarkdownV2 в обычном (не размеченном) тексте."""
    return _ESCAPE_RE.sub(r'\\\1', text)


def _escape_link_url(url):
    """Экранирует URL внутри `[текст](ссылка)` по правилам MarkdownV2."""
    return url.replace('\\', '\\\\').replace(')', '\\)')


def markdown_to_telegram_markdown_v2(text):
    """
    Конвертирует текст с обычной Markdown-разметкой в Telegram MarkdownV2.

    Поддерживаемая разметка: **жирный**, *курсив*, `код`,
    [текст ссылки](url). Всё остальное экранируется, чтобы Telegram
    не отклонил сообщение из-за спецсимволов (. ! - и т.п.).
    """
    parts = []
    pos = 0

    for match in _ENTITY_RE.finditer(text):
        parts.append(_escape(text[pos:match.start()]))

        if match.group('bold'):
            parts.append('*%s*' % _escape(match.group('bold_text')))
        elif match.group('italic'):
            parts.append('_%s_' % _escape(match.group('italic_text')))
        elif match.group('code'):
            parts.append('`%s`' % match.group('code_text').replace('\\', '\\\\'))
        elif match.group('link'):
            link_text = _escape(match.group('link_text'))
            link_url = _escape_link_url(match.group('link_url'))
            parts.append('[%s](%s)' % (link_text, link_url))

        pos = match.end()

    parts.append(_escape(text[pos:]))
    return ''.join(parts)
