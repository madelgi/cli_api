import os

from cli_api.app import create_app


app = create_app(os.getenv('ENVIRONMENT'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
