from setuptools import setup, find_packages

setup(
    name="generic_job_queue",
    version="0.0.7",
    author="David Ng",
    author_email="david.ng.dev@gmail.com",
    description=("The generic job queue"),
    url="https://github.com/davidNHK/generic-job-queue",
    download_url="https://github.com/davidNHK/generic-job-queue/archive/0.0.7.zip",
    license="BSD",
    packages=find_packages("./", exclude=["tests"]),
    keywords=['sqlalchemy', 'job queue', 'worker'],
    classifiers=[],
    install_requires=[
        'pylint',
        'pytest',
        'pytest-cov',
        'twine',
        'sqlalchemy'
    ]
)