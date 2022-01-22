FROM ubuntu:21.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y install \
  curl \
  bzip2

RUN curl -fL 'https://download.foldingathome.org/releases/public/release/fahclient/debian-stable-arm64/v7.6/fahclient_7.6.21_arm64.deb' > /fahclient.deb
# Install Folding@home
ADD sample-config.xml /usr/share/doc/fahclient/sample-config.xml
RUN dpkg -i /fahclient.deb
RUN rm /fahclient.deb

CMD FAHClient --config /etc/fahclient/config.xml