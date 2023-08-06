from setuptools import setup

setup(
    name='evol',
    version='0.2.0',
    description='A Grammar for Evolutionary Algorithms and Heuristics',
    author=['Vincent D. Warmerdam', 'Rogier van der Geer'],
    author_email='vincentwarmerdam@gmail.com',
    url='https://github.com/godatadriven/evol',
    packages=['evol', 'evol.helpers'],
    keywords=['genetic', 'algorithms', 'heuristics'],
    tests_require=[
        "pytest==3.3.1"
    ]
)
