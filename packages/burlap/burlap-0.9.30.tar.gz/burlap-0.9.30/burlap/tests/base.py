from __future__ import print_function

import os
import sys
import unittest
from commands import getstatusoutput
# from pprint import pprint

from burlap.common import set_state, get_state, clear_state, init_env, default_env, env, all_satchels, get_dryrun, set_dryrun, get_verbose, set_verbose
from burlap.deploy import init_env as deploy_init_env, delete_plan_data_dir, clear_fs_cache

def clear_runs_once(func):
    if hasattr(func, 'return_value'):
        print('clearing runs_once on %s' % func)
        print('return_value:', func.return_value)
        print('return_value:', func.wrapped.return_value)
        print('__dict__:', func.__dict__)
        # Fabric wraps function using a class that passes through get/hasattr
        # so we have to try deleting the attribute on a few levels.
        try:
            delattr(func, 'return_value')
        except AttributeError:
            pass
        try:
            delattr(func.wrapped, 'return_value')
        except AttributeError:
            pass
        assert not hasattr(func, 'return_value'), 'Unable to clear runs_once on %s' % func

class TestCase(unittest.TestCase):

    test_name_fout = sys.stdout

    test_name_format = '\n{bar}\nRunning test: {name}\n{bar}\n'

    # These keys will not be cleared between tests.
    # This is useful for keeping the Vagrant login, which is only set once before all the tests are run.
    keep_env_keys = []

    def getstatusoutput(self, cmd):
        print(cmd)
        status, output = getstatusoutput(cmd)
        print('output:', output)
        return status, output

    def get_keep_env_keys(self):
        return list(self.keep_env_keys)

    def clear_env(self):
        keep_env_keys = set(self.get_keep_env_keys())
        for k, v in env.items():
            if k in keep_env_keys:
                continue
            del env[k]

    def update_env(self, d):
        keep_env_keys = set(self.get_keep_env_keys())
        for k, v in default_env.items():
            if k in keep_env_keys:
                continue
            env[k] = v

    def setUp(self):
        # Always print the current test name before the test.
        rows, columns = map(int, os.popen('stty size', 'r').read().split())
        kwargs = dict(
            bar='#'*columns,
            name=self._testMethodName,
        )
        print(self.test_name_format.format(**kwargs), file=self.test_name_fout)

        # Save fabric state.
        self._env = env.copy()
#         print('before env clear:')
#         pprint(env, indent=4)

        # Reset fabric state.
        #self.clear_env()
        #self.update_env(default_env)
        init_env()
        deploy_init_env()

        # Save cwd.
        self._cwd = os.getcwd()
        print('cwd:', self._cwd)

        # Save burlap state.
        self._burlap_state = get_state()

        self._dryrun = get_dryrun()
        self._verbose = get_verbose()

        # Clear runs_once on legacy runs_once methods.
        from burlap import deploy, manifest
        modules = [deploy, manifest]
        for module in modules:
            for name in dir(module):
                func = getattr(module, name)
                if not callable(func):
                    continue
                clear_runs_once(func)

        # Clear runs_once on our custom runs_once methods.
        from burlap.common import runs_once_methods
        for meth in runs_once_methods:
            clear_runs_once(func)

        # Ensure all satchels re-push all their local variables back into the global env.
        for satchel in all_satchels.values():
            satchel.register()
            satchel.clear_caches()

        # Since these tests are automated, if we ever get a prompt, we should immediately fail,
        # because no action should ever be user-interactive.
        env.abort_on_prompts = True
        env.always_use_pty = False

        delete_plan_data_dir()

        clear_fs_cache()

        super(TestCase, self).setUp()

    def tearDown(self):

        set_dryrun(self._dryrun)
        set_verbose(self._verbose)

        # Restore CWD.
        os.chdir(self._cwd)

        # Restore fabric state.
        self.clear_env()
        self.update_env(self._env)

        # Restore burlap state.
        clear_state()
        set_state(self._burlap_state)

        super(TestCase, self).tearDown()
