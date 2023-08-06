from setuptools import setup
setup(
	name='defid_notifier',
	version='1.2.5',
	description='Mass notifier for Defacer.ID',
	url='http://github.com/p4kl0nc4t/defid_notifier',
	author="P4kL0nc4t",
	author_email="faizzjazadi@gmail.com",
	license="MIT",
	packages=['defid_notifier'],
	zip_safe=False,
	install_requires=['cfscrape', 'argparse'],
	entry_points = {
		'console_scripts': ['defid_notifier=defid_notifier:main'],
	}
     )
