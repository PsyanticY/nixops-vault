import sys
import subprocess

from distutils.core import setup, Command

setup(name='nixops-vault',
      version='@version@',
      description='NixOps resources for HashiCorp Vault',
      url='https://github.com/PsyanticY/nixops-vault',
      maintainer='PsyanticY',
      maintainer_email='iuns@outlook.fr',
      packages=['nixopsvault', 'nixopsvault.resources'],
      entry_points={'nixops': ['vault = nixopsvault.plugin']},
      py_modules=['plugin']
)

