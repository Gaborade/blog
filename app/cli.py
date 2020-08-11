import os
import click
from app import app

"""Using flask's native command line interface(click) to create
   commandline tools to speed up the workflow of translation"""

# os.system runs the command in the shell of your os. 
# when os.system runs and there is no error, it gives output of zero(0).
# however if an error occurs, it gives an output of 1. If error occurs,
# a runtime error is raised that stops the script

@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass



@translate.command()
@click.argument('lang')  #   to add a language argument to cli
def init(lang):
    """Initialize a new language"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Updates all the languages"""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    # if everything works perfectly the messages.pot file is deleted since it is a temporary file
    # and can be easily regenerated
    os.remove('messages.pot')



@translate.command()
def compile():
    """Compile all the languages into a messages.mo file"""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')