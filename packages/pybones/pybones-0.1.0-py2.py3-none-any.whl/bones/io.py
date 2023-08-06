# -*- coding: utf-8 -*-
import datetime
import os
import logging
import re
import shutil
import sys

import colorama
import git
import jinja2
import requests
import virtualenv

from .errors import InvalidURLError

colorama.init()
logger = logging.getLogger(__name__)
template_extension = '.jinja'  # template files are rendered


def create_structure(package_metadata=None, overwrite=None):
    """"""
    package_metadata = package_metadata or get_package_metadata(accept_defaults=True)
    package_path = package_metadata.get('package_path')
    name = package_metadata.get('project_name') or os.path.basename(package_path)
    package_metadata['project_name'.upper()] = name.upper()
    os.makedirs(package_path, mode=0o755, exist_ok=True)
    env = jinja2.Environment()

    # Build template
    bones_folder = os.path.dirname(os.path.realpath(__file__))
    template_folder_tree = os.path.join(bones_folder, 'templates')
    for root, folders, files in os.walk(template_folder_tree):
        relpath = root.replace(template_folder_tree, '').lstrip('/').replace('project_name', name)
        ignored_files = ['.DS_Store']

        for folder_name in folders:
            folder_path = os.path.sep.join(_ for _ in (package_path, relpath, folder_name) if _)
            folder_path = folder_path.replace('project_name', name)
            os.makedirs(folder_path, mode=0o755, exist_ok=True)

        for filename in files:
            if filename in ignored_files:
                continue
            template_file = True if filename.endswith(template_extension) else False
            real_name = filename.replace(template_extension, '')
            filepath = os.path.join(root, filename)
            realpath = os.path.sep.join(_ for _ in (package_path, relpath, real_name) if _)
            realpath = realpath.replace('project_name', name)

            with open(filepath, 'r', encoding='utf-8') as stream:
                data = stream.read()

            # Render file
            if template_file:
                jinja_template = env.from_string(data)
                data = jinja_template.render(**package_metadata)

            if os.path.exists(realpath) and not overwrite:
                response = input(_c(f'Warning: "{realpath}" already exists. Overwrite? [y/N]: '))
                if response.lower() in ['', 'n']:
                    continue

            # Write file
            with open(realpath, 'w') as stream:
                stream.write(data.rstrip())
                if realpath.endswith('.py'):
                    stream.write('\n')

            # Update permissions
            mode = os.stat(filepath).st_mode & 0o0777
            os.chmod(realpath, mode)

    # Create license file
    project_licence_filepath = os.path.join(package_path, 'LICENSE')
    license = package_metadata['license']
    licenses_folder = os.path.join(bones_folder, 'licenses')
    license_filepath = None
    for license_filename in os.listdir(licenses_folder):
        matching_pattern = license.replace(' ', '_')
        license_filename = license_filename.replace(' ', '_')
        if license_filename.startswith(matching_pattern):
            license_filepath = os.path.join(licenses_folder, license_filename)
            break
    if license_filepath and os.path.exists(license_filepath):
        write_license = True
        with open(license_filepath, 'r') as stream:
            license_data = stream.read()
        if license_filepath.endswith(template_extension):
            jinja_template = env.from_string(license_data)
            license_data = jinja_template.render(**package_metadata)
        if os.path.exists(project_licence_filepath) and not overwrite:
            write_license = False
            response = input(_c(f'Warning: "{project_licence_filepath}" already exists. Overwrite? [y/N]: '))
            if response.lower() in ['', 'n']:
                write_license = True
        if write_license is True:
            with open(project_licence_filepath, 'w') as stream:
                stream.write(license_data)
    return package_metadata


def create_virtualenv(package_metadata=None, replace=None):
    package_metadata = package_metadata or get_package_metadata(accept_defaults=True)
    package_name = package_metadata['package_name']
    venvs = os.getenv('WORKON_HOME') or os.path.join(os.getenv('HOME'), '.virtualenvs')
    venv_home = os.path.join(venvs, package_name)
    if (os.path.exists(venv_home) and replace) or not (os.path.exists(venv_home)):
        shutil.rmtree(venv_home)
        virtualenv.create_environment(home_dir=venv_home)
    return package_metadata


def _check_url(url):
    try:
        if requests.get(url).status_code == requests.codes.ok:
            return True
        else:
            raise InvalidURLError(url=url)
    except Exception:
        raise InvalidURLError(url=url)


