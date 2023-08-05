#!/usr/bin/env python
import os, atexit
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call

__version__ = '0.9.0'

git_recipes = [
    'https://gitlab.com/kooki/recipe/md.git',
    'https://gitlab.com/kooki/recipe/tex.git',
    'https://gitlab.com/kooki/recipe/web.git']

git_jars = [
    'https://gitlab.com/kooki/jar/default.git']

resource_dir_env = 'KOOKI_DIR'
resource_dir_default = '~/.kooki'


def get_kooki_dir():
    resource_dir = os.environ.get(resource_dir_env)
    if not resource_dir:
        resource_dir = os.path.expanduser(resource_dir_default)
    return resource_dir


def get_kooki_dir_jars():
    resources_dir = get_kooki_dir()
    jars_dir = os.path.join(resources_dir, 'jars')
    return jars_dir


def get_kooki_dir_recipes():
    resources_dir = get_kooki_dir()
    recipes_dir = os.path.join(resources_dir, 'recipes')
    return recipes_dir


def clone_repositories(path, repositories):
    tmp = os.getcwd()
    os.makedirs(path)
    os.chdir(path)
    for repository in repositories:
        command = 'git clone {}'.format(repository)
        check_call(command.split())
    os.chdir(tmp)


def post_install():
    kooki_dir_recipes = get_kooki_dir_recipes()
    clone_repositories(kooki_dir_recipes, git_recipes)
    kooki_dir_jars = get_kooki_dir_jars()
    clone_repositories(kooki_dir_jars, git_jars)


class NewInstall(install):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        atexit.register(post_install)


setup(
    name='kooki',
    version=__version__,
    description='The ultimate document generator.',
    author='Noel Martignoni',
    include_package_data=True,
    package_data={'kooki.config': ['format.yaml']},
    author_email='noel@martignoni.fr',
    url='https://gitlab.com/kooki/kooki',
    scripts=['scripts/kooki', 'scripts/kooki-recipe', 'scripts/kooki-jar'],
    install_requires=['empy', 'pyyaml', 'toml', 'requests', 'termcolor', 'mistune', 'karamel', 'munch'],
    packages=find_packages(exclude=['tests*']),
    test_suite='tests',
    cmdclass={
        'install': NewInstall,
    },
)
