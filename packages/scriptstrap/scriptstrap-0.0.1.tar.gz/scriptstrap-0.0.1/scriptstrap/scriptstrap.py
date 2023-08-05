"""Automatic creation of venv and installation of packages.

This script will automatically create a new venv, install packages using pip in
that venv and import specified modules. If a venv already exists, that venv
will be re-used upon next launch. The same goes for installed packages.

It is possible to specify which version of python the script is supposed to be
run with by calling for instance python2(...) or python3(...). It is
recommended to set the expected version of python using shebang and call
running(...) like this:


    #!/usr/bin/env python3

    import scriptstrap

    scriptstrap.running('requests')

    print(requests.get('http://google.com'))


A venv for python3 will be created and the script till be boostrapped using
that version as well.
"""
import re
import os
import sys
import inspect
import logging
import importlib
import subprocess

_LOGGER = logging.getLogger(__name__)


__all__ = ['running', 'python2', 'python3', 'custom']


def running(*modules, **kwargs):
    """Bootstrap using same python version as currently running."""
    version = os.path.basename(sys.executable).replace('python', '')
    _boostrap(version, *modules, **kwargs)


def python2(*modules, **kwargs):
    """Bootstrap using python2."""
    _boostrap('2', *modules, **kwargs)


def python3(*modules, **kwargs):
    """Bootstrap using python3."""
    _boostrap('3', *modules, **kwargs)


def custom(version, *modules, **kwargs):
    """Bootstrap using a custom version of python."""
    _boostrap(version, *modules, **kwargs)


def _boostrap(version, *modules, **kwargs):
    python = _lookup_python_version(version)
    frame = inspect.stack()[2]
    mod = inspect.getmodule(frame[0])

    venv_path = _venv_path(version)

    if _running_in_venv():
        _LOGGER.debug('Running in venv, will import modules now')

        for module_name in modules:
            _import_module(mod.__name__, module_name, module_name, venv_path)

        for module_name, package_name in kwargs.items():
            _import_module(mod.__name__, module_name, package_name, venv_path)

    else:
        activate_path = os.path.join(venv_path, 'bin', 'activate')
        if not os.path.exists(activate_path):
            _LOGGER.debug('No venv exists, creating a new one in %s',
                          venv_path)
            _create_venv(venv_path, python)

            # We need to install scriptstrap in the new venv, otherwise
            # re-launch will fail
            _run_in_venv(venv_path, 'pip', 'install', 'scriptstrap')

        os.unsetenv('VIRTUAL_ENV')
        python_path = os.path.join(venv_path, 'bin', python)
        os.execl(python_path, python_path, *sys.argv)


def _lookup_python_version(version):
    if version and version not in _available_python_versions():
        _LOGGER.error('Python %s is not available on this system!', version)
        sys.exit(1)

    return 'python' + version


def _running_in_venv():
    """Return wheter script is run inside correct venv."""
    if not hasattr(sys, 'real_prefix'):
        return False

    return os.environ.get('VIRTUAL_ENV', None) is None


def _available_python_versions():
    versions = set()  # This will be for instance {'2.7', '3.5'}

    for dirname in os.environ['PATH'].split(':'):
        try:
            for binary in os.listdir(dirname):
                full_path = os.path.join(dirname, binary)
                match = re.match(r'.*/python([0-9.]+)$', full_path)
                if os.path.isfile(full_path) and match:
                    versions.update([match.group(1)])

        except:  # pylint: disable=bare-except
            pass  # Silently ignore dirs we cannot read

    return versions


def _venv_path(py_version):
    script_path = os.path.abspath(sys.argv[0])
    return '{base_path}.venv{py_version}'.format(
        base_path=os.path.splitext(script_path)[0],
        py_version=py_version)


def _shell(*cmd):
    _LOGGER.debug('Running command: %s', ' '.join(cmd))

    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except FileNotFoundError:
        _LOGGER.error(
            'Could not find command %s, maybe you need to install it?', cmd[0])
        sys.exit(1)
    except subprocess.CalledProcessError:
        _LOGGER.exception('Failed to run: %s', ' '.join(cmd))
        sys.exit(1)


def _create_venv(destination, python):
    _shell('virtualenv', '-p', python, destination)


def _run_in_venv(venv_path, binary, *args):
    _shell(os.path.join(venv_path, 'bin', binary), *args)


def _import_module(target_module, module_name, package_name, venv_path):
    # Try to import module to see if it needs to be installed or not
    try:
        importlib.import_module(module_name)
    except ImportError:
        _run_in_venv(venv_path, 'pip', 'install', package_name)

    _LOGGER.debug('Importing module %s into %s', module_name, target_module)
    setattr(sys.modules[target_module],
            module_name,
            importlib.import_module(module_name))
