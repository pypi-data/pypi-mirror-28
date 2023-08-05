from distutils.core import setup
setup(
    name='masonite',
    packages=['masonite',
              'masonite.auth',
              'masonite.cashier',
              'masonite.extensions',
              'masonite.facades',
              'masonite.commands',
             ],  # this must be the same as the name above
    version='0.1.12',
    description='The core for the python framework',
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/python-framework',  # use the URL to the github repo
    # I'll explain this in a second
    download_url='',
    keywords=['python web framework', 'python3'],  # arbitrary keywords
    classifiers=[],
)
