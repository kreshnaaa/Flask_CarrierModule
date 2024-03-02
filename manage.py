# from flask import Flask
# from app import app
# from Modules.JobOppdesc import JobOppdesc_api
#  from flask_script import Manager


# manager = Manager(app)

# if __name__ =='__main__':
#     manager.run()

from flask_script import Manager
from app import app, db, mail
from Modules.JobOppdesc import JobOppdesc_api



manager = Manager(app)

if __name__ == '__main__':
    print("Test111")
    manager.run()

