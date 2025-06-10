# tpe-redes-grafana
## Integrantes
- Mateo Bartellini Huapalla - Legajo 61438
- Bautista Ignacio Canevaro - Legajo 62179
- Matias Wodtke - 62098


## Introducción
El objetivo de este trabajo es implementar una prueba de concepto para mostrar los posibles usos de Grafana en colaboración a Prometheus y Loki. Para eso, se utiliza una API Rest con acceso a una base de datos y presentación frontend. De ambas se extraen métricas y estadísticas para ser mostradas en diferentes dashboards. La api/website y el monitoreo en Grafana son componentes independientes entre si, pero comunicados mediante direcciones y puertos.

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
Se puede ahora navegar a `localhost:2000` y monitorear el servidor.


## Variables de entorno
### Variables de entorno de la página web
```
POSTGRES_PASSWORD="password" #contraseña para la base de datos
```


### Variables de entorno del stack de monitoreo
```
GF_SMTP_PASSWORD="password" #contraseña del mail para las alertas
```
