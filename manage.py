#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Index, List
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Index=Index, List=List)


if __name__ == '__main__':
    manager.run()
