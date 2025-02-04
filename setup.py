import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='semantic-code-search',
    version='0.1.0',
    author='Applynow',
    author_email='d.miyazaki@applynow.co.jp',
    description='Search your codebase with natural language.',
    install_requires=[
                'numpy',
                'prompt_toolkit',
                'Pygments',
                'sentence_transformers',
                'setuptools',
                'torch',
                'tree_sitter',
                'tree_sitter_builds',
                'tree_sitter_languages',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    url='https://github.com/applynow/semantic-code-search',
    package_dir={
        "semantic_code_search": "src/semantic_code_search"
    },
    entry_points={
        'console_scripts': [
            'sem=semantic_code_search.cli:main',
        ]
    },
    keywords='semantic code search',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)
