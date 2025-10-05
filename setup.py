from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='devkit-cli',
    version='0.1.0',
    description='AI-powered terminal assistant for developers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='sravya',
    author_email='m3l0dy.144@gmail.com',
    url='https://github.com/flurry101/devkit',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'colorama>=0.4.0',
    ],
    extras_require={
        'ai': ['google-generativeai>=0.3.0'],
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'build>=0.8.0',
            'twine>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'devkit=devkit.main:cli',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    keywords='cli developer-tools ai terminal productivity git devops snippets time-travel debugging',
    project_urls={
        'Bug Reports': 'https://github.com/flurry101/devkit/issues',
        'Source': 'https://github.com/flurry101/devkit',
        'Documentation': 'https://github.com/flurry101/devkit#readme',
    },
)