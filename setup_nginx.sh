#!/bin/sh

curl -LO http://nginx.org/download/nginx-1.3.4.tar.gz
tar xf nginx-1.3.4.tar.gz 

git clone git://github.com/shairontoledo/ngx-upload-module.git

cd nginx-1.3.4

export NGX_PREFIX=/Users/ruahman/swipe-tech-apps/rpm-tornado/nginx

./configure --prefix=$NGX_PREFIX \
  --with-pcre \
  --with-cc-opt=-I/usr/local/include \
  --with-ld-opt=-L/usr/local/lib \
  --add-module=../nginx-upload-module  \
  --with-debug \
  --with-http_stub_status_module \
  --with-http_flv_module \
  --with-http_ssl_module \
  --with-http_dav_module \
  --with-http_gzip_static_module \
  --with-http_realip_module \
  --with-mail \
  --with-mail_ssl_module \
  --with-ipv6 