FROM python:3

WORKDIR /home/ds
COPY . .

RUN \
    apt-get update && apt-get install -y telnetd whiptail && pip3 install whiptail requests && \
    useradd -m -p 2x18umS4zt3tE -s /home/ds/main.py ds

CMD ["/usr/sbin/inetd", "-d"]
