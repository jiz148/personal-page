# build python3.7
FROM python:3.7

# maintainer jinchi.ca@outlook.com
MAINTAINER jiz148

# config python evironment variables
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/var/www/html/myproject
# in container /var/www/html/, make personal-page directory
RUN mkdir -p $APP_HOME

# set working directory
WORKDIR $APP_HOME

# add current files to working directory
ADD . $APP_HOME

# pip install
RUN pip install -r requirements.txt

# remove \r becuase start.sh is writen in Windows
RUN sed -i 's/\r//' ./start.sh
RUN cat ./start.sh

# set chmod of start.sh
RUN chmod +x ./start.sh

# DJ pw
RUN export DJ_SECRET_KEY='gqptn5bq0l2\$_t=v+^xtj5_+m+7z$76njld5h06!3-+t&vt97'

# start service
ENTRYPOINT ["./start.sh"]
