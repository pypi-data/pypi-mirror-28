from setuptools import setup

def long_desc():
      with open('README.rst') as readme:
            return readme.read()
setup(name='package_boilerplate',
      version='0.9.0',
      description='A bare minimal package folder structure',
      long_description=long_desc(),
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Text Processing :: Linguistic',
      ],
      url='https://github.com/mirazmamun/python_package_boilerplate.git',
      author='Miraz Al-Mamun',
      author_email='mirazmamun@yahoo.com',
      license='MIT',
      packages=['package_boilerplate'],
      zip_safe=False)