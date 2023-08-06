from setuptools import setup

setup(name='ClosePlots',
      version='1.0',
      description='A button that lets you close subplots.',
      url='https://github.com/ojhall94/ClosePlots',
      download_url = 'https://github.com/ojhall94/ClosePlots/archive/1.0.tar.gz',
      author='Oliver James Hall',
      author_email='ojh251@student.bham.ac.uk',
      license='MIT',
      packages=['ClosePlots'],
      install_requires=[
            'matplotlib',
      ],
      zip_safe=False)
