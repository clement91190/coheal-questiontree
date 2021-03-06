import os
from questiontree.server import app
from flask import render_template

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  debug = (port == 5000)
  app.run(host='0.0.0.0', port=port, debug=debug)
