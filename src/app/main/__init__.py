from flask import Blueprint


BP_NAME = 'main'
MODULE = __name__
TEMPLATE_FOLDER = 'templates'

# In Flask
# template_folder='templates'
# maps to OS path
# app/templates

bp = Blueprint(name=BP_NAME, import_name=MODULE, template_folder=TEMPLATE_FOLDER)

from app.main import routes
