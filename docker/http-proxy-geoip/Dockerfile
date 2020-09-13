FROM nginx:alpine

# nginx:alpine contains NGINX_VERSION environment variable, like so:
# ENV NGINX_VERSION 1.18.0

# TEMPLATE GENERAL: https://gist.github.com/hermanbanken/96f0ff298c162a522ddbba44cad31081
# CONFIG GENERAL: https://medium.com/faun/total-nginx-monitoring-with-application-performance-and-a-bit-more-using-8fc6d731051b
# MODULO GEOip2 : https://github.com/leev/ngx_http_geoip2_module


# Se necesita Git para el pull, autoconf,automake y libtool para compilar los modulos de GeoIP (libmaxminddb)
RUN apk update && \        
  apk add git && \
  apk add autoconf && \
  apk add automake && \
  apk add libtool && \
  apk add openrc

#Instalar Ping

# Download sources
# Tambien se debe descargar la BD de maxmind (http://dev.maxmind.com/geoip/geoip2/geolite2/)
RUN wget "https://nginx.org/download/nginx-1.19.0.tar.gz" -O nginx.tar.gz && \
  wget "https://github.com/leev/ngx_http_geoip2_module/tarball/master" -O ngx_http_geoip2_module.tar.gz && \
  git clone --recursive https://github.com/maxmind/libmaxminddb
#  wget "https://github.com/maxmind/libmaxminddb/releases/download/1.4.2/libmaxminddb-1.4.2.tar.gz"

# For latest build deps, see https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  libc-dev \
  make \
  openssl-dev \
  pcre-dev \
  zlib-dev \
  linux-headers \
  curl \
  gnupg \
  libxslt-dev \
  gd-dev \
  geoip-dev \
  logrotate

# Con wget
#RUN tar -xzvf "libmaxminddb-1.4.2.tar.gz" && \
#  cd /libmaxminddb-1.4.2 && \
#  ./configure && \
#  make && \
#  make install && \
#  ldconfig && \

# Con Git , el ./bootstrap se hace en el directorio del pull de libmax y despues se instala el tarball
# Esto es solo para la libreria C que necesita para "entender" a la BD
RUN cd /libmaxminddb && \
  ./bootstrap && \
  ./configure && \
  make && \
  make install && \
  ldconfig /etc/ld.so.conf.d


# Reuse same cli arguments as the nginx:alpine image used to build
RUN CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') && \
  CONFARGS=${CONFARGS/-Os -fomit-frame-pointer/-Os} && \
  mkdir -p /usr/src && \
	tar -zxC /usr/src -f nginx.tar.gz && \
  tar -xzvf "ngx_http_geoip2_module.tar.gz" && \
  GEOIPDIR="$(pwd)/leev-ngx_http_geoip2_module*" && \
  cd /usr/src/nginx-1.19.0 && \
  ./configure --with-compat $CONFARGS --add-dynamic-module=$GEOIPDIR && \
  make && \
  make install && \
  rm /etc/nginx/conf.d/default.conf

COPY /nginx.conf /etc/nginx/nginx.conf
COPY /default.conf /etc/nginx/conf.d/default.conf
COPY /GeoLite2-City.mmdb $GEOIPDIR
COPY /GeoLite2-Country.mmdb $GEOIPDIR
COPY /nginx /etc/logrotate.d/nginx
COPY /logrotate.conf /etc/logrotate.conf
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]
RUN rm /var/log/nginx/access.log && \
    touch /var/log/nginx/access.log && \
    rm /var/log/nginx/error.log && \
    touch /var/log/nginx/error.log && \
    rm /nginx.tar.gz && \
#    rm ngx_http_geoip_2_module.tar.gz && \
    rm -r leev-ngx_http_geoip2_module-1cabd8a/ && \
    rm -r /usr/src/ && \
    chmod 644 /etc/logrotate.conf /etc/logrotate.d/nginx
#    echo '*/3 * * * * sh >/var/log/nginx/access.log' > /etc/crontabs/root


# Realizar cleanup instalacion
