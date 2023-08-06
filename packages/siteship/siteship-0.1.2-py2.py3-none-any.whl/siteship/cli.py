# -*- coding: utf-8 -*-

"""Console script for siteship."""

import click
import configparser
import os
import shutil
import tempfile
import requests

# Py2 / py3 support
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


from tinynetrc import Netrc
try:
    netrc = Netrc()
except FileNotFoundError:
    netrc = None


API_URL = 'https://siteship.sh/api/'
# API_URL = 'http://localhost:8000/api/'


def render_validation_errors(response):
    for field, errors in response.json().items():
        click.echo('* {} - {}'.format(
            click.style(field, fg='red'),
            ', '.join(errors) if isinstance(errors, type([])) else errors
        ))


@click.group()
def siteship(args=None):
    """Console script for siteship."""
    click.echo("Replace this message by putting your code into "
               "siteship.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


@siteship.command()
@click.option('--path', help='path to the static content directory')
@click.option('--domain', help='your-custom-domain.com')
@click.pass_context
def deploy(ctx, path, domain):
    # Get authentication details
    if not netrc or urlparse(API_URL).hostname not in netrc.hosts:
        ctx.invoke(login)

    config = configparser.ConfigParser()
    config.read('.siteship')

    # Read configuration from disk
    for site in config.sections()[:1]:
        conf = dict(config.items(site))

        if path:
            conf.update({'path': path})
        if domain:
            conf.update({'domain': domain})

        # Write configuration to disk
        with open('.siteship', 'w') as configfile:
            config[site] = conf
            config.write(configfile)

        with tempfile.TemporaryDirectory() as directory:
            archive = shutil.make_archive(os.path.join(directory, 'archive'), 'zip', conf['path'])

            r = requests.post(
                url='{}deploys/'.format(API_URL),
                data={
                    'site': '{}sites/{}/'.format(API_URL, site)
                },
                files={
                    'upload': open(archive, 'rb')
                }
            )
            if r.status_code == requests.codes.created:
                click.echo(click.style('Site deployed successfully!', fg='green'))
            elif str(r.status_code).startswith('4'):
                render_validation_errors(response=r)
            else:
                r.raise_for_status()


@siteship.command()
def whoami():
    if netrc:
        pass
    else:
        pass


@siteship.command()
def list():
    if netrc and urlparse(API_URL).hostname in netrc.hosts:
        r = requests.get('{}sites/'.format(API_URL))
        if r.status_code == requests.codes.ok:
            for site in r.json():
                click.echo('[{}] {} {}'.format(
                    site['id'],
                    click.style('*', fg='green'),
                    site['domain']
                ))
        elif str(r.status_code).startswith('4'):
            render_validation_errors(response=r)
        else:
            r.raise_for_status()
    else:
        click.echo(click.style('Please log in to list sites.', fg='red'))

@siteship.command()
@click.option('--email', prompt=True, help='Your login email')
@click.option('--password', prompt=True, hide_input=True, help='Your login password')
def register(email, password):
    r = requests.post('{}signup/'.format(API_URL), json={
        'email': email,
        'password': password
    })
    if r.status_code == requests.codes.created:
        netrc[urlparse(API_URL).hostname] = {
            'login': r.json()['email'],
            'password': r.json()['token']
        }
        netrc.save()
        click.echo(click.style('Signup completed you can now start shipping your sites!', fg='green'))
    elif str(r.status_code).startswith('4'):
        render_validation_errors(response=r)
    else:
        r.raise_for_status()


@siteship.command()
@click.option('--email', prompt=True, help='Your login email')
@click.option('--password', prompt=True, hide_input=True, help='Your login password')
def login(email, password):
    r = requests.post('{}auth/'.format(API_URL), json={
        'username': email,
        'password': password
    })
    r.raise_for_status()

    netrc[urlparse(API_URL).hostname] = {
        'login': email,
        'password': r.json()['token']
    }
    netrc.save()


@siteship.command()
def logout():
    if netrc and urlparse(API_URL).hostname in netrc.hosts:
        click.confirm('This will remove your login credentials!', abort=True)
        del netrc[urlparse(API_URL).hostname]
        netrc.save()
    else:
        click.echo(click.style('Not logged in.', fg='red'))


if __name__ == "__main__":
    siteship()
