from setuptools import setup
exec( open('aws4o/version.py').read() )
setup(name='aws4o',
      version=__version__,
      description='AWS Console Access via Stanford Single-Sign On',
      url='https://code.stanford.edu/gsb-circle-research/aws4o',
      author='W. Ross Morrow, Luba Gloukhova',
      author_email='gsb_circle_research@stanford.edu',
      license='MIT',
      packages=[ 'aws4o' ],
      install_requires=[ 'boto3', 'requests' ],
      scripts=[ 'bin/aws4o' ],
      zip_safe=False
    )