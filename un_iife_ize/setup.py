from distutils.core import setup
setup(
    name = "un_iife_ize",
    version = "1.0.0",
    description = "Javascript potential IIFE remover",
    author = "Yusaira Khan",
    author_email = "yusaira.khan@mail.mcgill.ca",
    url = "https://github.com/AmiApp/un-iife-ize",
    download_url = "https://raw.githubusercontent.com/AmiApp/un-iife-ize/master/un_iife_ize/un_iife_ize.py",
    keywords = ["javascript", "iife", "remove"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        ],
    long_description = """\
Javascript Potential IIFE removal
-------------------------------------

Variable declarations done properly in javascript files look like IIFEs to MeteorJS.
This removes that


Requires Python 3 or later
"""
)