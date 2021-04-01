from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="idchecker",
    version="1.1.2",
    author="Mikalai Lisitsa",
    author_email="mikalai.lisitsa@gmail.com",
    url="https://github.com/soulless-viewer/idchecker",
    description="IDChecker is a tool to get a list of ID records from 1Password, sorted by expiration date.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='1password op cli',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "docopt == 0.6.2"
    ],
    include_package_data=True,
    python_requires='>=3.6',
    scripts=['bin/idchecker'],
)
