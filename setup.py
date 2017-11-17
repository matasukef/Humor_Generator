from setuptools import setup, find_packages

with open('READM.rst') as f:
    readme = f.read()

with open('LICENSE', 'r') as f:
    license = f.read()

setup(
    name='HumorCaptionGenerator',
    version='0.0.1',
    description='Generate humor caption from images',
    long_description=readme,
    author='Kosuke Ftamata',
    author_email='f-e@toki.waseda.jp',
    url='https://matasukef.github.io',
    license=license,
    packages=find_packages(exclude=['test']),
    install_requires=['chainer', 'numpy']
    )
