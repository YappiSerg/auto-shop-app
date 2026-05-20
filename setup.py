from setuptools import setup

try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    BuildDoc = None


cmdclass = {}
command_options = {}

if BuildDoc is not None:
    cmdclass['build_sphinx'] = BuildDoc
    command_options['build_sphinx'] = {
        'project': ('setup.py', 'Auto Shop App'),
        'version': ('setup.py', '0.1.0'),
        'release': ('setup.py', '0.1.0'),
        'source_dir': ('setup.py', 'docs'),
        'build_dir': ('setup.py', 'docs/_build'),
        'builder': ('setup.py', 'html'),
    }


setup(
    cmdclass=cmdclass,
    command_options=command_options,
)
