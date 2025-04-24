from setuptools import setup, find_packages

setup(
    name='cli-linter',
    version='0.1',
    description='Навчальний CLI-інструмент для лабораторної роботи',
    author='Maksym Ivashchuk',
    url='https://github.com/nvmlnd/cli-lab',
    packages=find_packages(),
    install_requires=[
        'click>=7.0',
        'pandas>=2.0'
    ],
    entry_points='''
        [console_scripts]
        cli-linter=csv_linter.main:cli
    ''',
)
