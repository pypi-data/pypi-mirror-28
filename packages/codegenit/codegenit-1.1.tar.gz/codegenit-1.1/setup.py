from setuptools import setup

setup(name='codegenit',
      version='1.1',
      description='Generate a python project from a swagger file.',
      url='http://github.com/cidrblock/codegenit',
      author='Bradley A. Thornton',
      author_email='brad@thethorntons.net',
      license='MIT',
      packages=[
        'codegenit'
      ],
      install_requires=[
        'pygments',
        'astor'
      ],
      entry_points={
        'console_scripts': [
            'codegenit = codegenit.codegenit:main',
        ],
      },
      zip_safe=False)
