# Sleepy Cat Books

<p align="center">
  <img src="images/favicon.png" width="200" alt="Sleepy Cat Books Logo" />
</p>

## Requisitos

- Docker con Docker compose
- `.env`
- `frontend/.env.prod`

## Archivos .env

Formato de `.env`:

```conf
# Cors
# Todas las urls del back separadas por comas (,) como
# localhost (para correr local sin docker) o
# sleepy-cat-books-frontend (para correr con docker)
# con los puertos 4173 y 5173
BACKEND_CORS_ORIGINS=""

# Url del front
FRONTEND_HOST=""

# POSTGRES config
POSTGRES_SERVER= # Nombre del servidor de la base de datos
POSTGRES_PORT= # Puerto en que escuchará
POSTGRES_USER= # Usuario de la base de datos
POSTGRES_PASSWORD= # Contraseña del usuario de la base de datos
POSTGRES_DB= # Nombre de la base de datos

# Docker images config
DOCKER_IMAGE_BACKEND= # Nombre de la imagen del backend
DOCKER_IMAGE_FRONTEND= # Nombre de la imagen del frontend
```

Formato de `.env.prod`:

```conf
PUBLIC_BACKEND_URL= # Url del servicio en docker con el puerto
```

## Correr app

Es posible levantar la aplicación ejecutando:

```sh
docker compose up --build
```

Esto levantará todos los servicios necesarios desde la base de datos hasta el front.

Una vez levantado se puede acceder a la plataforma en la url: `localhost:4173/`

## Desarrollo

### Backend

#### Desarrollar

Para obtener autocompletado y documentación es necesario instalar un entorno virtual de python, se recomienda el uso de [uv](https://github.com/astral-sh/uv).

Con esta herramienta instalada, hay que correr:

```sh
uv sync
```

De modo que instale todos los paquetes necesarios.

Para iniciar el entorno virtual en la consola ejecutar:

```sh
source /path/to/backend/.venv/bin/activate
```

#### Correr con docker

Es posible levantar sólo el back ejecutando:

```sh
docker compose up sleepy-cat-books-backend --build
```

Y conectarse a `localhost:8080/docs` para obtener una página con la API disponible.

#### Scripts

En la carpeta `backend/scripts` se encuentran scripts útiles:

- `add_revision.sh` para hacer modificaciones a la base de datos en base a los cambios en los modelos (en `app/models`).
- `enter_db.sh` con la aplicación corriendo es posible ingresar a la base de datos directamente a una consola de postgresql.
- `prestart.sh` este script se usa para inicializar la basee de datos automáticamente al levantar con docker compose.
- `reset_db.sh` si se necesita reiniciar la base de datos.
- `tests-start.sh` para correr los tests del back.

### Frontend

La aplicación esta desarrollada en Svelte usando SvelteKit.

### Correr la aplicación

Para instalar las dependencias

```bash
npm i
```

Para correr la aplicación en modo desarrollo

```bash
npm run dev -- --open
```

<small>`El -- --open` es para abrir en una nueva pestaña </small>

Para buildear la aplicación

```bash
npm run build
```

Para correr preview de la aplicación en modo producción

```bash
npm run preview
```
