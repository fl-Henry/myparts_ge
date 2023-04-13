FROM ultrafunk/undetected-chromedriver

EXPOSE 5900

WORKDIR /root/app
COPY requirements.txt /root/app
COPY app/debug.sh /root/app

RUN cat ./debug.sh > /entrypoint.sh

# RUN pip install -r requirements.txt > /dev/null

# ENTRYPOINT ./DEBUG.sh
# ENTRYPOINT ./debug.sh

