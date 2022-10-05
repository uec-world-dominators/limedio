import setuptools
import os

root_dir = os.path.abspath(os.path.dirname(__file__))


def _requirements():
    return [name.rstrip() for name in open(os.path.join(root_dir, 'requirements.txt')).readlines()]


setuptools.setup(
    name='limedio',
    packages=setuptools.find_packages(),
    version='0.0.3',
    install_requires=_requirements(),
    author='shosatojp',
    author_email='me@shosato.jp',
    url='https://github.com/uec-world-dominators/limedio',
    description='UEC Auth',
    long_description='',
    keywords='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
