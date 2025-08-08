from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi

class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.security_definitions = {
            "Bearer": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
            }
        }
        schema.security = [{"Bearer": []}]
        return schema
