from setuptools import setup

setup(name='memect-http-error',
      version='0.0.7',
      description="error code package for memect.co",
      long_description="",
      classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'],
      keywords='http error code',
      author='@nanhuijuan',
      author_email='nanhuijuan@memect.co',
      url='https://pypi.python.org/pypi/memect-http-error',
      license='MIT',
      packages=['memect_http_error'],
      include_package_data=True,
      zip_safe=True,
      entry_points="")
