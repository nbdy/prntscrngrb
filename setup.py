from setuptools.command.sdist import sdist
from setuptools import setup, find_packages


class InstallSetupScript(sdist):
    def run(self):
        try:
            self.spawn(['pip3', 'install', 'bs4', 'requests', 'tqdm', 'lxml', 'random_user_agent',
                        'keras', 'git+https://github.com/GantMan/nsfw_model', 'podb', 'keras-ocr',
                        'git+https://github.com/torpyorg/torpy', 'pyrunnable', 'loguru', 'Pillow'])
        except Exception as e:
            print(e)
        super().run()


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
    cmdclass={
        'sdist': InstallSetupScript
    },
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
