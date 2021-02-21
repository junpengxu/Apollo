## 迭代介绍

### 版本号修改规则
- 增加完全独立的模型，修改第一位，整体功能上的新增, 修改第二位，功能上的优化修改第三位

### v 1.0.0
- 将创建爬虫任务简化，只需要提交需要爬取的帖子id，实现爬取整个帖子数据。
- 扫描任务的方式可以考虑通过扫redis，或者是mysql

### v 1.0.1
- 增加查询爬虫结果的详情页面，现实当前爬取的进度，帖子的简要信息，以列表的形式展示出次帖子已经爬取的post, 需要查看回复数据的话，再请求接口拉数据。这样做是为了避免后面数据量大了之后产生数据库层面的瓶颈

### nginx config
```
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
```

### supervisor.conf
- Apollo
```
[program:Apollo]
directory=/home/weakee/project/Apollo/server
command=/root/anaconda3/bin/gunicorn -w 3 -t 120 manage:app
autostart=true
autorestart=true
killasgroup=true
stopasgroup=true
stdout_logfile=/home/server/logs/%(program_name)s-stdout.log
stderr_logfile=/home/server/logs/%(program_name)s-stderr.log
stdout_logfile_maxbytes=1024MB
stdout_logfile_backups=5
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel=info
priority=1100
```

- Apollo-celery
```
[program:Apollo-celery]
directory=/home/weakee/project/Apollo/server
command=/root/anaconda3/bin/celery -A app.celery worker -c 8 -l INFO
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/home/server/logs/%(program_name)s-stdout.log
stderr_logfile=/home/server/logs/%(program_name)s-stderr.log
stdout_logfile_maxbytes=1024MB
stdout_logfile_backups=5
stdout_capture_maxbytes=1MB
stdout_events_enabled=false
loglevel=info
priority=1100
```