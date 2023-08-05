from setuptools import setup, find_packages
from setuptools.command.install import install
import commands

class CustomInstall(install):
  def run(self):
    install.run(self)
    self.execute(post_install,
                 (self.install_lib, self.verbose, self.dry_run),
                 msg="running post_install")


def post_install(install_dir, verbose, dry_run):
  # run the shell file
  install_shell_file = './network_opt/shell_after_installed.sh'
  (status, output) = commands.getstatusoutput('/bin/sh %s' % install_shell_file)
  print status, output
  print('-------network_opt installing process completed-------')

setup(
  name='network_opt',
  version='1.0',
 # packages=['network_opt'],
  packages=find_packages(),
  install_requires=['scapy','watchdog','ntplib',],
  data_files=[('/etc/init.d',['./network_opt/do_network_opt'])],
  package_data={
    '':['do_network_opt','shell_after_installed.sh'],
  },
  include_package_data=True,
  scripts=['./bin/network_opt'],
  cmdclass={
    'install': CustomInstall,
  }
)