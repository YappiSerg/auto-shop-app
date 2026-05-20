from setuptools import setup
from sphinx.setup_command import BuildDoc


setup(
    cmdclass={'build_sphinx': BuildDoc},
    command_options={
        'build_sphinx': {
            'project': ('setup.py', 'Auto Shop App'),
            'version': ('setup.py', '0.1.0'),
            'release': ('setup.py', '0.1.0'),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', 'docs/_build'),
            'builder': ('setup.py', 'html'),
        }
    },
    setup_requires=['Sphinx>=7.0,<9.0'],
)
