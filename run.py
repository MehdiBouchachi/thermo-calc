#!/usr/bin/env python
# thermocalc/run.py
"""
Application entry point for ThermoCalc.
Initializes the Flask application and starts the development server.
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
