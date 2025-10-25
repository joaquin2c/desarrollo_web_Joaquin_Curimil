# Instrucciones

## Instrucciones de la Tarea 2

Esta tarea se hizo pensando en que debia tener incluido todos los elementos basicos para ser probado, por lo que aparte de tener la pagina web se incluye imagenes y los datasets, no teniendo claro si es que se guardaron los datos dentros del dataset, pero de igual forma se incluye un archivo que los crea desde 0.

Seguir estos pasos:

-Instalar librerias encontradas en requirements.txt

-En caso de no haber archivos en los datasets seguir las instrucciones de *init_database.sql*, donde se crean los usuarios usados en la tarea 1 y se guardan dentro del dataset tarea2.

-En caso de crear usuarios mediante los comandos mysql es necesario tener en cuenta lo siguiente: Al crear un usuario mediante la pagina web se debe adjuntar una foto de forma obligatoria, por lo que al usar solo los comandos de mysql se tiene que agregar al menos una imagen por cada usuario nuevo.

-Hay tres carpetas de imagenes dentro de upload, siendo las carpetas *mini* y *medium* las imagenes con el resize pedido de la tarea 1, mientras que en la carpeta *normal* se tienen imagenes normales que pueden ser usadas para crear un nuevo aviso desde la pagina web.

-Al crear un nuevo aviso desde la pagina web se agregara: una columna con la información pertinente en la tabla aviso_adopcion, las diferentes formas de contactos en la tabla de contactar_por, los path de las fotos en la tabla foto, y las imagenes incluidas dentro de las carpetas "mini" y "medium", teniendo en cada carpeta el tamaño requerido.

## Tarea 3

-En este caso el pre-procesos del conteo de fechas se hace desde el servidor, al ser un caso de prueba, pero presiento que en un caso real fallaria si hartos usuarios hacen la misma petición al mismo tiempo, por lo que tendría más sentido que el servidor cada cierto tiempo actualize un archivo json guardado en la carpeta de datos que contenga el conteo de avisos por día, por lo que el unico costo que realmente habría sería cargar el json y enviarlo al usuario.

-Al usar el verificador w3 con los html *Highcharts* es el unico que obtiene problemas, pero estos errores no se pueden corregir al ser generado directamente por estre framework, por lo que siguiendo la recomendación del auxiliar se dejarán estos errores. 
