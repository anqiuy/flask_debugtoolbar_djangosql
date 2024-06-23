# Flask DebugToolbar DjangoSQL Panel

This is a custom panel for Flask DebugToolbar that displays Django SQL queries.

## Installation

Install the package using pip:

```bash
pip install Flask-DebugToolbar-DjangoSQL

## Usage

1. Make sure you have Flask and Flask-DebugToolbar installed in your project.

2. Add DjangoSQLPanel to your Flask DebugToolbar setup by including it in the DEBUG_TB_PANELS configuration:

```python
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

# Configuration for Flask-DebugToolbar
app.config['DEBUG_TB_PANELS'] = [
    'flask_debugtoolbar_djangosql.DjangoSQLPanel'
]

toolbar = DebugToolbarExtension(app)

if __name__ == "__main__":
    app.run()
```

3. Access your Flask application with the debug mode enabled (app.run(debug=True)) and open the debug toolbar in your browser to see Django SQL queries.

## Contributing
Feel free to contribute by forking the repository and sending pull requests. Please make sure to add tests for any new features or changes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.