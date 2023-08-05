from setuptools import setup, find_packages


setup(
    name='FastGets',
    version='0.1.4',
    url='https://github.com/ShuJuHeiKe/FastGets',
    description='Python Crawling Framework for Humans',
    author='ShuJuHeiKe',
    maintainer='XuYong',
    maintainer_email='tonyxuourlove@gmail.com',
    packages=find_packages(exclude=['examples', 'tests']),
    license='BSD',
    python_requires='>=3.0',
    entry_points="""
    [console_scripts]
    fastgets_worker=fastgets.worker:main
    fastgets_api_server=fastgets.api.app:run
    """
)
