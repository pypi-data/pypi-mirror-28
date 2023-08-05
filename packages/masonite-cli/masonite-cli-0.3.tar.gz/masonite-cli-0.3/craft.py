import click
import shutil
import sys
import importlib
import os
from subprocess import call

''' Append the projects directory to the sys path 
    This is used so project modules are importable like the config module
'''
sys.path.append(os.getcwd())

from config import application

@click.command()
@click.argument('command')
@click.argument('submodule', default=False)
@click.argument('function', default=False)
def cli(command, submodule, function):
    ''' Masonite Command Line Helper Tool '''
    found = False

    # run through providers array
    for key, provider in enumerate(application.PROVIDERS):
        if hasattr(importlib.import_module(provider), sys.argv[1]):
            print('\033[92mExecuting Command ...\033[0m')
            getattr(importlib.import_module(provider), sys.argv[1])()
            found = True
            break

    # run through these commands here
    if not found:
        try:
            globals()[command](command, submodule, function)
            found = True
        except Exception as e:
            print(e)

    # run through third party commands
    if not found:
        try:
            if function:
                module = importlib.import_module(
                    command + ".commands." + submodule)
                command = getattr(module, function)
            elif submodule:
                module = importlib.import_module(
                    command + ".commands." + submodule)
                command = getattr(module, submodule)
            else:
                module = importlib.import_module(
                    command + ".commands." + command)
                command = getattr(module, command)

            command()
            found = True
        except Exception as e:
            print(e)

def install(command, submodule, function):
    call(["pip3", "install", "-r", "requirements.txt"])

    # create the .env file if it does not exist
    if not os.path.isfile('.env'):
        shutil.copy('.env-example', '.env')


def serve(command, submodule, function):
    call(["gunicorn", "-w 2", "mine:application"])


def view(command, submodule, function):
    if os.path.isfile('resources/templates/' + sys.argv[2] + '.html'):
        print('\033[95m' + sys.argv[2] + ' View Exists!' + '\033[0m')
    else:
        open('resources/templates/' + sys.argv[2] + '.html', 'w+')
        print('\033[92m' + sys.argv[2] +
              ' View Created Successfully!' + '\033[0m')


def controller(command, submodule, function):
    if os.path.isfile('app/http/controllers/' + sys.argv[2] + '.py'):
        print('\033[95m' + sys.argv[2] + ' Controller Exists!' + '\033[0m')
    else:
        f = open('app/http/controllers/' + sys.argv[2] + '.py', 'w+')
        f.write("''' A Module Description '''\n")
        f.write('from masonite.view import view\n\n')
        f.write('class ' + sys.argv[2] + '(object):\n')
        f.write("    ''' Class Docstring Description '''\n\n")
        f.write('    def __init__(self):\n')
        f.write('        pass\n')

        print('\033[92m' + sys.argv[2] + ' Created Successfully!' + '\033[0m')


def makemigration(command, submodule, function):
    from app.Migrations import Migrations
    from config import database
    f = open('databases/migrations/' + sys.argv[2] + '.py', 'w+')
    f.write("''' A Migration File '''\n")
    f.write('from playhouse.migrate import *\n')
    f.write('from config import database\n')
    f.write('from app.Migrations import Migrations\n')
    f.write('import os\n\n')
    f.write("engine = database.ENGINES['default']\n")
    if database.DRIVER == 'mysql':
        f.write("migrator = MySQLMigrator(engine)\n\n")  # migration engine
    elif database.DRIVER == 'postgres':
        # migration engine
        f.write("migrator = PostgresqlMigrator(engine)\n\n")
    f.write("class " + sys.argv[3] + "(Model):\n    ")
    f.write("pass\n\n")
    f.write("engine.create_table(" + sys.argv[3] + ", True)\n\n")
    f.write("migrate(\n    ")
    f.write("migrator.add_column('" +
            sys.argv[3] + "', 'column_name', CharField(default=255)),\n")
    f.write(')\n\n')
    f.write('query=Migrations.update(batch=1).where(\n')
    f.write('    Migrations.migration == os.path.basename(__file__))\n')
    f.write('query.execute()\n')

    Migrations.create(migration=sys.argv[2] + '.py')

    print('\033[92mMigration ' + sys.argv[2] +
          '.py Created Successfully!' + '\033[0m')


