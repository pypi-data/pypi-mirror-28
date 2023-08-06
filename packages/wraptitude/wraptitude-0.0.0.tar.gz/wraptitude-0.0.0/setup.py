from distutils.core import setup

with open('README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name='wraptitude',
    version='0.0.0',
    description='Wrap the results of your Python functions',
    long_description=long_description,
    author='Brett Beatty',
    author_email='brettbeatty@gmail.com',
    url='https://github.com/brettbeatty/wraptitude',
    packages=['wraptitude'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    keywords=['wrapper', 'decorator']
)
