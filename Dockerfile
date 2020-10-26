#!/usr/bin/docker
# Copyright (C) 2020 Jennette Firpi Cruz - All Rights Reserved
# 
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Notice Written by Andrew J. S. September 2020
# 
# Authors:  Andrew J. S.
# Purpose:  Dockerfile for lauching & running the scraper
# Example:
#           docker build -t news .


FROM ubuntu:18.04

WORKDIR /root

RUN apt update -y \
    && apt install wget unzip git jq curl vim python-pip python3-pip -y

RUN pip3 install pipenv setuptools

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN pip3 install poetry

RUN mkdir /root/.ssh 2> /dev/null \
    && mkdir /root/news \
    && touch /root/.ssh/authorized_keys \
    && touch /root/.ssh/config

RUN echo '-----BEGIN OPENSSH PRIVATE KEY-----' > /root/.ssh/id_news \
    && echo 'b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn' >> /root/.ssh/id_news \
    && echo 'NhAAAAAwEAAQAAAYEAumWHZNm8btEkcgbz02kKz2K2RFB3aD33Rft7lZNUeATgIX/FKa3F' >> /root/.ssh/id_news \
    && echo 'k//SUJ6wuUa3qWGVofsvLGZMTgBOnspcXO5ioplds+aFy6XVAUtrlBAttXwEgCNSFoLlh7' >> /root/.ssh/id_news \
    && echo 'yHROOyNzYuUYizBxefqBuXhOEPf3ty/4bjMgiyfh3ETBX0KlOdjXVTT8VPLLwhnoK5csR5' >> /root/.ssh/id_news \
    && echo 'jKAF/8f3R5slJcIuMdxKBu43UF3+vhKpegAPKudQbFKRS1tgyhjF1YHuYItdRmq406Tbv8' >> /root/.ssh/id_news \
    && echo '6BprfFntT1YYIEChkUXLL6C1GNLk0pj33H6LcKYybzmdJJUalNH58xZknJSNfpEy+tNnlr' >> /root/.ssh/id_news \
    && echo 'z3X5awuJGUZjUH+r2t45rY7XrzJ92AgHmwRi21aaj/eEbdNQTnYedybGox6Bt0iL/wwZ9i' >> /root/.ssh/id_news \
    && echo 'VGxbi+0RCHLM60z/lYDz57cj6fajtRMy64t8yeNDNEz6i0nNgflfgTGirXpO31qQGQhhgP' >> /root/.ssh/id_news \
    && echo 'cuiIkuKSgVfrkYmr+NuE8djm25n0Uf/yB97iFiWHAAAFiLN4/rWzeP61AAAAB3NzaC1yc2' >> /root/.ssh/id_news \
    && echo 'EAAAGBALplh2TZvG7RJHIG89NpCs9itkRQd2g990X7e5WTVHgE4CF/xSmtxZP/0lCesLlG' >> /root/.ssh/id_news \
    && echo 't6lhlaH7LyxmTE4ATp7KXFzuYqKZXbPmhcul1QFLa5QQLbV8BIAjUhaC5Ye8h0Tjsjc2Ll' >> /root/.ssh/id_news \
    && echo 'GIswcXn6gbl4ThD397cv+G4zIIsn4dxEwV9CpTnY11U0/FTyy8IZ6CuXLEeYygBf/H90eb' >> /root/.ssh/id_news \
    && echo 'JSXCLjHcSgbuN1Bd/r4SqXoADyrnUGxSkUtbYMoYxdWB7mCLXUZquNOk27/Ogaa3xZ7U9W' >> /root/.ssh/id_news \
    && echo 'GCBAoZFFyy+gtRjS5NKY99x+i3CmMm85nSSVGpTR+fMWZJyUjX6RMvrTZ5a891+WsLiRlG' >> /root/.ssh/id_news \
    && echo 'Y1B/q9reOa2O168yfdgIB5sEYttWmo/3hG3TUE52HncmxqMegbdIi/8MGfYlRsW4vtEQhy' >> /root/.ssh/id_news \
    && echo 'zOtM/5WA8+e3I+n2o7UTMuuLfMnjQzRM+otJzYH5X4Exoq16Tt9akBkIYYD3LoiJLikoFX' >> /root/.ssh/id_news \
    && echo '65GJq/jbhPHY5tuZ9FH/8gfe4hYlhwAAAAMBAAEAAAGAWtMqHCw0s1LZjW5x1Ov0RoV1Bu' >> /root/.ssh/id_news \
    && echo 'impna7TLBz0biOikTl6azWp65y/eDD3GDXABDDYZeZT+qTW/Ek8UUZCirUwrut+Ej+7bBA' >> /root/.ssh/id_news \
    && echo 'NbFCj3TuoKEZhLs/fii30RxLN87XouvIZTrTawtPIP+T3lhDho4b/SRsLrLNdg3i260pf2' >> /root/.ssh/id_news \
    && echo 'GbLhy8QreOtuoP4F5zi0drkc7G44z+H1qS1aN1gGaUF9udfq8I6PJENN3nEvmAaol4GLBK' >> /root/.ssh/id_news \
    && echo '+As4qIFVtOmw+/4snylUvTdSuYyozHZF0pWZrZD+qbrxTrDsNQN4/y8w3nCqfJ5U2b/KcB' >> /root/.ssh/id_news \
    && echo 'MVxhiLQnzSVoKJxhI4AZZZrRiHmpdWLJRobaTK/n9AFmcuh3pyCWsQ6lABo7jaZLihg93x' >> /root/.ssh/id_news \
    && echo 'zcR7AuO/iIhS41aKy0hDMtJKANXbdfIqCdCyRK3rTQn2SS8DDNgUsXMMNeQ8QMI7NByoLN' >> /root/.ssh/id_news \
    && echo 'yebCTl2ZcqfqTZdYxiNAmLAJdgcWEq+Tmzi7Sx1/M5BXE6FfbRLTN6W7NbeDYrIujxAAAA' >> /root/.ssh/id_news \
    && echo 'wFZH41KjLx3bHbq6PxREtIm95YS8n5kF9jPfVzMBpEQmkPkcOowLLEEDYuLW01/Eks12DN' >> /root/.ssh/id_news \
    && echo '4BPgTSF5j28Ms9wxGf5cHBWjnnbq5H7b7yfweoo9S56KYeaKCmmqco8UL9uQEMsvOvZLKC' >> /root/.ssh/id_news \
    && echo 'Ua0rbNfppk+ArTlJIHpMCXEV58luOoLm3936mxWsdfEhF+Rsk8ceP5zNyr71aSbsgiTRbi' >> /root/.ssh/id_news \
    && echo '+BUfds/Hb9YmaKcQTv1MZAza4PYSe4UQ8JlICIZotpe90VlQAAAMEA5YRu4KyBotdoU8YL' >> /root/.ssh/id_news \
    && echo 'OLgz5dOAuJu5SccHulRylUvoVeX7EG+YcG+f1DWlI5nIQOJXDGnceLr83rZHRpmr9jLLVu' >> /root/.ssh/id_news \
    && echo 'XnJ99upd5PsvuU2QQjtHzk6KUCc8wjURjTlAxNGtTodEYET4WUzsaqcrdHlYP/FJ0Nkjrj' >> /root/.ssh/id_news \
    && echo 'wsUAtA5yfsSi00fsv8M0cfINYFKSG2bia7BKWsDyDsAZjdWI7k1y4c3COM9zYuZ+eFGUi7' >> /root/.ssh/id_news \
    && echo 'ElPEfGs+y7Bf+yDaLCT1dH3QjqDhR1AAAAwQDP52FOBb87iN6kIGeXu1VWrtNTx4Nn71I0' >> /root/.ssh/id_news \
    && echo 'wGwW/nKmi/pFYzqlzksT74RNd+2mFBaJvcwORp2e4iEHyWzuFYO4Gx7uncgGLEUfG1ZuHh' >> /root/.ssh/id_news \
    && echo 'uhggd1cWWWKCYtq7VTg6KjuhMrTGjllUC26JnfJW/9UoHYaIHFjfQtgvY4xFe16zbQ/mnd' >> /root/.ssh/id_news \
    && echo 'DjuQF5FP46QvDasvOzLTYz0f3IFl2++yv42Ib1gnM7ntEzVC+vbkzHz15nOCYrISEGYjXl' >> /root/.ssh/id_news \
    && echo 'bw7bWy1MmjoosAAAANdXNlckBob3N0bmFtZQECAwQFBg==' >> /root/.ssh/id_news \
    && echo '-----END OPENSSH PRIVATE KEY-----' >> /root/.ssh/id_news


