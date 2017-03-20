#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

from datetime import datetime
import os

def main():

    module = AnsibleModule(
        argument_spec=dict(
          dbname = dict(required=True),
          username = dict(default="postgres"),
          password = dict(default="", no_log=True),
          host = dict(default=""),
          port = dict(default=5432),
          dump_format = dict(default='custom', choises=['plain', 'custom', 'directory', 'tar']),
          dump_path = dict(required=True),
          jobs = dict(type='int'),
          pg_bin_path = dict(required=False, type='path'),
          role = dict(),
          no_owner = dict(default=False, type='bool'),
          raw_params = dict(type='list')
        )
    )

    dbname = module.params['dbname']
    username = module.params['username']
    password = module.params['password']
    host = module.params['host']
    port = module.params['port']
    jobs = module.params['jobs']
    dump_format = module.params['dump_format']
    dump_path = module.params['dump_path']
    pg_bin_path = module.params['pg_bin_path']
    role = module.params['role']
    no_owner = module.params['no_owner']
    raw_params = module.params['raw_params']

    if not os.path.exists(dump_path) or not os.access(dump_path, os.R_OK):
        module.fail_json(msg="{} not found or permissions denied".format(dump_path))

    args = []
    if password:
        args.append("PGPASSWORD={}".format(password))
    if pg_bin_path:
        pg_restore_path = os.path.join(pg_bin_path, 'pg_restore')
        if os.path.exists(pg_restore_path) and is_executable(pg_restore_path):
            args.append(pg_restore_path)
        else:
            module.fail_json(msg="pg_restore not found in specified path")
    else:
        args.append(module.get_bin_path("pg_restore", True))
    if host:
        args.append("--host={}".format(host))
    if port:
        args.append("--port={}".format(port))
    if jobs:
        args.append("--jobs={}".format(jobs))
    if dump_format:
        args.append("--format={}".format(dump_format))
    if dbname:
        args.append("--dbname={}".format(dbname))
    if role:
        args.append("--role={}".format(role))
    if no_owner:
        args.append("--no-owner".format(no_owner))
    if raw_params:
        for param in raw_params:
            args.append(param)
    if dump_path:
        args.append("{}".format(dump_path))

    module.run_command(args, check_rc=True)
    module.exit_json(changed=True, args=args, raw_params=raw_params)



from ansible.module_utils.basic import AnsibleModule, is_executable

if __name__ == '__main__':
    main()
