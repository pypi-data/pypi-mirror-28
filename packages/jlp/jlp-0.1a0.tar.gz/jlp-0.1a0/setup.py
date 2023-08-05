from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='jlp',
    version='0.1-alpha',
    description='tool for installing Julia packages',
    long_description=readme,
    author='FUKUDA Yutaro',
    author_email='sktnkysh+dev@gmai.com',
    packages=find_packages(),
    install_requires=['pyyaml'],
    url='https://github.com/sktnkysh/jlp_Julia-Package-Manager',
    license='MIT',
    entry_points={'console_scripts': ["jlp=jlp.jlp:main"]},)
