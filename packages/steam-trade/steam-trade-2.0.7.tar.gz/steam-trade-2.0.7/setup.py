from setuptools import setup

setup(
        name="steam-trade",
        version="2.0.7",
        description='An Asynchronous, event based steam trade library',
        packages=["pytrade"],
        url="https://github.com/Zwork101/steam-trade",
        author="Zwork101",
        author_email="zwork101@gmail.com",
        keywords="steam trade",
        install_requires = [
            "aiohttp",
            "rsa",
            "steamid",
            "pyee"
        ],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6"
        ]
)

