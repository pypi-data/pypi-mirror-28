from setuptools import setup, find_packages


setup(
    name='FastGets',
    version='0.1.5',
    url='https://github.com/ShuJuHeiKe/FastGets',
    description='Python Crawling Framework for Humans',
    author='ShuJuHeiKe',
    maintainer='XuYong',
    maintainer_email='tonyxuourlove@gmail.com',
    packages=find_packages(),
    license='BSD',
    entry_points="""
    [console_scripts]
    fastgets_worker=fastgets.work:main
    fastgets_api_server=fastgets.api.app:run
    """
)
