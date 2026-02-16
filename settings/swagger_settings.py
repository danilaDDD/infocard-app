from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample

SPECTACULAR_SETTINGS = {
    'TITLE': 'Infocard API',
    'DESCRIPTION': 'API документация для Infocard проекта',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SECURITY': [
            {
                'name': 'Access Token',
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-Access-Token',
                'description': 'Дополнительный токен для специальных операций',
            },
        ],
}