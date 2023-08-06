from setuptools import setup

setup(name='notify-run',
      version='0.0.2',
      description='Client for notify.run notifications.',
      author='Paul Butler',
      author_email='notify@paulbutler.org',
      url='https://notify.run/',
      packages=['notify_run'],
      entry_points={
          'console_scripts': [
              'notify-run = notify_run.cli:main'
          ]
      },
      install_requires=[
          'PyQRCode==1.2.1',
          'requests==2.18.4',
      ],
      )
