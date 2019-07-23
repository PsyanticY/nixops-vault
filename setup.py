import sys
import subprocess

from distutils.core import setup, Command

setup(name='nixops-hashicorpvault',
      version='@version@',
      description='NixOps resources for HashiCorp Vault',
      url='https://github.com/PsyanticY/nixops-hashicorpvault',
      maintainer='PsyanticY',
      maintainer_email='iuns@outlook.fr',
      packages=['nixopshashicorpvault', 'nixopshashicorpvault.resources'],
      entry_points={'nixops': ['hashicorpvault = nixopshashicorpvault.plugin']},
      py_modules=['plugin']
)

