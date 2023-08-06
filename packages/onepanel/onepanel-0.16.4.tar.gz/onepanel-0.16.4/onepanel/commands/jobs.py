"""
Job commands
"""
import os
import sys
import json
import subprocess

import click
import websocket

from onepanel.commands.base import APIViewController
from onepanel.commands.login import login_required


class JobViewController(APIViewController):

    def __init__(self, conn):

        super(JobViewController, self).__init__(conn)

        project = self.get_project()

        self.endpoint = '{root}/accounts/{account_uid}/projects/{project_uid}/jobs'.format(
            root=self.conn.URL,
            account_uid=project.account_uid,
            project_uid=project.project_uid
        )


@click.group(help='Job commands group')
@click.pass_context
def jobs(ctx):
    ctx.obj['vc'] = JobViewController(ctx.obj['connection'])
    ctx.obj['project'] = ctx.obj['vc'].get_project()

@jobs.command('create', help='Execute a command on a remote machine in the current project')
@click.argument(
    'command',
    type=str
)
@click.option(
    '-m', '--machine-type',
    type=str,
    required=True,
    help='Machine type ID'
)
@click.option(
    '-e', '--environment',
    type=str,
    required=True,
    help='Instance template ID'
)
@click.pass_context
@login_required
def create_job(ctx, command, machine_type, environment):
    new_job = {
        'command': command,
        'machineType': {
            'uid': machine_type
        },
        'instanceTemplate': {
            'uid': environment
        }
    }

    created_job = ctx.obj['vc'].post(post_object=new_job)

    if created_job:
        print('New job created: {}'.format(created_job['uid']))

    return


@jobs.command('list', help='Show commands executed on remote machines')
@click.option(
    '-a', '--all',
    type=bool,
    is_flag=True,
    default=False,
    help='Include finished commands'
)
@click.pass_context
@login_required
def list_jobs(ctx, all):
    vc = ctx.obj['vc']
    items = vc.get(params='?running=true' if not all else '')

    if items is None or len(items) == 0:
        print('No jobs found. Use "--all" flag to retrieve completed jobs.')
        return

    vc.print_items(items, fields=['uid', 'command'], field_names=['ID', 'COMMAND'])

@jobs.command('stop', help='Stop a job')
@click.argument(
    'job_uid',
    type=str
)
@click.pass_context
@login_required
def kill_job(ctx, job_uid):
    ctx.obj['vc'].delete(job_uid, field_path='/active', message_on_success='Job stopped', message_on_failure='Job not found')

@jobs.command('logs', help='Show a log of the command')
@click.argument(
    'job_uid',
    type=str
)
@click.pass_context
@login_required
def job_logs(ctx, job_uid):

    conn = ctx.obj['connection']
    project = ctx.obj['project']

    url = '{root}/accounts/{account_uid}/projects/{project_uid}/jobs/{job_uid}/logs'.format(
        root=conn.URL,
        account_uid=project.account_uid,
        project_uid=project.project_uid,
        job_uid=job_uid
    )

    r = conn.get(url)
    c = r.status_code

    if c == 200:

        resp_text = r.text
        # Response contains escaped characters. E.g., r.content is:
        # b'"rm: cannot remove \'README.md\': No such file or directory\\n"'
        # Clean them first
        log_lines = resp_text[1:-1].split('\\n')
        print('\n'.join(log_lines), end='')
        return True

    elif c == 400:

        # Streaming via WebSocket
        # See https://pypi.python.org/pypi/websocket-client/

        streaming_url = '{ws_root}/accounts/{account_uid}/projects/{project_uid}/jobs/{job_uid}/logs?access_token={token}&tail_lines=1'.format(
            ws_root='wss://c.onepanel.io/api',
            account_uid=project.account_uid,
            project_uid=project.project_uid,
            job_uid=job_uid,
            token=conn.token
        )

        ws = websocket.WebSocketApp(
            url=streaming_url,
            header=conn.headers,
            on_message=lambda ws, message: print(message, end=''),
            on_error=print
        )
        ws.run_forever()

    elif c == 404:

        print('Job not found: {}'.format(job_uid))

    else:

        print('Error: {}'.format(c))

    return False

def jobs_download_output(ctx, path, directory):
    #
    # Resource
    #
    dirs = path.split('/')

    # Job output: Method 2
    # <account_uid>/projects/<project_uid>/jobs/<job_uid>
    if len(dirs) == 5:
        try:
            account_uid, projects_dir, project_uid, jobs_dir, job_uid = dirs
            assert (projects_dir == 'projects') and (jobs_dir == 'jobs')
        except:
            print('Incorrect job path')
            return None
    else:
        print('Incorrect job uid')
        return None

    #
    # Directory
    #
    if directory is None or directory == '.':
        home = os.getcwd()
    else:
        home = os.path.join(os.getcwd(), directory)

    #
    # Clone
    #
    cmd = (
            'rm -rf .onepanel_download'   # Cleaning after previous errors to avoid "is not an empty directory" error
            ' && git lfs clone --quiet -b job-{job_uid} https://{host}/{account_uid}/{project_uid}-output.git .onepanel_download'
            ' && cp -r .onepanel_download/jobs/{job_uid}/output/ {dir}'
            ' && rm -rf .onepanel_download'
        ).format(
            host='git.onepanel.io',
            account_uid=account_uid,
            project_uid=project_uid,
            job_uid=job_uid,
            dir=home
        )
    p = subprocess.Popen(cmd, shell=True)
    p.wait()

    if p.returncode == 0:
        print('Job output downloaded to: {dir}'.format(dir=home))
        return True
    else:
        print('Unable to download')
        return False

@jobs.command('delete', help='Delete a job')
@click.argument(
    'job_uid',
    type=str
)
@click.pass_context
@login_required
def delete_job(ctx, job_uid):
    ctx.obj['vc'].delete(job_uid, message_on_success='Job deleted', message_on_failure='Job not found')