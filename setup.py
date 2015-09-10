from setuptools import setup, find_packages

setup(
    name = 'coinkite-api',
    version = '1.0.1',
    description = 'Coinkite API (Python binding)',
    long_description = "Provides this fully-featured reference API wrapper for Coinkite's powerful Bitcoin (and Litecoin/Blackcoin) services. Works with Google App Engine and normal Python server-side applications. Also includes a simple CLI program to ease experimental use of cURL with the Coinkite API.",
    author = 'Coinkite Inc.',
    author_email = 'support@coinkite.com',
    license = 'BSD',
    url = 'https://github.com/coinkite/coinkite-python',
    keywords = ['coinkite', 'bitcoin', 'api'],
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['simplejson>=3.2.0', 'python-dateutil>=1.5'],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: BSD License',
    ],
)
