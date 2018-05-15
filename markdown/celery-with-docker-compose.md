title: 使用非root用户在容器中运行celery
date: 2017-12-17 20:45:11
---

在 docker 环境中， 如果使用 root 用户运行 celery worker会有下面才警告出现. 虽然可以通过`C_FORCE_ROOT`环境变量来避免这个问题。 但毕竟 celery 官方并不推荐使用 root。好在 docker-compose 有user参数指定用户.

```text
 RuntimeWarning: You're running the worker with superuser privileges: this is
absolutely not recommended!

Please specify a different user using the -u option.

User information: uid=0 euid=0 gid=0 egid=0

  uid=uid, euid=euid, gid=gid, egid=egid,
```


## `docker-compose.yml`

```yaml
  celery_worker:
    build: .
    user: nobody #add
    env_file: '.env'
    entrypoint: ./entrypoint.sh "worker"
    volumes_from:
      - web
    depends_on:
      - web

  celery_beat:
    build: .
    user: nobody #add
    env_file: '.env'
    entrypoint: ./entrypoint.sh "beat"
    volumes_from:
      - web
    depends_on:
      - web
```
