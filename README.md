# tpe-redes-grafana
## Integrantes
- Mateo Bartellini Huapalla - Legajo 61438
- Bautista Ignacio Canevaro - Legajo 62179
- Matias Wodtke - Legajo 62098


## Introducción
El objetivo de este trabajo es implementar una prueba de concepto para mostrar los posibles usos de Grafana en colaboración a Prometheus y Loki. Para eso, se utiliza una API Rest con acceso a una base de datos y presentación frontend. De ambas se extraen métricas y estadísticas para ser mostradas en diferentes dashboards. La api/website y el monitoreo en Grafana son componentes independientes entre si, pero comunicados mediante direcciones y puertos.


## Variables de entorno
### Variables de entorno de la página web
```
POSTGRES_PASSWORD="password" #contraseña para la base de datos
```

### Variables de entorno del stack de monitoreo
```
GF_SMTP_PASSWORD="password" #contraseña del mail para las alertas
```


## Compilación
### Compilación de la página web
```sh
cd website
docker compose build
```

### Compilación del stack de monitoreo
```sh
cd monitoring
docker compose build
```


## Ejecución
### Ejecución de la página web
```sh
cd website
docker compose up -d
```

Se puede ahora navegar a `localhost/docs` y `localhost:3000` para probar la API y el sitio web respectivamente.

### Ejecución del stack de monitoreo
```sh
cd monitoring
docker compose up -d
```
Se puede ahora navegar a `localhost:2000` y monitorear el servidor. Las credenciales por defecto son `admin:admin`.

## Funcionalidades
### Página web
Navegando a `localhost:3000` el usuario puede registrarse, iniciar sesión, buscar películas por título y escribir una reseña.

### Documentación de la API
El endpoint `localhost/docs` ofrece una interfaz siguiendo OpenAPI para poder probar la API.

### Monitoreo
En `localhost:2000` se puede acceder a la UI de Grafana. Las credenciales son `admin:admin`. Dentro del panel izquierdo, yendo a `Dashboard > Website > API Dashboard` se puede acceder al dashboard con los datos de la página web, como son el uptime de la página y los nodos que exportan a Prometheus, el uso de CPU de la máquina host, la cantidad y duración promedio de requests, la cantidad de conexiones TCP abiertas y algunos logs de interés. Yendo en cambio a `Dashboard > Database > DB Dashboard`, se pueden ver las métricas asociadas a la base de datos: el uptime, el uso de disco en función del tiempo y porcentual.

Otra funcionalidad a analizar es la de las alertas. Navegando en el panel izquierdo a `Alerting > Alert rules`, se podrá ver que hay definidas dos reglas, una para `Database` y una para `Website`. La primera es una regla para alertar en función al uso de disco de la base de datos (el valor límite está elegido para que se pueda testear corriendo el script `create_users.sh` con valor 1000). La segunda es una regla que alertará cuando la página web se encuentre caída por más de 30 segundos, lo cual se puede probar deteniendo el contenedor `tpe-redes-api`. Ambas reglas alertarán a los mails configurados en los archivos provistos al levantar el contenedor (véase los archivos de `monitoring/grafana_data/provisioning/alerting`). Diríjase a esos archivos para cambiar los destinatarios. En caso de querer testear el mailing, comuníquese con los dueños del repositorio para así obtener una App Password para la cuenta de GMail configurada por defecto (o configure la suya propia en `monitoring/docker-compose.yml`).

### Manejo de usuarios y equipos
Esta funcionalidad se eligió no automatizar su configuración. Las razones de esto es que (1) las maneras aconsejadas por la documentación de hacerlo implican el uso de herramientas que escapan al foco de esta prueba (Ansible, Terraform) y (2) se buscó mostrar el uso de la herramienta en vivo.

Para crear un usuario, navegue a `Administration > Users and Access > Users`. Ahí puede crear un nuevo usuario (invitándolo o asignándole contraseña). En la misma sección puede crear un equipo y asignar un usuario. Si ahora se dirige a la sección de dashboards, al seleccionar una carpeta verá en la parte superior derecha, la posibilidad de cambiar los permisos de la misma. Sacando el permiso de vista y agregando un nuevo permiso que dependa del equipo, podrá configurar con mayor granularidad el acceso a los recursos dentro de la carpeta elegida. Para poder verificarlo, cierre la sesión de administrador e ingrese a la cuenta creada anteriormente.