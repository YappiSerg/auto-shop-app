import os

from setuptools import Command, setup


class BuildSphinx(Command):
    description = 'build Sphinx documentation'
    user_options = [
        ('builder=', 'b', 'Sphinx builder to use'),
        ('source-dir=', 's', 'documentation source directory'),
        ('build-dir=', 'd', 'documentation build directory'),
    ]

    def initialize_options(self):
        self.builder = 'html'
        self.source_dir = 'docs'
        self.build_dir = os.path.join('docs', '_build')

    def finalize_options(self):
        self.source_dir = os.path.abspath(self.source_dir)
        self.build_dir = os.path.abspath(self.build_dir)

    def run(self):
        try:
            from sphinx.cmd.build import build_main
        except ImportError as exc:
            raise RuntimeError(
                'Sphinx is required to build documentation. '
                'Install dependencies with: py -m pip install -r requirements.txt'
            ) from exc

        output_dir = os.path.join(self.build_dir, self.builder)
        result = build_main([
            '-b',
            self.builder,
            self.source_dir,
            output_dir,
        ])
        if result != 0:
            raise SystemExit(result)


setup(
    cmdclass={'build_sphinx': BuildSphinx},
)
