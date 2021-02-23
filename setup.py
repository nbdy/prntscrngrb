from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="prntscrngrb",
    version="0.1",
    description="",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/prntscrngrb",
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License'
    ],
    keywords="",
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    entry_points={
        'console_scripts': [
            'prntscrngrb = prntscrngrb.__main__:main'
        ]
    },
    package_data={
        "prntscrngrb": ["nsfw_nn/*"]
    },
    long_description_content_type="text/markdown",
)
