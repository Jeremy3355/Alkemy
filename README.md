# Alkemy Challenge

## Descripcion
Alkemy callenge analisis de datos: el proyecto consiste en la obtencion de informacion, procesamiento y carga de la misma a un servidor postgresql

## Requisistos previos
Previo a la ejecucion del archivo `.py` debemos crear una un enotorno virtual de python con la libreria `venv`, cual se encuentra preinstalada en python, e instalar `postgresql`.

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

### Instalacion de postgresql
Como base de datos vamos a estar usando postgresql. Para su descarga vamos a ir a la sigeunte pagina https://www.postgresql.org/download/

* Al entrar al link nos encontraremos con la siguente pagina donde seleccionaremos el sistema operativo que tengamos.
<img src=imagenes\pg_descarga_1.png>

* Luego de seleccionar el sistema operativo, haremos clik en `Download the installer`.
<img src=imagenes\pg_descarga_2.png>

* Elegimos la veersion que mejor se ajuste a nuestro sistema. A modo de recomendacion, lo mejor es no usar la ultima version.
<img src=imagenes\pg_descarga_3.png>

* Usando el instalador procedemos con la instalacion del programa. Durante el proceso, nos pedira crear una contraseña por seguridad de la base de datos.

### Instalacion de librerias
El proyecto utiliza las sigeunte librerias:
* `sqlalchemy`
* `sqlalchemy_utils`
* `psycopg2`
* `pandas`
* `python-decouple`
* `requests`
* `os`
* `glob`
* `sys`
* `logging`

De las cuales `requests`, `os`, `glob`, `sys` y `logging` son nativas de python.

Para proceder con la insatalacion de las librerias, antes iniciaremos el entorno virtual previamente creado de la siguente forma:
* En el cmd buscaremos la carpeta donde previmente creamos el entorno virtual haceindo uso del comando `cd`.
* Una vez encontrada la carpeta, entraremos en ella y a su vez en la carpeta `Script`.
* Dentro de `Script` ejecutaremos el archivo `activar.bat`. De la misma manera que para ver los ficheros dentro de un directorio, podemos usarlo para navegar entre los archivos que se encuentran en el.
Ej:
```
C:\Usuarios\Usuario\Escritorio\nombre_del_entorno\Script\>activar.bat
```
De esta manera se nos ejecutara el cmd con el entorno virtual del python. Nos aparecera esto:
```
(nombre_del_entorno) C:\Usuarios\Usuario\Escritorio\nombre_del_entorno\Script\>
```
Una vez iniciado, instalaremos las librerias con el siguente comando:
```
pip install `nombre de la libreria`
```
Debemos repetir este comando para cada libreria que no sea nativa de python.

Para desactivar el entorno virtual simplemente debemos ir al mismo directorio en donde se enceuntra `activar.bat` y ejecutamos `desactivar.bat`.

## Setup del proyecto
Descargaremos le archivo `creacion_de_tablas.sql` y la carpeta `src` y los guardaremos en una nueva carpeta (el nombre es indiferente) dentro del entorno virtual para tener una mejor organizacion.

### Configuracion de informacion sensibles
La informacion sensible, como las claves de conexion a la base de datos, seran guardadas en un archivo `.env`. Tambien se gurdaran variables de configuracion para facilitar el deploy.

Dentro de la carpeta donde se encuentra `creacion_de_tablas.sql` y `src` crearemos un archivo `.env`. 

Dentro declararemos las siguenetes varaibles (los nombres deben ser los que se especifican en el README debido que sino el programa no hara una correcrta lectura de las mismas):
* `pgusuario`: usuario de postgresql
* `pgcontrasenia`: contraseña de postgresql
* `pghost`: host donde se esta ejecutando del servidor, en este caso seria `localhost`
* `pgpuerto`: puerto donde se este ejecutando el servidor, por defecto suele ser `5432`
* `pgdb`: nombre de la base de datos a utilzar. El mismo pude ser creado en postgresql o en el caso de no hacerlo, el programa `src.py` lo creara con el nombre definido en este campo.
* `url_museos`: URL del dataset de los museos.

  https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv
