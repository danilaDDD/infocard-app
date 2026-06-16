SPECTACULAR_SETTINGS = {
    'TITLE': 'Infocard API',
    'DESCRIPTION': 'API документация для Infocard проекта',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SECURITY': [{'PrimaryTokenAuth': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'PrimaryTokenAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-Access-Token',
                'description': 'Первичный токен доступа',
            }
        }
    },
}