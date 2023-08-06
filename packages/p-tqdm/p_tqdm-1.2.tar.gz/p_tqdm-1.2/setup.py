from setuptools import setup

setup(
    name = 'p_tqdm',
    packages = ['p_tqdm'],
    version = '1.2',
    description = 'Parallel processing with progress bars',
    author = 'Kyle Swanson',
    author_email = 'swansonk.14@gmail.com',
    url = 'https://github.com/swansonk14/p_tqdm',
    license = 'MIT',
    install_requires = ['tqdm', 'pathos'],
    test_suite='nose.collector',
    tests_require=['nose'],
    keywords = ['tqdm', 'progress bar', 'parallel'],
    classifiers = [],
)
