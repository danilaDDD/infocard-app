import os


def test_env():
    assert os.environ.get('ENV') == 'test'

def test_settings():
    from django.conf import settings

    assert settings is not None

    db_settings = settings.DATABASES.get('default')
    assert db_settings is not None

    assert 'test' in db_settings['NAME']
    assert db_settings['ENGINE'] == 'django.db.backends.postgresql'