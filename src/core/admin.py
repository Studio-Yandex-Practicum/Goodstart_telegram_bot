from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    """Необходим для оверрайда списка приложений в админке."""

    def get_app_list(self, request, app_label=None):
        """Формирование собственного списка моделей в админке."""
        app_list = super().get_app_list(request)
        studyclass_dict = {}
        subject_dict = {}
        for app in app_list:
            if app['app_label'] == 'auth':
                app_list.remove(app)
            if app['app_label'] == 'schooling':
                for model in app['models']:
                    if model['object_name'] == 'StudyClass':
                        studyclass_dict = model
                    if model['object_name'] == 'Subject':
                        subject_dict = model
                app['models'] = [
                    model for model in app['models']
                    if model['object_name'] not in ['Subject', 'StudyClass']
                ]
        app_list.append(
            {
                'name': 'Предметы и классы',
                'app_label': 'schooling',
                'app_url': '/admin/schooling/',
                'has_module_perms': True,
                'models': [
                    studyclass_dict,
                    subject_dict,
                ],
            },
        )
        return app_list
