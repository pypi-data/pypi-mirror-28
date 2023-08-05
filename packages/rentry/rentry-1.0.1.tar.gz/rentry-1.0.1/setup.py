from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='rentry',
    version='1.0.1',
    description='Markdown pastebin from command line',
    license='MIT',
    long_description=read('README'),
    author='radude',
    author_email='admin@rentry.co',
    url='https://github.com/radude/rentry',
    download_url='https://github.com/radude/rentry/archive/1.0.1.tar.gz',
    keywords=['markdown', 'pastebin', 'cli', 'terminal', 'console', 'markup'],
    scripts=['rentry'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
