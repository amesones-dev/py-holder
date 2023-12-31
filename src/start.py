"""Run a Flask App using the create_app factory"""
import os

from app import create_app
app = create_app()

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(host='0.0.0.0', port=int(server_port))
