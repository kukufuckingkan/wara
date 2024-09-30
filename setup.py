
from setuptools import setup

setup(
    name="wara",
    version="0.0.1",
    description='Wara api',
    author='Ali Keita',
    author_email='keita.kukukhan@gmail.com',
    #packages=['kukukan','conda','memory','aminatu','ali','ana'],
    install_requires=[
        'flask~=3.0.3',
        'gunicorn',
        'PyYAML',
        'moril==2.0.7',
        'sparkql==0.10.0',
        'pyspark==3.5.3',
        'flask_cors',
        'APScheduler',
        'moril==2.0.9'

    ],
    python_requires='>=3.9.6'
)