def get_package_metadata(package_path=None, project_name=None, accept_defaults=None, check_url=None):
    metadata = {}
    response = ''
    if package_path and project_name:
        project_path = os.path.join(package_path, project_name)
        if os.path.exists(project_path):
            for root, folders, files in os.walk(project_path):
                folders[:] = [_ for _ in folders if not _.startswith('.')]
                files[:] = [_ for _ in files if _ == '__metadata__.py']
                for filename in files:
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r') as stream:
                        exec(stream.read(), globals(), metadata)
                        metadata = metadata.get('package_metadata') or metadata
                        break
                if metadata:
                    project_name = metadata['name']
                    break
    elif package_path and not project_name:
        project_name = os.path.basename(package_path)
        project_path = os.path.join(package_path, project_name)
    elif not package_path and project_name:
        package_path = os.path.realpath(os.getcwd())
        project_path = os.path.join(package_path, project_name)
    elif not package_path and not project_name:
        package_path = os.path.realpath(os.getcwd())
        project_name = os.path.basename(package_path)
        project_path = os.path.join(package_path, project_name)

    if not accept_defaults and os.path.dirname(os.path.realpath(package_path)) == os.getcwd():
        response = input(_c(f'Package path [{package_path}]: '))
        package_path = response or package_path
        if package_path.startswith('~'):
            package_path = os.path.expanduser(package_path)
        else:
            package_path = os.path.abspath(package_path)
        project_name = os.path.basename(response or package_path).replace('-', '_')

    global_config = read_git_config()
    user_info = {k: v for k, v in global_config['user'].items()}

    python_version = '.'.join(sys.version.split(' ')[0].split('.')[:2])
    metadata.setdefault('python_version', python_version)

    if not accept_defaults:
        response = input(_c(f'Project name [{project_name}]: '))
    metadata.setdefault('project_name', response or project_name)
    metadata.setdefault('package_path', project_path)
    metadata['package_name'] = metadata['project_name']
    metadata['project_name'] = metadata['project_name'].replace(' ', '_').replace('-', '_')

    description = metadata.get('description') or 'A bones project'
    if not accept_defaults:
        response = input(_c(f'Project description [{description}]: '))
    metadata.setdefault('description', response or description)

    version = metadata.get('version') or '0.1.0'
    if not accept_defaults:
        response = input(_c(f'Project version [{version}]: '))
    metadata.setdefault('version', response or version)

    license = 'MIT'
    if not accept_defaults:
        response = input(_c(f'Project license [{license}]: '))
    metadata.setdefault('license', response or license)

    url = metadata.get('url') or f'https://www.pypi.org'
    if not accept_defaults:
        while True:
            response = input(_c(f'Project url (must be public and valid for pypi) [{url}]: '))
            if not check_url or check_url and _check_url(response or url):
                break
    elif check_url:
        _check_url(url)
    metadata.setdefault('url', response or url)

    author = metadata.get('author') or user_info['name']
    if not accept_defaults:
        response = input(_c(f'Author name [{author}]: '))
    metadata.setdefault('author', response or author)

    author_email = metadata.get('author_email') or user_info['email'].lower()
    if not accept_defaults:
        response = input(_c(f'Author name [{author_email}]: '))
    metadata.setdefault('author_email', response or author_email)

    maintainer = metadata.get('maintainer') or user_info['name']
    if not accept_defaults:
        response = input(_c(f'Maintainer name [{maintainer}]: '))
    metadata.setdefault('maintainer', response or maintainer)

    maintainer_email = metadata.get('maintainer_email') or user_info['email'].lower()
    if not accept_defaults:
        response = input(_c(f'Maintainer name [{maintainer_email}]: '))
    metadata.setdefault('maintainer_email', response or maintainer_email)

    year = metadata.get('year') or datetime.datetime.utcnow().year
    if not accept_defaults:
        response = input(_c(f'Copyright year(s) [{year}]: '))
    metadata.setdefault('year', response or year)
    return metadata


def read_git_config(config_path=None):
    config_path = config_path or os.path.join(os.getenv('HOME'), '.gitconfig')
    config = {}
    parser = git.GitConfigParser([config_path])
    for section in parser.sections():
        config.setdefault(section, {})
        for key, value in parser.items(section):
            config[section][key] = value
        if not config[section]:
            del config[section]
    return config


def setup_git(package_metadata):
    """"""
    package_path = package_metadata.get('package_path')
    project_name = package_metadata.get('project_name')
    package_path = os.path.realpath(package_path)
    logger.info(f'Building "{project_name}" under "{package_path}"')
    git.Repo.init(package_path)
    return package_metadata


def update_git(package_metadata):
    """"""
    filepaths = set()
    package_path = package_metadata.get('package_path')
    git.Repo.init(package_path)
    repo = git.Repo(package_path)
    if not (repo.is_dirty() or repo.untracked_files):
        return package_metadata
    for root, folders, files in os.walk(package_path):
        folders[:] = [f for f in folders if f not in ['.git']]
        for filename in files:
            filepath = os.path.join(root, filename)
            filepaths.add(filepath)
    # is path dirty?
    filepaths = sorted(filepaths)
    repo.index.add(filepaths)
    repo.index.commit("First commit")
    tag_name = 'bones-auto-generated'
    try:
        tags = repo.tags or []
        for tag in tags:
            if tag_name == tag.name:
                repo.delete_tag(tag)
        repo.create_tag(tag_name, message='Created by bones')
    except TypeError as e:
        pass
    return package_metadata


# ----------------------------------------------------------------------
def _c(string, color=None):
    """Colorizes output"""
    delimiters = {
        ('[', ']'): colorama.Fore.GREEN,
        ('"', '"'): colorama.Fore.YELLOW,
    }
    final = string
    reset = colorama.Style.RESET_ALL
    for start, end in delimiters:
        pattern = f'\\{start}(.*?)\\{end}'
        actual_color = color or delimiters[(start, end)]
        for result in re.findall(pattern, string):
            original = ''.join((start, result, end))
            colored = ''.join((start, actual_color, result, reset, end))
            final = final.replace(original, colored)
    return final

    if all(s in string for s in ['[', ']']):
        afore, middle = string.split('[')
        middle, after = middle.split(']')
        begin = color or colorama.Fore.GREEN
        end = colorama.Style.RESET_ALL
        replacement = f'[{begin}{middle}{end}]'
        original = f'[{middle}]'
        final = string.replace(original, replacement, 1)
    return final
