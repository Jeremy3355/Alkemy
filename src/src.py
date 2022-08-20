# Se importan todas las extenciones que van a ser utilizadas
import requests as r
import os
import glob
import pandas as pd
import sys
import logging
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from decouple import AutoConfig

# Configuracion decouple
config = AutoConfig(search_path='*')

# Se definen parametros basicos que se van a utilizar a lo largo de todo el codigo
sql_sentenicias = 'creacion_de_tablas.sql'
lista_url = [
    config('url_museos'),
    config('url_cines'),
    config('url_bibliotecas')
    ]

# Funciones #

# Test de conexion a la base de datos y status de los URLs
def test_conexiones():
    error = 0
    try:
        get_engine(
        config('pgusuario'),
        config('pgcontrasenia'),
        config('pghost'),
        config('pgpuerto'),
        config('pgdb')
        )
    except: 
        logging.error('Error de conexion a la base de datos')
        error = 1
    try:
        for url in lista_url:
            r.get(url).raise_for_status()
    except:
        logging.error('Error en la conexion con ' + url)
        error = 1
    if error == 1: sys.exit()
    """
    # Conexion con base de datos #
    try:
        genera un llamado a la base de datos
    except:
        caso de no logar la conexion, activa el flag de error y avisa a traves de un log lo ocurrido
        
    # Conexion con URLs #
    try:
        revisa que los URLs no den error 404, en el caso de dar error 404 sale del for
    except:
        al dar error 404 activa el flag de error y avisa a traves de un log que el URL fallo
    if error  == 1: 
        si se activo el flag de error, se frena la ejecucion del programa
    """
    
# Creacion de enlace con la base de datos
def get_engine(usuario, contraseña, host, puerto, db):
    url = f"postgresql://{usuario}:{contraseña}@{host}:{puerto}/{db}"
    if not database_exists(url):
        create_database(url)
        logging.info('Base de datos creada correctamente')
    engine = create_engine(url, pool_size=50, echo=False)
    return engine
    """
    url = genera el URL de conexion con la base de datos con la informacion de conexion que se le brinda
    
    if not database_exists(url):
        revisa si la base de datos ingresada no existre. En el caso de que sea verdadero, se creara e 
        informara a traves del log.
        
    engina = genera la conexion con la base de datos tomando el url como referencia
    
    return engine
    devuelve el engine
    """

# Creaion de ficheros a utilizar
def path_create():
    if not os.path.isdir(config('pathData') + "//datasets"):
        os.makedirs(config('pathData') + "//datasets")
    if not os.path.isdir(config('pathData') + "//logs"):
        os.makedirs(config('pathData') + "//logs")
    """
    if not os.path.isdir(direccion)
        revisa si la direccion no existe.
        os.makedirs(direccion)
        Crea la direccion si la sentencia if fue verdadera
    """

# Descarga los .csv de los URLs y los organiza en un sistema de carpetas anidados por año-mes
def get_csv(url):
    archivo = r.get(url)
    h = r.head(url, allow_redirects = True)
    header = h.headers
    content_type = header.get('content-type')
    file_name = url.split('/')[-1]
    fecha = date.today().strftime("%d-%m-%Y")
    pathMes = date.today().strftime("%Y-%B")
    if 'museos_datosabiertos' in file_name:
        cat = 'museos'
        nom = 'museos'
    elif 'cine' in file_name:
        cat = 'salasDeCine'
        nom = 'cines'
    elif 'biblioteca_popular' in file_name:
        cat = 'bibliotecasPopulares'
        nom = 'bibliotecas'
    else: return logging.error('Archivo no valido') 
    if not os.path.isdir(config('pathData') + f"//datasets//{cat}//{pathMes}"):
        os.makedirs(config('pathData') + f"//datasets//{cat}//{pathMes}")
    if 'text/csv' in content_type.lower():
        with open(config('pathData') + f'//datasets//{cat}//{pathMes}//{nom}-{fecha}.csv', 'wb') as dir:
            dir.write(archivo.content)
    else: 
        logging.error('El archivo no es un dataset')
        sys.exit()
    """
    if 'museos_datosabiertos' in file_name:
    elif 'cine' in file_name:
    elif 'biblioteca_popular' in file_name:
    revisa que a que categoria corresponde el archivo descargado.
    
    else: return 
        devuelve un log de error
       
    if not os.path.isdir(direccion):
        os.makedirs(direccion)
    genera el anidado de carpetas para gurdar ordenadamente los archivos
    
    if 'text/csv' in content_type.lower():
        with open(direccion_de_gurdado, 'wb') as dir:
            dir.write(archivo.content)
    revisa que el archivos sea del tipo text o csv y lo guarda en la direccion que se creo previamente con
    el nombre generado especificamente para ese archivo.
    
    else:
        en el caso de que sea falso, genera un log de error y frena la ejecucion del programa
    """

