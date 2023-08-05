from setuptools import setup

setup(
      name='kenessa',
      version='0.2.2',
      description='Rwanda Administrative Location',
      classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Development Status :: 4 - Beta",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      keywords= 'rwanda administrative location',
      url='https://github.com/rmuhire/kenessa',
      author='Remy Muhire',
      author_email='rmuhire@exuus.com',
      license='MIT',
      packages=['kenessa'],
      entry_points={
          'console_scripts': ['kenessa-province=kenessa.command_line:main'],
      },
      package_data = {'kenessa': ['kenessa.db']},
      zip_safe=False
)