* `url_cines`: URL del dataset de los cines.

  https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv
* `url_bibliotecas`: URL del dataset de las bibliotecas.

  https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv
* `pathData`: ruta donde se encuentra guardado el proyecto, especificamente la carpeta creada en la seccion de `Setup del proyecto`.

Ej: `Los ´*´ representan la informacion a completar`
```
pgusuario= *
pgcontrasenia= *
pghost= *
pgpuerto= *
pgdb= *
url_museos= *
url_cines= *
url_bibliotecas= *
pathData= *
```
Hay una varaible que no se registrara dentro del archivo `.env` debido a que es la ruta de configuracion para la libreria que se encarga de leer las variables del archivo `.env`. La misma se encuentra en la `linea 14` del archivo `src.py`. En el campo `search_path` hay que colocar la ruta donde se encuentra almacenado el archivo `.env`.
```
config = AutoConfig(search_path='*')
```
A modo de recomendacion, es bueno colocar en los paths una barra extra para que no haya errores al ejecutar el programa.

### Cracion de base de datos
Este paso no es estrictamente necesario hacero, debido a que el propio programa en el caso de no encontrar una bases de datos con el nombre especificado, se encargara de crearla previamente a seguir ejecuando el resto del programa.

* Ejecutamos pgAdmin 4
<img src=imagnes\pgadmin_1.png>

* Ingresamos la conrtaseña
<img src=imagenes\pgadmin_2.png>

* Desplegmaos el menu de `Servers`
<img src=imagenes\pgadmin_3.png>

* Desplegamos el menu de `PostgreSQL 13`
<img src=imagenes\pgadmin_4.png>

* Nos pedira ingresar la contraseña
* Damos clik drecho sobre `Database` -> `Create` -> `Database`
<img src=imagenes\pgadmin_5.png>

* En el campo `Database` colocamos el nombre
<img src=imagenes\pgadmin_6.png>

### Ejecucion del programa
* Como primer paso debemos encender el entorno virtual, como previamente se indico.
* Una vez dentro navegamos por los ficheros y abrimos la carpeta donde se encuentran los archivos que corespondientes al proyecto.
* Entramos en la carpeta `src` y ejecutamos `src.py`

Una vez finalizada la ejecucion del programa, veremos que tenemos nuevos ficheros creados en la carpeta del proyecto. Uno de ellos lleva el nombre `logs`, donde se encuentra el archivo que nos indicara si hubieron errores al ejecutarse el programa, de no hableros, la correcta ejecucio del mismo.

### Verificaion de ingesta
Para tener certeza de que los datos fueron ingestados correctamente, vamos a revisar las tablas dentro de la base de datos. Para ello seguiremos los siguentes pasos:
* Seguiremos los mismo pasos que en la seccion `Creacion de base de datos` hasta el paso 5.
<img src=imagenes\verificacion_1.png>

* Una vez dentro de `Database`, entraremos a la base de datos con el nombre que hayamos decidio.
<img src=imagenes\verificacion_2.png>

* Dentro, desplegaremos la seccion `Schemas`, que abrira automaticamente la seccion `public`
<img src=imagenes\verificacion_3.png>

* Nos dirigiremos a `Tablas`
<img src=imagenes\verificacion_4.png>

* Seleccionaremos una de las tablas y daremos clik derecho. Se nos desplegaran una serie de opciones de las cuales seleccionaremos las sigeuntes `View/Edit Data` -> `All Rows`.
<img src=imagenes\verificacion_5.png>

* De este modo podremos ver todos los datos de la tabla seleccionada.
<img src=imagenes\verificacion_6.png>

### Aclaraciones
En el challenge se pide crear una tabla con la siguente informacion:
* Cantidad de registros totales por categoria
* Cantidad de registros totales por fuente
* Cantidad de registros por provincia y categoria

Para evitar problemas de normalizacion se creo una tabla por cada item.
