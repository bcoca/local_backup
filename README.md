# local_backup
role that allows copying/moving remote backup_file to controller dir by config

To use just import the role and aftewards just use copy and other modules as normal.
If the `ANSIBLE_LOCAL_BACKUP` is set it will copy backup_file into that directory.
If the `ANSIBLE_REMOTE_BACKUP_CLEANUP` is also set it will remove the bakcup from the remote once copied.

```
- hosts: localhost
  gather_facts: false
  roles:
    - local_backup
  tasks:
    - copy: backup=yes src=testing2 dest=testing1

```

If running multiple plays you really only need to load once
```
- hosts: localhost
  gather_facts: false
  environment:
	ANSIBLE_LOCAL_BACKUP: /var/tmp/backups/
  roles:
    - local_backup

- hosts: yolo
  tasks:
    - copy: backup=yes src=testing2 dest=testing1
      environment:
	    ANSIBLE_LOCAL_BACKUP: /backupdir/
```

But if running against the controller, you need to set the envionrment vars before calling Ansible
```
ANSIBLE_LOCAL_BACKUP=/backups/ ansible-playbook ...

```
