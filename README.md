# Alkemy Challenge

## Descripcion
Alkemy callenge analisis de datos: el proyecto consiste en la obtencion de informacion, procesamiento y carga a un servidor postgresql

## Proyecto
Previo a la ejecucion del archivo `.py` debemos crear una un enotorno virtual de python con la libreria `venv`, la caul se encuentra preinstalada en python, y crear una base de datos con `postgresql`.

### Generacion del entorno virtual
* Abrir el cmd
* Buscar la localizacion donde queremos crear el entorno virtual. Para ello navegaremos con el comando `cd`. Con el tab podemos ver los ficheros que se encuentran en ese directorio.
Ej:
```
C:\Usuarios\Usuario\>cd Escritorio
```
* Creamos el envorno virtual con el siguente comando:
```
C:\Usuarios\Usuario\Escritorio\>python -m venv nombre_del_entorno
```
En el campo `nombre_del_entorno` se colocal en nombre que va a tener la carpeta del entorno virtual

Por el momento no es necesario activar el enorno virtual.

### Creacion de la base de datos
Como base de datos vamos a estar usando postgresql. Para su descarga vamos a ir a la sigeunte pagina https://www.postgresql.org/download/

* Al entrar al link no encontraremos con la siguente pagina donde seleccionaremos el sistema operativo que tengamos.
<img src=imagenes\pg_descarga_1.png>

* Luego de seleccionar el sistema operativo, haremos clik en `Download the installer`.
<img src=imagenes\pg_descarga_2.png>

* Elegimos la veersion que mejor se ajuste a nuestro sistema. A modo de recomendacion, lo mejor es no usar la ultima version.
<img src=imagenes\pg_descarga_3.png>

* Usando el instalador procedemos con la instalacion del programa. Durant el proceso, nos pedira crear una contraseña por seuridad de la base de datos.

### Setup del proyecto

