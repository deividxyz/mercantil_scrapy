FROM ubuntu
MAINTAINER IL DEIVID https://www.deivid.xyz

# Instalando python y dependencias dpkg

RUN apt-get update && apt-get install -y python3 && apt-get install -y ipython3 && apt-get install -y python3-pip && apt-get install -y libssl-dev && apt-get install -y tor && apt-get install -y privoxy && apt-get install -y curl && apt-get install -y netcat && apt-get install -y libffi-dev 

# Instalando paquetes de python

RUN pip3 install scrapy && pip3 install stem && pip3 install requests && pip3 install scrapy-fake-useragent

# Config TOR

RUN echo "ControlPort 9051" >> /etc/tor/torrc

RUN echo HashedControlPassword $(tor --hash-password "my password" | tail -n 1) >> /etc/tor/torrc

# Config Privoxy

RUN echo "forward-socks5t / 127.0.0.1:9050 ." >> /etc/privoxy/config

RUN service tor start && service privoxy start

# Copio scraper a directorio home de imagen virtual

COPY mercantil /home/mercantil

# Parches para Scrapy (TOR y bypass de redirección 302)

COPY parches/tor_controller.py /usr/local/lib/python3.5/dist-packages/scrapy/utils
COPY parches/redirect.py /usr/local/lib/python3.5/dist-packages/scrapy/downloadermiddlewares

# creando archivos ejecutables

RUN chmod +x /home/mercantil/start.sh

# el archivo code representa la categoría del sitio (se encuentran aprox 15000 en el sitio), y lastmsg representa la página actual de la categoría

RUN echo 1 > /home/mercantil/code
RUN echo 0 > /home/mercantil/lastmsg

# Registrando proxy TOR como proxy de sistema

ENV HTTPS_PROXY https://127.0.0.1:8118
ENV HTTP_PROXY http://127.0.0.1:8118

