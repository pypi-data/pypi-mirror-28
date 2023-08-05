from distutils.core import setup

setup(
    name = 'pyPipelineStream',
    packages = ['pyPipelineStream'],
    version = '0.2.0',
    description = 'A pipelining framework designed for data analysis but can be useful to other applications',
    author = 'daniyall',
    author_email = 'daniyal.l@outlook.com',
    url = 'https://github.com/daniyall/pyPipelining',
    download_url = 'https://github.com/daniyall/pyPipelining/archive/0.2.0.tar.gz', # I'll explain this in a second
    keywords = ['data-science', 'pipelining', 'stream-processing', "data-analysis"], # arbitrary keywords
    classifiers = [],
    python_requires=">=3",
    license="LICENSE.txt",
    long_description=open('README.md', 'rt').read()
)