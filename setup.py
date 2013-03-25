from setuptools import setup, find_packages

setup(
	name='Benjen', 
	version='1.1.1', 
	packages=find_packages(), 
	scripts=['benjen.py'], 
	install_requires=['Markdown>=2.3', 'Pygments>=1.6', 'PyYAML>=3.10', 'Mako>=0.7.3', 'PyRSS2Gen>=1.0.0'], 

	author='Cody Brocious', 
	author_email='cody.brocious@gmail.com', 
	description='Static blog engine', 
	license='Public Domain/WTFPL', 
	keywords='blog static', 
	url='https://github.com/daeken/benjen', 

	entry_points=dict(
		console_scripts=[
			'benjen = benjen:main'
		]
	)
)
