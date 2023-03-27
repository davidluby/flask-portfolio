import sys
sys.path.insert(0, '/var/www/api')

activate = '/home/ec2-user/api/venv/bin/activate_this.py'
with open(activate) as file_:
    exec(file_.read(), dict(__file__=activate))

from app import app as application