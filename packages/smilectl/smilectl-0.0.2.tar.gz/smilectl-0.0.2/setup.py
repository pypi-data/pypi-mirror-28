"""Setup smilectl package."""
from setuptools import setup

__version__ = "0.0.2"

setup(
    name="smilectl",
    version=__version__,
    description="Smile Lab job launch tool.",
    install_requires=["jsonnet", "simplejson", "smile"],
    zip_safe=False,
    packages=["smilectl"],
    package_data={"smilectl": ["lib/*"]},
    data_files=[],
    url="https://zhengxu.work/",
    entry_points={"console_scripts": ["smilectl = smilectl:app_main"]})
