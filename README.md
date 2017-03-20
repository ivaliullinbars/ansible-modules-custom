## Custom Ansible modules

### pg_dump module params

| parameter       | required | default  | choices   | comment                                      |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **dbname**      | yes      |          |           | --dbname=**dbane**                           |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **username**    | no       | postgres |           | --username=**username**                      |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **password**    | no       |          |           | PGPASSWORD=**password**                      |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **host**        | no       |          |           | --host=**host**                              |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **port**        | no       | 5432     |           |                                              |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **dump_format** | no       | custom   | custom    | --format=**dump_format**                     |
|                 |          |          | directory |                                              |
|                 |          |          | plain     |                                              |
|                 |          |          | tar       |                                              |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **dump_dir**    | no       |          |           | Path to backup dir                           |
|                 |          |          |           | By default use user $HOME dir                |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **jobs**        | no       |          |           | --jobs=**jobs**                              |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **pg_bin_path** | no       |          |           | Irregular path to pg bin's                   |
|-----------------|----------|----------|-----------|----------------------------------------------|
| **raw_params**  | no       |          |           | Another pg_dump options in list on by string |


### Example

Playbook pg_dump:
```
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
```
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
