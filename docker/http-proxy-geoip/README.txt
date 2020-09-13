----------------------------------------DOCKERFILE---------------------------------------------

Imagen a utilizar

	FROM nginx:alpine

Se necesita Git para el pull, autoconf,automake y libtool para compilar los modulos de GeoIP (libmaxminddb)

	RUN apk update && \        
		apk add git && \
		apk add autoconf && \
		apk add automake && \
		apk add libtool && \
		apk add crond

Download sources

	RUN wget "https://nginx.org/download/nginx-1.19.0.tar.gz" -O nginx.tar.gz && \
		wget "https://github.com/leev/ngx_http_geoip2_module/tarball/master" -O ngx_http_geoip2_module.tar.gz && \
		git clone --recursive https://github.com/maxmind/libmaxminddb

Se instala librerias de libmaxmind

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
		geoip-dev



Se crean directorios, se extraen los tarball y se configura.

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


Se copian las config de nginx y las BD de GeoIP2

	COPY /shared/newcos-teams/sandbox-05/Dockerfiles/NginxGeolocalization/nginx.conf /etc/nginx/nginx.conf
	COPY /shared/newcos-teams/sandbox-05/Dockerfiles/NginxGeolocalization/default.conf /etc/nginx/conf.d/default.conf
	COPY /shared/newcos-teams/sandbox-05/Dockerfiles/NginxGeolocalization/GeoLite2-City.mmdb $GEOIPDIR
	COPY /shared/newcos-teams/sandbox-05/Dockerfiles/NginxGeolocalization/GeoLite2-Country.mmdb $GEOIPDIR

Se expone el puerto 80

	EXPOSE 80

Se borra el link de los logs, se limpia la imagen

	RUN rm /var/log/nginx/access.log && \
			rm /var/log/nginx/error.log && \
			rm /nginx.tar.gz && \
			rm -r leev-ngx_http_geoip2_module-1cabd8a/ && \
			rm -r /usr/src/ && \





----------------------------------------nginx.conf---------------------------------------------


Cargar los modulos en MAIN

	load_module modules/ngx_http_geoip2_module.so;
	load_module modules/ngx_stream_geoip2_module.so;



	http {

		# Variable para test
		map $host $my_variable {
		 default 190.210.91.137;
		}

		log_format  main  '$remote_addr [$time_local] $request '
			      '$status $body_bytes_sent '
			      '$http_user_agent '
			      '"$geoip2_data_city_name" "$geoip2_data_state_name" '
			      '"$geoip2_data_country_name" "$geoip2_data_country_iso_code" '
			      '"$geoip2_data_latitude" "$geoip2_data_longitude"';


Modulos GEOIP , source es para hacer override del campo que debe tomar,
por defecto es ip_addr, los default el latitud y longitud son para que en caso de no encontrarlos
al momento de visualizarlos en GeoIP, no se rompa el mapa.

		geoip2 /GeoLite2-City.mmdb {
		$geoip2_data_city_name source=$my_variable city names es;
	#        $geoip2_data_postal_code postal code;
		$geoip2_data_latitude  default=0  location latitude;
		$geoip2_data_longitude  default=0  location longitude;
		$geoip2_data_state_name source=$my_variable subdivisions 0 names es;
	#        $geoip2_data_state_code  subdivisions 0 iso_code;
	    }

	    geoip2 /GeoLite2-Country.mmdb {
	#        $geoip2_data_continent_code source=$my_variable  continent code;
		$geoip2_data_country_iso_code source=$my_variable country iso_code;
		$geoip2_data_country_name source=$my_variable country names es;
	    }

	}
	
	
	
----------------------------------------telegraf.conf---------------------------------------------


Se crea especifica la DB

	[[outputs.influxdb]]
	  urls = ["http://192.168.10.31:8086"]

	  database = "telegraf_geolocation"
	  database_tag = ""


Se parsea los logs con grok

[[inputs.logparser]]

   files = ["/var/log/access.log"]
   from_beginning = true

    [inputs.logparser.grok]
        patterns = ["%{CUSTOM_LOG}"]
        custom_patterns = '''
        CUSTOM_LOG %{HOSTNAME:Hostname:tag} \[%{HTTPDATE:Fecha}\] %{WORD:Metodo} / %{NOTSPACE:Metodo_info} %{INT:Status} %{INT:Bytes_sent} %{NOTSPACE:HTTP_User_Agent} %		{QS:Ciudad} %{QS:Estado} %{QS:Pais} %{QS:Codigo_pais:tag} "%{DATA:Latitud}" "%{DATA:Longitud}"
        '''

      	timezone = "Local"
      	unique_timestamp = "auto"


----------------------------------------docker-compose.yml---------------------------------------------

El compose se conforma de 2 servicios: telegraf y nginx. Ambos contenedores tienen el prefijo "newcos_".
El contenedor de nginx se buildea con el Dockerfile, el volumen es donde va a estar el access.log, que se
guardara en esta misma carpeta, para que telegraf pueda obtener los datos y enviarlo a la DB.
El contenedor de telegraf, tambien se le crean volumenes, que son para el sock de docker,
el archivo de configuracion, y el access.log que guarda nginx.
Ambos utilizan la red monitoring.




