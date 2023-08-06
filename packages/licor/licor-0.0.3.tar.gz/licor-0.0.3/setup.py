from setuptools import setup, find_packages

setup(
	name = "licor",
	version = "0.0.3",
	packages = find_packages(),
	package_data = {"licor": ["templates/*", "templates/*/*"]},
	author = "Daniel Knüttel",
	author_email = "daniel.knuettel@daknuett.eu",
	install_requires = ["docopt"],
	description = "A script to add license disclaimers",
	long_description = open("README.rst").read(),

	entry_points = {"console_scripts": ["licor = licor.main:main"]}
     )
