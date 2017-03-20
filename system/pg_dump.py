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
          dump_dir = dict(required=True),
          jobs = dict(type='int'),
          pg_bin_path = dict(required=False, type='path'),
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
    dump_dir = module.params['dump_dir']
    pg_bin_path = module.params['pg_bin_path']
    raw_params = module.params['raw_params']

    dump_name = "{}_{:%Y%m%d%H%M}".format(dbname, datetime.now())
    if os.path.exists(dump_dir) and os.path.isdir(dump_dir):
        if os.access(dump_dir, os.W_OK) and os.access(dump_dir, os.X_OK):
            dump_path = os.path.join(dump_dir, dump_name)
        else:
            module.fail_json(msg="Permission denied: {}".format(dump_dir))
    else:
        module.fail_json(msg="{} not found or it is not directory".format(dump_dir))

    args = []
    if password:
        args.append("PGPASSWORD={}".format(password))
    if pg_bin_path:
        pg_dump_path = os.path.join(pg_bin_path, 'pg_dump')
        if os.path.exists(pg_dump_path) and is_executable(pg_dump_path):
            args.append(pg_dump_path)
        else:
            module.fail_json(msg="pg_dump not found in specified path")
    else:
        args.append(module.get_bin_path("pg_dump", True))
    if host:
        args.append("--host={}".format(host))
    if port:
        args.append("--port={}".format(port))
    if jobs:
        args.append("--jobs={}".format(jobs))
    if dump_format:
        args.append("--format={}".format(dump_format))
    if dump_path:
        args.append("--file={}".format(dump_path))
    if dbname:
        args.append("--dbname={}".format(dbname))
    if raw_params:
        for param in raw_params:
            args.append(param)

#    module.run_command(args, check_rc=True)
    module.exit_json(changed=True, args=args, raw_params=raw_params)



from ansible.module_utils.basic import AnsibleModule, is_executable

if __name__ == '__main__':
    main()
