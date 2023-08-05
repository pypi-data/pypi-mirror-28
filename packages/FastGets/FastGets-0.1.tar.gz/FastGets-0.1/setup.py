from setuptools import setup


setup(
    name='FastGets',
    version='0.1',
    url='https://github.com/ShuJuHeiKe/FastGets',
    description='Python Crawling Framework for Humans',
    author='ShuJuHeiKe',
    maintainer='XuYong',
    maintainer_email='tonyxuourlove@gmail.com',
    license='BSD',
    python_requires='>=3.0',
    install_requires=[
        'werkzeug==0.13',
        'mongoengine==0.15.0',
        'requests==2.18.4',
        'lxml==4.1.1',
        'redis-2.10.6',
        'mockredispy==2.9.3',
        'Flask==0.12.2',
        'python-crontab==2.2.8',
        'psutil==5.4.2',
        'xlrd==1.1.0',
        'croniter==0.3.20',
    ],
)
