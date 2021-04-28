# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import constants as C
from ansible.module_utils.backup import local_backup
from ansible.plugins.action import ActionBase
from ansible.utils.vars import merge_hash


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):

        # individual modules might disagree but as the generic the action plugin, pass at this point.
        self._supports_check_mode = True
        self._supports_async = True

        result = super(ActionModule, self).run(tmp, task_vars)

        if not result.get('skipped'):

            if result.get('invocation', {}).get('module_args'):
                # avoid passing to modules in case of no_log
                # should not be set anymore but here for backwards compatibility
                del result['invocation']['module_args']

            # FUTURE: better to let _execute_module calculate this internally?
            wrap_async = self._task.async_val and not self._connection.has_native_async

            # do work!
            result = merge_hash(result, self._execute_module(task_vars=task_vars, wrap_async=wrap_async))

        if not wrap_async:
            local_backup(self, task_vars, result)

            # remove a temporary path we created
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
