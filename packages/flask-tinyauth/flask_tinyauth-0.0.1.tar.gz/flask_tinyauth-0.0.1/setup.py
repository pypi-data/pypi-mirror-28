from setuptools import find_packages, setup

version = '0.0.1'

setup(
    name='flask_tinyauth',
    version=version,
    license='Apache Software License',
    classifiers=[
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'flask_restful',
    ],
    extras_require = {
        'test': [
            'flake8',
            'flake8-isort',
            'pytest',
            'pytest-cov',
            'codecov',
        ],
    }
)
