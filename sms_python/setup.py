from setuptools import setup, find_packages


PACKAGE = 'tencent_cloud_sample'
NAME = 'tencent_cloud_sample'
DESCRIPTION = 'Tencent Cloud SDK Code Sample Library for Python'
AUTHOR = 'Tencent'
AUTHOR_EMAIL = 'tencentcloudapi@tencent.com'
URL = 'https://gitee.com/tencent-cloud-cloudshell/python-sdk'
VERSION = __import__(PACKAGE).__version__
REQUIRES = [
    'tencentcloud-sdk-python'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='Apache License 2.0',
    url=URL,
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    platforms='any',
    install_requires=REQUIRES,
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development'
    )
)
