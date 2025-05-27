# tpe-redes-grafana
Por Mateo Bartellini Huapalla, Bautista Ignacio Canevaro y Matías Wodtke

## Introducción
El objetivo de este trabajo es implementar una prueba de concepto para mostrar los posibles usos de Grafana en colaboración a Prometheus y Loki. Para eso, se utiliza una API Rest con acceso a una base de datos. De ambas se extraen métricas y estadísticas para ser mostradas en un dashboard.

## Ejecución
### Ejecución de la página web
```sh
cd website
docker compose up -d
```

Se puede ahora navegar a `localhost/docs` y probar la API.

### Ejecución del stack de monitoreo
```sh
cd monitoring
docker compose up -d
```