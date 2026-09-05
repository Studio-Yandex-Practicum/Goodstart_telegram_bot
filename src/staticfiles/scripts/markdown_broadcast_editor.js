document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('textarea.markdown-editor').forEach(function (el) {
        if (el.dataset.easymdeInitialized) {
            return;
        }
        el.dataset.easymdeInitialized = 'true';

        new EasyMDE({
            element: el,
            spellChecker: false,
            status: false,
            placeholder: 'Например: **Жирный текст**, *курсив*, [ссылка](https://example.com)',
            toolbar: [
                'bold', 'italic', 'link', 'code', '|',
                'preview', 'guide',
            ],
        });
    });
});
