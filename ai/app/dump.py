# dump.py
from json import dumps

from main import app


print(dumps(app.openapi()))
