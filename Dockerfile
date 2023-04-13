FROM ultrafunk/undetected-chromedriver

WORKDIR /root/app
COPY requirements.txt /root/app

CMD pip install -r requirements.txt

