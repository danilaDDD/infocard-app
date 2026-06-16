from drf_spectacular.openapi import AutoSchema


class PrimaryTokenAutoSchema(AutoSchema):
    def get_security(self):
        return [{'PrimaryTokenAuth': []}]
