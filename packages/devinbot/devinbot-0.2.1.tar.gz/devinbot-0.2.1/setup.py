from setuptools import setup

setup(
    name='devinbot',
    version='0.2.1',
    url='https://github.com/peterskipper/devin',
    license='MIT',
    author='Peter Skipper',
    author_email='peter.skipper@gmail.com',
    description='Command line tool to recommend albums',
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'devin = devin.cli:devin_main'
        ]
    }
)
