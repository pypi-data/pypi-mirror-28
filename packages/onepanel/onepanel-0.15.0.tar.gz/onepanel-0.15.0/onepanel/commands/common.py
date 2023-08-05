import os
import click

from onepanel.commands.login import login_required
from onepanel.commands.projects import projects_clone
from onepanel.commands.datasets import datasets_clone
from onepanel.gitwrapper import GitWrapper

def get_entity_type(path):
    dirs = path.split('/')
    entity_type = None
    if len(dirs) == 3:
        account_uid, dir, uid = dirs
        if dir == 'projects':
            entity_type = 'project'
        elif dir == 'datasets':
            entity_type = 'dataset'
    return entity_type

@click.command('clone', help='Clone <account_uid>/<uid> project from server.')
@click.argument('path', type=click.Path())
@click.argument('directory', type=click.Path(), required=False)
@click.option(
    '-i', '--include',
    type=str,
    help='Regex pattern to include lfs objects'
)
@click.option(
    '-x', '--exclude',
    type=str,
    help='Regex pattern to exclude lfs objects (Default to * for projects)'
)
@click.pass_context
@login_required
def clone(ctx, path, directory, include, exclude):
    entity_type = get_entity_type(path)
    if entity_type == 'project':
        projects_clone(ctx, path, directory, include, exclude)
    elif entity_type == 'dataset':
        datasets_clone(ctx, path, directory, include, exclude)
    else:
        click.echo('Invalid project or dataset path.')


@click.command('push', help='Push changes to onepanel')
@click.pass_context
@login_required
def push(ctx):
    home = os.getcwd()
    GitWrapper().push(home)

@click.command('pull', help='Pull changes from onepanel (fetch and merge)')
@click.pass_context
@login_required
def pull(ctx):
    home = os.getcwd()
    GitWrapper().pull(home)