# Lee los .csv del disco local 
def leer_csv(cat):
    recent_file = sorted(glob.iglob(config('pathData') + f'//datasets//{cat}//*//*'),
                         key = os.path.getctime, reverse = True)
    df = pd.read_csv(recent_file[0])
    return df
    """
    recent_file = sorted(glob.iglob(direccion),
                         key = os.path.getctime, reverse = True)
    dentro de la direccion otorgada, genera una lista con los nombres de los archivos ordenados por fecha de carga ascendente
    
    df = pd.read_csv(recent_file[0])
    lee el csv mas reciente y lo guarda en una variable local
    
    retun df
    devuelve el csv
    """
    
# Crea las tablas a partir de queries guardadas en un .sql
def crear_tablas(archivo, engine):
    conexion = engine.raw_connection()
    cursor = conexion.cursor()
    try:
        with open(config('pathData') + '//' + archivo, 'r') as sentencias:
            query = sentencias.read()
            cursor.execute(query)
    except:
        logging.error('Error al intentar crear tablas')
        cursor.close()
        sys.exit()
    finally:
        conexion.commit()
        cursor.close()
    """
    try:
        with open(config('pathData') + '//' + archivo, 'r') as sentencias:
            query = sentencias.read()
            cursor.execute(query)
        abre el archivo donde se encuentran las queries de creacion de tablas y las ejecuta en el cursor previamente creado.
    except:
        en el caso de que falle, se genera un log con el error, se cierra el cursor y frena la ejecucion del programa
    finally:
        genera un commit a la base de datos y cierra la coenxion
    """
    
#  Ingesta los datos a la base de datos
def ingesta(df, tabla, engine):
    conexion = engine.raw_connection()
    cursor = conexion.cursor()
    try:
        df.to_sql(tabla , engine, if_exists = 'append', index = False)
    except:
        logging.error(f'Error al intar ingestar datos en tabla {tabla}')
        cursor.close()
    finally:
        conexion.commit()
        cursor.close()
        logging.info(f'Datos ingestados correctamente en tabla: {tabla}')
    """
     try:
        df.to_sql(tabla , engine, if_exists = 'append', index = False)
        toma el dataframe de pandas, lo convierte en sentencias sql y lo sube a la base de datos
        a traves del engine
    except:
        logging.error(f'Error al intar ingestar datos en tabla {tabla}')
        cursor.close()
        en el caso de haber un error, lo informa a traves del log y cierra el cursor
    finally:
        conexion.commit()
        cursor.close()
        logging.info(f'Datos ingestados correctamente en tabla: {tabla}')
        genera un commit en la base de datos, cierra el cursor e informa que la tabla se ingesto correctamente
    """
    
# Test ficheros #
path_create()

# Configuracion del logging
logging.basicConfig(filename = config('pathData') + '\\logs\\log.log',
                    level = logging.INFO,
                    format = '%(asctime)s - %(levelname)s: %(message)s')

# Testeo de conexiones #
test_conexiones()

# Recopilacion de datos #

for url in lista_url:
    get_csv(url)

# Procesaminto de datos #

# Lee los .csv del disco y los almacena en sus respectivas varibles
df_museos = leer_csv('museos')
df_cines = leer_csv('salasDeCine')
df_bibliotecas = leer_csv('bibliotecasPopulares')

# Tabla normalizada #

# Se unifica el nombre de las columnas a utilizar
df_museos.rename(columns = {
    'Cod_Loc':'cod_loc',
    'IdProvincia':'idprovincia',
    'IdDepartamento':'iddepartamento',
    'categoria':'categoria',
    'provincia':'provincia',
    'localidad':'localidad',
    'nombre':'nombre',
    'direccion':'direccion',
    'CP':'cp',
    'telefono':'telefono',
    'Mail':'mail',
    'Web':'web'},inplace = True)
df_cines.rename(columns = {
    'Cod_Loc':'cod_loc',
    'IdProvincia':'idprovincia',
    'IdDepartamento':'iddepartamento',
    'Categoría':'categoria',
    'Provincia':'provincia', 
    'Localidad':'localidad',
    'Nombre':'nombre',
    'Dirección':'direccion',
    'CP':'cp',
    'Teléfono':'telefono',
    'Mail':'mail',
    'Web':'web',
    'Fuente':'fuente'}, inplace = True)
df_bibliotecas.rename(columns = {
    'Cod_Loc':'cod_loc',
    'IdProvincia':'idprovincia',
    'IdDepartamento':'iddepartamento',
    'Categoría':'categoria',
    'Provincia':'provincia', 
    'Localidad':'localidad',
    'Nombre':'nombre',
    'Domicilio':'direccion',
    'CP':'cp',
    'Teléfono':'telefono',
    'Mail':'mail',
    'Web':'web',
    'Fuente':'fuente'}, inplace = True)

