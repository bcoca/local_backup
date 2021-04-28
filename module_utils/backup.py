# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os


def local_backup(action, task_vars, result):

    dest = os.environ.get('ANSIBLE_LOCAL_BACKUP')

    if 'backup_file' in result and dest:
        result['backup_file_removed'] = False
        host = task_vars.get('inventory_hostname')

        new_task = action._task.copy()
        new_task.args=dict(src=result['backup_file'], dest=dest)
        fetch_action = action._shared_loader_obj.action_loader.get('ansible.legacy.fetch',
                                                                  task=new_task,
                                                                  connection=action._connection,
                                                                  play_context=action._play_context,
                                                                  loader=action._loader,
                                                                  templar=action._templar,
                                                                  shared_loader_obj=action._shared_loader_obj)
        backup = fetch_action.run(task_vars=task_vars)
        if backup.get('failed'):
            action._display.warning("Unable to backup '%s' from %s: %s" % (result['backup_file'], host, backup.get('msg')))
        else:
            action._display.vvv("Backup '%s' from %s successful, to: %s" % (result['backup_file'], host, dest))
            result['controller_backup'] = dest
            module_args = dict(
                path=result['backup_file'],
                state='absent'
            )
            cleanup = os.environ.get('ANSIBLE_REMOTE_BACKUP_CLEANUP')
            if cleanup:
                destroy = action._execute_module(module_name='ansible.legacy.file', module_args=module_args, task_vars=task_vars, wrap_async=False)
                if destroy.get('failed'):
                    err = 'No feedback given by module'
                    for msg in ('module_stderr', 'stderr', 'module_stdout', 'stdout', 'msg'):
                        if destroy.get(msg):
                            err = destroy[msg]
                    action._display.warning('Unable to remove remote backup (%s): %s' % (result['backup_file'], err))
                else:
                    result['remote_backup_removed'] = True
