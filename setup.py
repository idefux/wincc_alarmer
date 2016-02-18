from wincc_alarmer.__init__ import __version__
from setuptools import setup, find_packages

install_requires = [
        'click',
        'pywincc',
        'premailer',
        'jinja2'
    ]

setup(
    description='wincc_alarmer: poll wincc alarm archives and trigger emails \
    or syslog messages',
    author='Stefan Fuchs',
    url='https://github.com/Idefux/wincc_poller',
    install_requires=install_requires,
    name='wincc_alarmer',
    version=__version__,
    packages=find_packages(exclude=['docs', 'templates', 'venv', 'tests']),
    entry_points={
                  'console_scripts': [
                                      'wincc_alarmer = wincc_alarmer.cli:poll',
                                      'test_email = wincc_alarmer.cli:test_email',
                                      ],
                  },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
                 ],
)
