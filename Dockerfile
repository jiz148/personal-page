# build python3.7
FROM python:3.7

# maintainer jinchi.ca@outlook.com
MAINTAINER jiz148

# config python evironment variables
ENV PYTHONUNBUFFERED 1

# 在容器内/var/www/html/下创建 mysite1文件夹
# in container /var/www/html/, make personal-page directory
RUN mkdir -p /var/www/html/personal-page

# set working directory
WORKDIR /var/www/html/personal-page

# add current files to working directory
ADD . /var/www/html/personal-page

# pip install
RUN pip install -r requirements.txt

# remove \r becuase start.sh is writen in Windows
RUN sed -i 's/\r//' ./start.sh

# set chmod of start.sy
RUN chmod +x ./start.sh
