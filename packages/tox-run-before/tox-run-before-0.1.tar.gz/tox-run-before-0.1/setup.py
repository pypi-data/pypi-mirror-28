from setuptools import setup, find_packages


def get_long_description():
    description = ""
    for name in ("README.rst", "AUTHORS.rst", "CHANGELOG.rst"):
        try:
            fp = open(name, "r")
            description += fp.read()
        except IOError:
            pass
        finally:
            fp.close()
    return description


setup(
    name="tox-run-before",
    version="0.1",
    description="Tox plugin to run shell commands before the test environments are created.",
    long_description = get_long_description(),
    author="Praekelt Consulting",
    author_email="dev@praekelt.com",
    license="BSD",
    url="",
    packages=find_packages(),
    install_requires=[
        "tox"
    ],
    include_package_data=True,
    py_modules=["tox_run_before"],
    entry_points={"tox": ["run_before = tox_run_before"]},
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
