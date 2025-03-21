import sys
sys.path.insert(0, '/var/www/api')

activate_this = '/home/ec2-user/api/venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application