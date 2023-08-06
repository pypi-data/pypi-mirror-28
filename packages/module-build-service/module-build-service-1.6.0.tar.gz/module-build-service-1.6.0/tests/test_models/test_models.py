# Copyright (c) 2016  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Ralph Bean <rbean@redhat.com>

import os
import unittest

import modulemd

from tests.test_models import init_data
from module_build_service import conf
from module_build_service.models import ComponentBuild, ModuleBuild, make_session


class TestModels(unittest.TestCase):
    def setUp(self):
        init_data()

    def test_app_sqlalchemy_events(self):
        with make_session(conf) as session:
            component_build = ComponentBuild()
            component_build.package = 'before_models_committed'
            component_build.scmurl = \
                ('git://pkgs.domain.local/rpms/before_models_committed?'
                 '#9999999999999999999999999999999999999999')
            component_build.format = 'rpms'
            component_build.task_id = 999999999
            component_build.state = 1
            component_build.nvr = ('before_models_committed-0.0.0-0'
                                   '.module_before_models_committed_0_0')
            component_build.batch = 1
            component_build.module_id = 1

            session.add(component_build)
            session.commit()

        with make_session(conf) as session:
            c = session.query(ComponentBuild).filter(ComponentBuild.id == 1).one()
            self.assertEquals(c.component_builds_trace[0].id, 1)
            self.assertEquals(c.component_builds_trace[0].component_id, 1)
            self.assertEquals(c.component_builds_trace[0].state, 1)
            self.assertEquals(c.component_builds_trace[0].state_reason, None)
            self.assertEquals(c.component_builds_trace[0].task_id, 999999999)

    def test_context_functions(self):
        """ Test that the build_context, runtime_context, and context hashes are correctly
        determined"""
        build = ModuleBuild.query.filter_by(id=1).one()
        mmd = modulemd.ModuleMetadata()
        yaml_path = os.path.join(
            os.path.dirname(__file__), '..', 'staged_data', 'testmodule_dependencies.yaml')
        mmd.load(yaml_path)
        build.modulemd = mmd.dumps()
        build.build_context, build.runtime_context = ModuleBuild.contexts_from_mmd(build.modulemd)
        self.assertEqual(build.build_context, 'f6e2aeec7576196241b9afa0b6b22acf2b6873d7')
        self.assertEqual(build.runtime_context, '1739827b08388842fc90ccc0b6070c59b7d856fc')
        self.assertEqual(build.context, 'e7a3d35e')
