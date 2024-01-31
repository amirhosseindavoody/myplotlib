import pathlib
import setuptools

setuptools.setup(
    name="myplotlib",
    version="0.1.0",
    description="Custom plotting routines inspired by JMP statistical analysis software.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/amirhosseindavoody/myplotlib",
    author="Amirhossein Davoody",
    author_email="amirhossein.davoody@gmail.com",
    license="The Unlicense",
    project_urls={
        "Source": "https://github.com/amirhosseindavoody/myplotlib",
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    install_requires=[
        "matplotlib",
        "pandas>=2.0",
        "scipy",
        "numpy",
        "loguru",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
