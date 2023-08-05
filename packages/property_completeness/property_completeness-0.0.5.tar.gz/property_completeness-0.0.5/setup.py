from setuptools import setup

long_description = '''required input format: a list of dictionaries 
				   '''
setup(name='property_completeness',
      version='0.0.5',
      description='compute property completeness',
      long_description=long_description,
      classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 2.7',
      ],
      license = 'BSD',
	keywords='',
      packages = ['property_completeness'],
      author='Rex Sang',
      author_email='rex@enodoinc.com')