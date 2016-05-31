##
# Copyright 2012-2016 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBlock for installing Java, implemented as an easyblock

@author: Jens Timmerman (Ghent University)
"""

import os
import shutil

from distutils.version import LooseVersion
from easybuild.easyblocks.generic.packedbinary import PackedBinary
from easybuild.tools.run import run_cmd


class EB_Java(PackedBinary):
    """Support for installing Java as a packed binary file (.tar.gz)
    Use the PackedBinary easyblock and set some extra paths.
    """
    
    def extract_step(self):
        """Unpack the source"""
        if LooseVersion(self.version) < LooseVersion('1.7'):
            try: 
                os.chmod(self.src[0]['path'], 0755)
            except OSError, err:
                raise EasyBuildError("Failed adding execution permission to java installer: %s", err)
            try:
                os.chdir(self.builddir)
            except OSError, err:
                raise EasyBuildError("Failed to move to build dir: %s", err)
            run_cmd(self.src[0]['path'], log_all=True, simple=True, inp='')
        else:
            PackedBinary.extract_step(self)
    
    def install_step(self):
        if LooseVersion(self.version) < LooseVersion('1.7'):
            try:
                os.rmdir(self.installdir)
                shutil.copytree(os.path.join(self.builddir, 'jdk%s' % self.version), self.installdir)
            except OSError, err:
                raise EasyBuildError("Failed to install by copying: %s", err)
        else:
            PackedBinary.install_step(self)

    def make_module_extra(self):
        """
        Set JAVA_HOME to install dir
        """
        txt = PackedBinary.make_module_extra(self)
        txt += self.module_generator.set_environment('JAVA_HOME', self.installdir)
        return txt
