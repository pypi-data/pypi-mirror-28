"""Setup, install, test.
"""
from os import path
from setuptools import setup

try:
    import m2r
    readme_name = path.join(path.abspath(path.dirname(__file__)), 'README.md')

    with open(readme_name) as f:
        LONG_DESCRIPTION = m2r.parse_from_file(f)

except Exception:
    LONG_DESCRIPTION = ''


setup(name='pebble-notification_client',
      version='2.0.0',
      description='SQS client for Pebble\'s notification-centre',
      url='https://github.com/mypebble/notification-client',
      author='Pebble',
      author_email='tom.picton@talktopebble.co.uk',
      license='MIT',
      long_description=LONG_DESCRIPTION,
      packages=['notification_client'],
      install_requires=[
          'queue-fetcher', 'boto3', 'Django', 'djangorestframework', 'six'
      ],
      zip_safe=False)
