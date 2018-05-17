from distutils.core import setup

setup(name='logan',
      version='0.0.1',
      author='Maciej "Ishari" Biazik',
      author_email='mastoffp@gmail.com',
      packages=['logan'],
      entry_point={
          'console_scripts': [
              'logan-search = logan.__init__:main'
          ]
      }
      )
