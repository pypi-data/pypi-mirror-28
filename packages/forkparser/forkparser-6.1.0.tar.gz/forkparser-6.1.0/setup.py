from setuptools import setup

setup(
    name = 'forkparser',
    version = '6.1.0',
    description = 'A hopefully temporary fork of Universal Feed Parser, which handles RSS 0.9x, RSS 1.0, '
                  'RSS 2.0, CDF, Atom 0.3, and Atom 1.0 feeds',
    author = 'Kurt McKee',
    author_email = 'contactme@kurtmckee.org',
    maintainer = 'Tom Most',
    maintainer_email = 'forkparser@freecog.net',
    url = 'https://github.com/twm/feedparser',
    download_url = 'https://pypi.python.org/pypi/forkparser',
    platforms = ['POSIX', 'Windows'],
    packages = ['feedparser', 'feedparser.datetimes', 'feedparser.namespaces', 'feedparser.parsers'],
    install_requires = [
        'sgmllib3k;python_version>="3.0"',
    ],
    keywords = ['atom', 'cdf', 'feed', 'parser', 'rdf', 'rss'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML',
    ],
)