def modelmigration(command, submodule, function):
    from app.Migrations import Migrations
    import subprocess
    f = open('databases/migrations/automatic_migration_for_' +
             sys.argv[2] + '.py', 'w+')
    f.write("''' A Migration File '''\n")
    f.write('import os\n\n')
    f.write('from app.Migrations import Migrations\n')
    f.write('from app.' + sys.argv[2] + ' import ' + sys.argv[2] + '\n')
    f.write('from config import database\n\n')

    f.write("ENGINE = database.ENGINES['default']\n\n")
    f.write("ENGINE.drop_table(" + sys.argv[2] + ", True)\n")
    f.write("ENGINE.create_table(" + sys.argv[2] + ", True)\n\n")
    f.write("QUERY = Migrations.update(batch=1).where(\n    ")
    f.write("Migrations.migration == os.path.basename(__file__))\n")
    f.write("QUERY.execute()\n")

    if '--model' in sys.argv:
        subprocess.call('python craft model ' + sys.argv[2], shell=True)

    Migrations.create(
        migration='automatic_migration_for_' + sys.argv[2] + '.py')
    print('\033[92mMigration ' + sys.argv[2] +
          '.py Created Successfully!' + '\033[0m')


def deploy(command, submodule, function):
    import subprocess
    from config import application
    output = subprocess.Popen(
        ['heroku', 'git:remote', '-a', application.NAME.lower()], stdout=subprocess.PIPE).communicate()[0]
    if not output:
        create_app = input(
            "\n\033[92mApp doesn't exist for this account. Would you like to craft one?\033[0m \n\n[y/n] > ")  # Python 2
        if 'y' in create_app:
            subprocess.call(['heroku', 'create', application.NAME.lower()])
            if '--local' in sys.argv:
                subprocess.call(['python', 'craft', 'deploy', '--local'])
            elif '--current' in sys.argv:
                subprocess.call(['python', 'craft', 'deploy', '--current'])
            else:
                subprocess.call(['python', 'craft', 'deploy'])
    else:
        if '--local' in sys.argv:
            subprocess.call(['git', 'push', 'heroku', 'master:master'])
        elif '--current' in sys.argv:
            subprocess.call(['git', 'push', 'heroku', 'HEAD:master'])
        else:
            subprocess.call(['git', 'push', 'heroku', 'master'])

def auth(command, submodule, function):
    f = open('routes/web.py', 'a')
    # add all the routes
    f.write('\nROUTES = ROUTES + [\n    ')
    f.write("Get().route('/login', 'LoginController@show'),\n    ")
    f.write("Get().route('/logout', 'LoginController@logout'),\n    ")
    f.write("Post().route('/login', 'LoginController@store'),\n    ")
    f.write("Get().route('/register', 'RegisterController@show'),\n    ")
    f.write("Post().route('/register', 'RegisterController@store'),\n    ")
    f.write("Get().route('/home', 'HomeController@show'),\n")
    f.write(']\n')

    # move controllers
    shutil.copyfile("kernal/auth/controllers/LoginController.py",
                    "app/http/controllers/LoginController.py")
    shutil.copyfile("kernal/auth/controllers/RegisterController.py",
                    "app/http/controllers/RegisterController.py")
    shutil.copyfile("kernal/auth/controllers/HomeController.py",
                    "app/http/controllers/HomeController.py")

    # move templates
    shutil.copytree("kernal/auth/templates/auth",
                    "resources/templates/auth")
