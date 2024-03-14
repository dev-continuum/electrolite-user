# electrolite-user
### Introduction:  
This project provides user side API's which will be integrated to the Android and iOS Apps

### To run the web app locally 
1. Export environment variables:  
    `export ACTIVE_ENVIRONMENT dev`  
    `export AWS_ACCESS_KEY_ID <aws_id>`  
    `export AWS_SECRET_ACCESS_KEY <aws secret key>`  
2. In project's virtual env run main.py file:  
    `python main.py`  
3. In local env better to configure it in pycharm.   
    It will be easier to debug.  

   
### To run the web app on stage 
1. Export environment variables:  
    `export ACTIVE_ENVIRONMENT dev`  
    `export AWS_ACCESS_KEY_ID <aws_id>`  
    `export AWS_SECRET_ACCESS_KEY <aws secret key>`  
2. In project's virtual env run main.py file:  
    `gunicorn -k uvicorn.workers.UvicornWorker app:app` 

   
### To run the web app on prod 

#### Deployment
- Currently Deployed on EC2 as a linux service  
- This service then communicates to Nginx  
- Nginx is mapped to load balancer  
- Load balancer is mapped to route53 and utilizes the https certificate from aws

1. Export environment variables:  
    `export ACTIVE_ENVIRONMENT dev`  
    `export AWS_ACCESS_KEY_ID <aws_id>`  
    `export AWS_SECRET_ACCESS_KEY <aws secret key>`   

  
#### Create linux service:  
1. got to cd /etc/systemd/system/
2. create file electrolite.service
3. add this content  
   ```
    [Unit]
    Description=Gunicorn instance for webhook web server
    After=network.target
    [Service]
    WorkingDirectory=/home/ubuntu/electrolite-user
    ExecStart=/home/ubuntu/electrolite-user/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker app:app --timeout 600 --access-logfile /home/ubuntu/electrolite-user-logs/gunicornlogs.log
    Restart=always
    [Install]
    WantedBy=multi-user.target
    ```
4. configure nginx proxy  
  ```
upstream uvicorn {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response

    # for a TCP configuration
     server 0.0.0.0:8000 fail_timeout=0;
     # server unix:/tmp/uvicorn.sock;
  }


  map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
  }



server {
        listen 80 default_server;
        listen [::]:80 default_server;


        server_name _;

    location / {
      # checks for static file, if not found proxy to app
       try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header Host $http_host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
      proxy_redirect off;
      proxy_buffering off;
      proxy_pass http://uvicorn;
      add_header 'Access-Control-Allow-Origin' '*';
      add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
      add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
      add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
    }

}
```

5. start electrolite service  
    ``sudo systemctl daemon-reload``  
    ``sudo systemctl start electrolite.service``
6. restart nginx  
    ``sudo systemctl restart nginx``
