import os
from setuptools import setup, find_packages

__version__ = '0.1.4'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASEDIR, 'README.rst')).read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='ambisafe_tenant',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    url='https://github.com/Ambisafe/ambisafe_tenant_client',
    download_url='https://github.com/Ambisafe/ambisafe_tenant_client/get/v{0}.zip'
        .format(__version__),
    author='Kirill Pisarev',
    author_email='kirill@ambisafe.co',
    keywords=['ambisafe', 'ethereum', 'etoken'],
    description='Ambisafe-tenant server client library',
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
    ],
    test_suite='test.test',
    setup_requires=install_requires
)
