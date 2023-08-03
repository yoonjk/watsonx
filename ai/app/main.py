from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from router import route

tags_metadata = [
    {
        "name": "watsonx",
        "description": "Users Operations with Watsonx.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(servers=[{"url": "http://example.com", "description": "test"}], openapi_tags=tags_metadata)


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Custom title",
        version="3.0.1",
        description="Custom description",
        routes=app.routes
    )
    http_methods = ["post", "get", "put", "delete"]
    # look for the error 422 and removes it
    for method in openapi_schema["paths"]:
        for m in http_methods:
            try:
                del openapi_schema["paths"][method][m]["responses"]["422"]
            except KeyError:
                pass
            
    for schema in list(openapi_schema["components"]["schemas"]):
        if schema == "HTTPValidationError" or schema == "ValidationError":
            del openapi_schema["components"]["schemas"][schema]

    app.openapi_schema = openapi_schema

    return app.openapi_schema

app.openapi = custom_openapi 
app.include_router(route)

