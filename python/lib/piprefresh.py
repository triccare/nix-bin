# piprefresh: update all pip installs

import pip
from subprocess import call
for dist in pip.get_installed_distributions():
    if 'site-packages' in dist.location:
        try:
            call(['pip', 'install', '-U', dist.key])
        except Exception as exc:
            print(exc)
