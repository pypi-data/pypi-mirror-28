from setuptools import setup


setup(
    name="pykintone",
    packages=[
        "pykintone",
        "pykintone.application_settings",
        "pykintone.user_api"
    ],
    install_requires=[
        "PyYAML",
        "requests",
        "pytz",
        "tzlocal"
    ],
    version="0.3.10",
    description="Python library to access kintone",
    author="icoxfog417",
    author_email="icoxfog417@yahoo.co.jp",
    url="https://github.com/icoxfog417/pykintone",
    keywords=["kintone"],
    classifiers=[],
)
