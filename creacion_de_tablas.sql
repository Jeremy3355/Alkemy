-- Creacion de tablas --

-- Tabla general noramlizada --
DROP TABLE IF EXISTS datos_argentina_espacios_publicos_normalizados;
CREATE TABLE datos_argentina_espacios_publicos_normalizados(
    cod_loc int DEFAULT NULL,
    idprovincia int DEFAULT NULL,
    iddepartamento int DEFAULT NULL,
    categoria varchar DEFAULT NULL,
    provincia varchar DEFAULT NULL,
    localidad varchar DEFAULT NULL,
    nombre varchar DEFAULT NULL,
    direccion varchar DEFAULT NULL,
    cp varchar DEFAULT NULL,
    telefono varchar DEFAULT NULL,
    Mail varchar DEFAULT NULL,
    web varchar DEFAULT NULL,
    fechacarga date DEFAULT current_date
);

-- Tabla informacion de cines --
DROP TABLE IF EXISTS informacion_cines_provincias;
CREATE TABLE informacion_cines_provincias(
    provincia varchar DEFAULT NULL,
    pantallas int DEFAULT NULL,
    butacas int DEFAULT NULL,
    espacios_INCAA int DEFAULT NULL,
    fechaCarga date DEFAULT current_date
);

-- Tabla cantidad de registros por categoria --
DROP TABLE IF EXISTS registros_categorias;
CREATE TABLE registros_categorias (
    categoria varchar DEFAULT NULL,
    cantidad_de_registros int DEFAULT NULL,
    fechacarga date DEFAULT current_date
);

-- Tabla cantidad de registros por fuente
DROP TABLE IF EXISTS registros_fuente;
CREATE TABLE registros_fuente (
    fuente varchar DEFAULT NULL,
    cantidad_de_registros int DEFAULT NULL,
    fechacarga date DEFAULT current_date
);

-- Tabla cantidad de registros por provincia y categoria
DROP TABLE IF EXISTS registros_prov_cat;
CREATE TABLE registros_prov_cat (
    provincia varchar DEFAULT NULL,
    categoria varchar DEFAULT NULL,
    cantidad_de_registros int DEFAULT NULL,
    fechacarga date DEFAULT current_date
);