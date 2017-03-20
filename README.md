## Custom Ansible modules

### pg_dump module params

| parameter | required | default | choices | comment |
|-----------|----------|---------|---------|---------|
| dbname | yes | | | --dbname=**dbane** |
| username | no | postgres | | --username=**username** |
| password | no | | | PGPASSWORD=**password** |
| host | no | | | --host=**host** |
| port | no | 5432 | | --port=**port** |
| dump_format<br><br><br><br> | no<br><br><br><br> | custom<br><br><br><br> | custom<br>directory<br>plain<br>tar | --format=**dump_format**<br><br><br><br> |
| dump_dir<br><br> | no<br><br> | | | Path to backup dir<br>By default use user $HOME dir |
| jobs | no | | | --jobs=**jobs** |
| pg_bin_path | no |          |           | Irregular path to pg bin's                   |
| raw_params | no | | | Another pg_dump options in list on by string |

### pg_restore module params

| parameter | required | default | choices | comment |
|-----------|----------|---------|---------|---------|
| dbname | yes | | | --dbname=**dbane** |
| username | no | postgres | | --username=**username** |
| password | no | | | PGPASSWORD=**password** |
| host | no | | | --host=**host** |
| port | no | 5432 | | --port=**port** |
| dump_format<br><br><br><br> | no<br><br><br><br> | custom<br><br><br><br> | custom<br>directory<br>plain<br>tar | --format=**dump_format**<br><br><br><br> |
| dump_dir<br><br> | no<br><br> | | | Path to backup dir<br>By default use user $HOME dir |
| jobs | no | | | --jobs=**jobs** |
| pg_bin_path | no |          |           | Irregular path to pg bin's                   |
| role | no | | | --role=**role** |
| no_owner | no | | | --no-owner |
| raw_params | no | | | Another pg_dump options in list on by string |

### Example

Playbook pg_dump:
```yml
- name: pg_dump task
  pg_dump:
    dbname: test_db_name
    username: test_user_name
    password: test_user_pass
    host: "192.168.1.1"
    port: 5433
    dump_format: directory
    dump_dir: "/backups"
    jobs: 4
    pg_bin_path: "/usr/pgsql-9.6/bin"
    raw_params: ["--schema-only"]
```

Playbook pg_restore:
```yml
- name: pg_restore task
  pg_restore:
    dbname: test_db_name
    username: test_user_name
    password: test_user_pass
    host: "192.168.1.2"
    port: 5434
    dump_format: custom
    dump_path: "/backups/test_db_name_201703200030"
    jobs: 2
    pg_bin_path: "/usr/pgsql-9.6/bin"
    role: postgres
    no_owner: yes
    raw_params: ["--table=south_migrations"]
```

### Usage

Export ANSIBLE_LIBRARY environment variable. Like:
```
export ANSIBLE_LIBRARY=/home/q/Desktop/git/ansible-modules-custom:/home/q/.ansible/modules
```
*/home/q/Desktop/git/ansible-modules-custom* - path to this repo files
