## 项目描述

从政府网站抓取每天各城区的房子销售情况，目前只抓取了成都时公布的各城区数据。

## 本地分析

    $ python plot.py

## Heroku 部署

Travis CI 中的 `Cron Job` 不支持每天具体的时间点触发，只可以选择 `Daily/Hourly`等，所以，选用 `Heroku`。

Heroku 同时支持该项目的 Web 页面显示。

部署过程参考官方文档，定时任务用了 `Heroku Scheduler addons`。

## 部署到服务器

### 安装 pyenv

### 安装项目依赖包

    $ pip install -r requirements.txt

### 设置系统时区

将系统时区设置为 `Asia/Shanghai`

    $ sudo dpkg-reconfigure tzdata

查看系统时区：

    $ cat /etc/timezone

### 部署展示页面

    $ /data/pyenv/versions/3.6.3/envs/daily-house-deal/bin/python run.py

(可选)，通过 supervisor 管理：

    $ cat /etc/supervisor/conf.d/daily-house-deal.conf
    [program:daily-house-deal]
    command=/data/pyenv/versions/3.6.3/envs/daily-house-deal/bin/python run.py
    directory=/data/web/daily-house-deal
    user=wm
    numprocs=1
    priority=999
    autostart=true
    autorestart=true
    startsecs=10
    startretries=10
    exitcodes=0,2
    stopsignal=QUIT
    redirect_stderr=false
    stdout_logfile=/data/log/supervisor/daily-house-deal_stdout.log
    stdout_logfile_maxbytes=10MB
    stdout_logfile_backups=10
    stdout_capture_maxbytes=10MB
    stdout_events_enabled=false
    stderr_logfile=/data/log/supervisor/daily-house-deal_stderr.log
    stderr_logfile_maxbytes=1MB
    stderr_logfile_backups=10
    stderr_capture_maxbytes=1MB

(可选)，通过 nginx 做反向代理：

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:5001;
    }

### 设置 crontab

每晚23:58:00 自动抓取数据，crontab 设置如下：

    # m h  dom mon dow   command
    58 23 * * * cd /data/web/daily-house-deal && /data/pyenv/versions/3.6.3/envs/daily-house-deal/bin/python daily_deal.py && sudo supervisorctl restart daily-house-deal

注：通过 dash 写了个简单的展示页面，每次更新完数据，重启服务，让它基于最新数据展示。
