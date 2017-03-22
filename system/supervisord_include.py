#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

try:
    from ConfigParser import ConfigParser
except ImportError:
    configparser_found = False
else:
    configparser_found = True
import os
import re

def main():

    module = AnsibleModule(
        argument_spec=dict(
          name = dict(required=True)
#          include_files = dict(),
#          config = dict(),
#          params = dict(type='list')
        )
    )

    if not configparser_found:
        module.fail_json(msg="This module required installed ConfigParser python lib")

    name = module.params['name']
#    include_files = module.params['include_files']
#    config = module.params['config']
#    params = module.params['params']

    parser = ConfigParser()
#    if include_files:
#        config_file_path = include_files.replace('*', name)
#    if config:
#        parser.read(config)
#        include_files = parser.get('include', 'files')
#        config_file_path = include_files.replace('*', name)
#    else:
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read()
            if re.search('supervisord', cmdline):
                cmdline_array = cmdline.split('\x00')
                if '-c' in cmdline_array:
                    config_index = cmdline_array.index('-c') + 1
                elif '--configuration' in cmdline_array:
                    config_index = cmdline_array.index('--configuration') + 1
                else:
                    for element in cmdline_array:
                        if re.search('--configuration=', element):
                            config_index = element.split('=')[1]
                if not config_index:
                    config = '/etc/supervisord.conf'
                else:
                    config = cmdline_array[config_index]
        except IOError:
            continue
    try:
        if os.path.exists(config) and os.path.isfile(config):
            parser.read(config)
            include_files = parser.get('include', 'files')
            config_file_path = include_files.replace('*', name)
        else:
            module.fail_json(msg="File {} not found".format(config))
    except NameError:
        module.fail_json(msg="File {} not found".format(config))
   
    parser.read(config_file_path)
    names = []
    groups = []
    for section in parser.sections():
        if re.search('group:', section):
            groups.append(
              {
                'name': section.split(':', 1)[1],
                'programs': re.split(r'(?:,|\s)+', parser.get(section, 'programs'))
              }
            )
        if re.search('program', section):
            names.append(section.split(':', 1)[1])
    run_list = []
    for group in groups:
        for name in names:
            if name in group['programs']:
                run_list.append("{}:{}".format(group['name'], name))

    for name in names:
        if not re.search('pushme_', name):
            if 'environment' in parser.options("program:{}".format(name)):
                env = re.split('(?:,|\s)', parser.get("program:{}".format(name), 'environment'))
                break

    
    
    module.exit_json(changed=False, run_list=run_list, env=env)

            
         
    


from ansible.module_utils.basic import AnsibleModule, is_executable

if __name__ == '__main__':
    main()