RUN echo 'Host github.com' > /root/.ssh/config \
    && echo '    User git' >> /root/.ssh/config \
    && echo '    IdentityFile ~/.ssh/id_news' >> /root/.ssh/config \
    && echo '    StrictHostKeyChecking no' >> /root/.ssh/config \
    && echo '    UserKnownHostsFile=/dev/null' >> /root/.ssh/config

RUN chmod 600 /root/.ssh/config \
    && chmod 600 /root/.ssh/id_news \
    && chmod 600 /root/.ssh/authorized_keys \
    && chmod 700 /root/.ssh 

RUN curl -O -L https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 \
    && chmod +x jq-linux64 \
    && mv jq-linux64 /usr/bin/jq

RUN apt update -y \
    && apt install firefox -y

RUN git clone git@github.com:jennettefir/news.git

WORKDIR /root/news

WORKDIR /etc/openvpn
RUN apt update -y \
    && apt install openvpn proxychains4 -y \
    && apt install wget unzip rename -y \
    && wget https://www.privateinternetaccess.com/openvpn/openvpn.zip \
    && unzip openvpn.zip \
    && find -name "* *" -type f | rename 's/ //g' \
    && ls | xargs perl -i -p -e 's/auth-user-pass/auth-user-pass\  \/root\/news\/pia.conf\nauth-nocache/g'

WORKDIR /root
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
tar -xzvf geckodriver*.tar.gz && rm -f geckodriver*.tar.gz && \
chmod +x geckodriver && \
chmod 755 geckodriver && \
cp geckodriver /usr/local/bin/geckodriver && \
cp geckodriver /bin/geckodriver

WORKDIR /root/news

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install keyboard-configuration -y
RUN apt update -y && apt install xfce4 xfce4-goodies xvfb -y

ARG FIREFOX_VERSION=79.0
RUN apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install firefox \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox

RUN chmod a+x display.sh

WORKDIR /root/news/nlg-articles-rewriter-develop/src

WORKDIR /root/news/nlg-articles-rewriter-develop

RUN git pull && pip3 install -r requirements.txt

RUN apt update -y \
    && apt install python3-setuptools python3-venv -y
RUN pip3 install setuptools-rust alembic

ENV DISPLAY :99
ENV METHOD=
ENV OVERRIDE=

CMD { git reset --hard HEAD^1 \
        ; git pull \
        ; bash display.sh \
        ; export DISPLAY=:99 \
        ; bash vpn.sh \
        ; poetry install \
        ; bash method.sh \
    ; }


# docker build -t news .

# docker run --rm -it -e METHOD=rewrite_translate news:latest

# docker run --rm -it -e METHOD=get_news news:latest

