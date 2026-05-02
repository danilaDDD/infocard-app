import os

import pytest


@pytest.mark.initial
class TestSettings:
    def test_env(self):
        assert os.environ.get('ENV') == 'test'

    def test_settings_loaded(self):
        from django.conf import settings

        assert settings is not None

    def test_database_engine(self):
        from django.conf import settings

        db = settings.DATABASES.get('default')
        assert db is not None
        assert db['ENGINE'] == 'django.db.backends.postgresql'

    def test_database_name_contains_test(self):
        from django.conf import settings

        db = settings.DATABASES.get('default')
        assert 'test' in db['NAME']