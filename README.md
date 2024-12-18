# SimpleStudentCourseManagementSystem
Simple Student Course Management System, 简易学生选课管理系统

During Production, 还在制作中

## Version
#### Python version: 3.8.2
#### Django version: 2.2.11
install method:
```txt
pip3 install Django==2.2.11 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## TODO
- student opeartion
- search course
- form css



python manage.py makemigrations
python manage.py migrate

## TIPS
#### account
Teahcer:
任猎城
u: 1280000001
p: 12345678
镇天稽
u: 1110000001
p: 22334455
爱嘤诗贝伦
u: 1160000001
p: 12341234
牛有力
u: 2660000001
p: password



Student:
李大爽
u: 2020000001
p: libigshuang

张三
u: 2018000001
p: zhang333


2044000001
three12345

2020000002
xiaored



## Problems
#### 1 如何给Class-Based Views 的as_view()生成的view方法里面传参。
比如UpdateTeacherView和UpdateStudentView里面获取不到view方法传入的其他参数
解决方法： 重写get_context_data()， 在里面先写入固定的参数

# 选课系统部署指南

## 项目简介
这是一个基于Django开发的选课系统，支持教师和学生用户，具有课程管理、选课、评分、课程评教等功能。

## 环境要求
- Python 3.11+
- MySQL 8.0+
- 虚拟环境工具 (推荐使用 virtualenv)

## 安装步骤

1. **创建并激活虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
创建 `.env` 文件并添加以下配置：
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost:3306/database_name
ALLOWED_HOSTS=.example.com,localhost,127.0.0.1
```

4. **数据库迁移**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **创建超级用户**
```bash
python manage.py createsuperuser
```

## 部署步骤

### 使用 Gunicorn 和 Nginx 部署

1. **安装 Nginx**
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# CentOS
sudo yum install nginx
```

2. **配置 Nginx**
创建配置文件 `/etc/nginx/sites-available/select_class`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }

    location /media/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

3. **收集静态文件**
```bash
python manage.py collectstatic
```

4. **创建 Gunicorn 系统服务**
创建文件 `/etc/systemd/system/gunicorn.service`：
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=your-user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock select_class.wsgi:application

[Install]
WantedBy=multi-user.target
```

5. **启动服务**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Vercel部署指南

### 准备工作

1. **GitHub仓库设置**
   - 将项目推送到GitHub仓库
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <你的GitHub仓库URL>
   git push -u origin main
   ```

2. **Vercel账号设置**
   - 在 [Vercel](https://vercel.com) 注册账号
   - 关联你的GitHub账号

### 部署步骤

1. **在Vercel中导入项目**
   - 点击 "New Project"
   - 选择你的GitHub仓库
   - 选择 "Import"

2. **配置环境变量**
   在Vercel项目设置中添加以下环境变量：
   ```
   DEBUG=False
   ALLOWED_HOSTS=.vercel.app
   SECRET_KEY=<你的密钥>
   DATABASE_URL=<你的数据库URL>
   ```

3. **部署配置**
   - Framework Preset: 选择 "Other"
   - Build Command: `sh build_files.sh`
   - Output Directory: `staticfiles`
   - Install Command: `pip install -r requirements.txt`

4. **数据库配置**
   - 使用Vercel支持的数据库服务（如PostgreSQL）
   - 更新DATABASE_URL环境变量

### 部署后检查

1. **验证静态文件**
   - 检查CSS和JavaScript文件是否正确加载
   - 验证图片等媒体文件是否显示

2. **测试功能**
   - 测试用户登录/注册
   - 验证数据库操作
   - 检查文件上传功能

### 常见问题

1. **静态文件404**
   - 确保已运行 `python manage.py collectstatic`
   - 检查 `vercel.json` 中的静态文件路由配置

2. **数据库连接错误**
   - 验证DATABASE_URL格式
   - 确保数据库服务器允许Vercel IP访问

3. **部署失败**
   - 检查构建日志
   - 验证依赖版本兼容性
   - 确保所有必要的环境变量都已设置

### 更新部署

1. **推送更新**
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. **Vercel自动部署**
   - Vercel将自动检测更改并重新部署
   - 可在Vercel仪表板监控部署状态

## 安全配置

1. **更新 settings.py**
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
```

2. **配置 HTTPS**
建议使用 Let's Encrypt 获取免费的 SSL 证书：
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 维护说明

1. **数据库备份**
```bash
python manage.py dumpdata > backup.json
```

2. **更新代码后的操作**
```bash
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart gunicorn
```

## 常见问题排查

1. **检查日志**
```bash
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u gunicorn
```

2. **检查权限**
```bash
sudo chown -R www-data:www-data /path/to/your/project/static
sudo chown -R www-data:www-data /path/to/your/project/media
```

3. **测试 Gunicorn**
```bash
gunicorn --bind 0.0.0.0:8000 select_class.wsgi:application
```

## 性能优化建议

1. **配置缓存**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **静态文件处理**
- 使用 CDN
- 启用 Gzip 压缩
- 配置浏览器缓存

## 联系方式
如有问题，请联系系统管理员。