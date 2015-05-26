from setuptools import setup, find_packages

setup(
    name="libraw.py",
    version="1.0",
    description="python bindings using ctypes for libraw",
    url="https://github.com/paroj/libraw.py",
    author="Pavel Rojtberg",
    license="LGPLv2",
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    py_modules=["libraw"]
)
