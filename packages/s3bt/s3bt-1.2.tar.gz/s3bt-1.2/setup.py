from setuptools import setup
exec( open('s3bt/version.py').read() )
setup(name='s3bt',
      version=__version__,
      description='S3-mediated bulk data transfers',
      url='https://code.stanford.edu/gsb-circle-research/s3bt',
      author='W. Ross Morrow',
      author_email='gsb_circle_research@stanford.edu',
      license='MIT',
      packages=[ 's3bt' ],
      install_requires=[
			'boto3',
			'requests',
			'Crypto'
      ],
      scripts=[
      		'bin/s3bt'
      ],
      zip_safe=False
    )