from setuptools import setup, find_packages

setup(
    name='pyuiautomator',
    version='1.3',
    description="uiautomator",
    keywords='uiautomator',
    author='hpw123',
    author_email='hpw15101048214@gmail.com',
    url='https://github.com/SuperMan42',
    packages=['pyuiautomator'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'websocket-client>=0.46.0',
    ]
)
