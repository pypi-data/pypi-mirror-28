from setuptools import setup

setup(
    name='lektor-gulp-support',
    version='0.1.2',
    author=u'Drayuk',
    author_email='ekentiako@gmail.com',
    url='http://github.com/selgem/lektor-gulp-support',
    description='Adds support for gulp to Lektor',
    license='MIT',
    py_modules=['lektor_gulp_support'],
    entry_points={
        'lektor.plugins': [
            'gulp-support = lektor_gulp_support:GulpSupportPlugin',
        ]
    }
)
