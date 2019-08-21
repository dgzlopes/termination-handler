from distutils.core import setup

import setuptools

with open('README.md') as f:
    long_description = f.read()

setup(
    name='termination-handler',
    version='0.0.2',
    description='Handle termination notices on spot/preemptible instances.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgzlopes/termination-handler',
    license='MIT',
    install_requires=[
        'requests',
        'cloud-detect',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
    ],
    author='Daniel González Lopes',
    author_email='danielgonzalezlopes@gmail.com',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'termination-handler = termination_handler.termination_handler:main',
        ],
    },
)
