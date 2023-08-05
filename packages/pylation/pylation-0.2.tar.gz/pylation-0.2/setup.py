from distutils.core import setup

setup(name='pylation',
      version='0.2',
      description='Test upload of relational network',
      url='http://github.com/bheff88/pylation',
      author='Braden Heffernan',
      author_email='baheffer@ucalgary.ca',
      license='MIT',
      packages=['pylation'],
      install_requires=['numpy>=1.9.1',
                        'scipy>=0.14',
                        'six>=1.9.0',
			'keras',
			'pyyaml'],
      zip_safe=False)