# Se crea el dataframe con la informacion normalizada
df_normalizado = pd.concat([df_museos[[
                                'cod_loc',
                                'idprovincia',
                                'iddepartamento',
                                'categoria',
                                'provincia',
                                'localidad',
                                'nombre',
                                'direccion',
                                'cp',
                                'telefono',
                                'mail',
                                'web']],
                            df_cines[[
                                'cod_loc',
                                'idprovincia',
                                'iddepartamento',
                                'categoria',
                                'provincia',
                                'localidad',
                                'nombre',
                                'direccion',
                                'cp',
                                'telefono',
                                'mail',
                                'web']], 
                            df_bibliotecas[[
                                'cod_loc',
                                'idprovincia',
                                'iddepartamento',
                                'categoria',
                                'provincia',
                                'localidad',
                                'nombre',
                                'direccion',
                                'cp',
                                'telefono',
                                'mail',
                                'web']]],
                           ignore_index = True)

# Tabla cantidad de registros por categoria #

# Creacion del dataframes auxiliares
df_a = df_bibliotecas.groupby('categoria').categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_b = df_cines.groupby('categoria').categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_c = df_museos.groupby('categoria').categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_a.reset_index(inplace = True)
df_b.reset_index(inplace = True)
df_c.reset_index(inplace = True)

# Creacion del dataframe solicitado
df_categorias = pd.concat([df_a[['categoria', 'cantidad_de_registros']],
                           df_b[['categoria', 'cantidad_de_registros']],
                           df_c[['categoria', 'cantidad_de_registros']]],
                          ignore_index = True)

# Tabla cantidad de registros por fuente #

# Creacion del dataframes auxiliares
df_a = df_bibliotecas.groupby('fuente').fuente.count().to_frame().rename(columns = {'fuente':'cantidad_de_registros'})
df_b = df_cines.groupby('fuente').fuente.count().to_frame().rename(columns = {'fuente':'cantidad_de_registros'})
df_c = df_museos.groupby('fuente').fuente.count().to_frame().rename(columns = {'fuente':'cantidad_de_registros'})
df_a.reset_index(inplace = True)
df_b.reset_index(inplace = True)
df_c.reset_index(inplace = True)

# Creacion del dataframe solicitado
df_fuentes = pd.concat([df_a[['fuente', 'cantidad_de_registros']],
                        df_b[['fuente', 'cantidad_de_registros']],
                        df_c[['fuente', 'cantidad_de_registros']]],
                       ignore_index = True)

# Tabla cantidad de registros por provincia y categoria #

# Creacion del dataframes auxiliares
df_a = df_bibliotecas.groupby(['provincia', 'categoria']).categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_b = df_cines.groupby(['provincia', 'categoria']).categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_c = df_museos.groupby(['provincia', 'categoria']).categoria.count().to_frame().rename(columns = {'categoria':'cantidad_de_registros'})
df_a.reset_index(inplace = True)
df_b.reset_index(inplace = True)
df_c.reset_index(inplace = True)

# Creacion del dataframe solicitado
df_prov_cat = pd.concat([df_a[['provincia', 'categoria', 'cantidad_de_registros']],
                         df_b[['provincia', 'categoria', 'cantidad_de_registros']], 
                         df_c[['provincia', 'categoria', 'cantidad_de_registros']]],
                        ignore_index = True )
df_prov_cat.sort_values('provincia', inplace = True)

# Tabla informacion cines #

# Creacion del dataframe con la informacion solicitada
df_info_cines = df_cines[['provincia', 'Pantallas','Butacas','espacio_INCAA']].groupby('provincia').sum()
df_cines_aux = df_cines[['provincia','espacio_INCAA']].groupby('provincia').count()
df_info_cines = df_info_cines.merge(df_cines_aux, left_on = 'provincia', right_on='provincia')
df_info_cines.reset_index(inplace = True)

# Se renombran las columnas para un mejor inegracion con la base de datos
df_info_cines.rename(columns = {
    'Pantallas':'pantallas',
    'Butacas':'butacas',
    'espacio_INCAA':'espacios_incaa'}, inplace = True)

# Creacion y actualizacion de la base de datos #

# Se genera el enlace con la base de datos
engine = get_engine(
        config('pgusuario'),
        config('pgcontrasenia'),
        config('pghost'),
        config('pgpuerto'),
        config('pgdb')
        )

# Crea las tablas
crear_tablas(sql_sentenicias, engine)

# Ingesta de datos
ingesta(df_normalizado, 'datos_argentina_espacios_publicos_normalizados', engine)
ingesta(df_categorias, 'registros_categorias', engine)
ingesta(df_fuentes, 'registros_fuente', engine)
ingesta(df_prov_cat, 'registros_prov_cat', engine)
ingesta(df_info_cines, 'informacion_cines_provincias', engine)
