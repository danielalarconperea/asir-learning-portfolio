date
cat
echo
tr
rm
history
less
grep
ls
sed
cut
uname
tee
xargs
touch

***

## `grep` (Global Regular Expression Print)

**Propósito:** 🔍 Busca patrones de texto dentro de ficheros o en la entrada estándar (STDIN).

**Opciones Útiles:**

* **`-i` (ignore-case):** Ignora mayúsculas y minúsculas al buscar.
    * *Ejemplo:* `grep -i "error" /var/log/syslog` (Buscará "error", "Error", "ERROR", etc.)
* **`-v` (invert-match):** Muestra todas las líneas que *no* coinciden con el patrón.
    * *Ejemplo:* `cat fichero.txt | grep -v "^#"` (Muestra el fichero sin las líneas que empiezan por `#` (comentarios)).
* **`-n` (line-number):** Muestra el número de línea donde se encontró la coincidencia.
    * *Ejemplo:* `grep -n "main" programa.c`
* **`-c` (count):** En lugar de mostrar las líneas, muestra un recuento de cuántas líneas coinciden.
    * *Ejemplo:* `grep -c "warning" /var/log/messages`
* **`-r` o `-R` (recursive):** Busca recursivamente en todos los ficheros de un directorio.
    * *Ejemplo:* `grep -r "mi_funcion" /proyecto/src/` (Busca el texto en todos los ficheros de la carpeta `src`).
* **`-l` (files-with-matches):** Muestra solo los *nombres* de los ficheros que contienen el patrón, no las líneas.
    * *Ejemplo:* `grep -l "TODO" *` (Te dice qué ficheros tienen una tarea "TODO").
* **`-w` (word-regexp):** Fuerza al patrón a coincidir solo con palabras completas.
    * *Ejemplo:* `grep -w "error"` (Coincidirá con "error" pero no con "terrores").
* **`-E` (extended-regexp):** Utiliza Expresiones Regulares Extendidas (ERE). Permite usar caracteres como `+` (uno o más), `?` (cero o uno) y `|` (OR lógico). Es el equivalente a `egrep`.
    * *Ejemplo:* `grep -E "error|warning" log.txt` (Busca líneas que contengan "error" O "warning").
* **`-P` (perl-regexp):** Utiliza Expresiones Regulares Compatibles con Perl (PCRE). Es el motor de regex más potente, permitiendo cosas como `\d` (dígitos) o búsquedas *lookaround*.
    * *Ejemplo:* `grep -P "\d{3}-\d{2}-\d{4}" contactos.txt` (Busca algo que parezca un número de SSN).

***

## `ls` (List)

**Propósito:** 📁 Lista el contenido de un directorio.

**Opciones Útiles:**

* **`-l` (long):** Muestra el listado en formato largo (permisos, propietario, grupo, tamaño, fecha, nombre).
    * *Ejemplo:* `ls -l`
* **`-a` (all):** Muestra *todos* los ficheros, incluidos los ocultos (los que empiezan por `.`).
    * *Ejemplo:* `ls -a` (Verás `.bashrc`, `.profile`, etc.)
* **`-h` (human-readable):** Usado *junto* con `-l`, muestra los tamaños en formato legible (p.ej., `4.0K`, `1.2M`, `2G`).
    * *Ejemplo:* `ls -lh`
* **`-t` (time):** Ordena los ficheros por fecha de modificación (los más nuevos primero).
    * *Ejemplo:* `ls -lt`
* **`-r` (reverse):** Invierte el orden. Muy común usarlo con `-t` para ver los más antiguos primero.
    * *Ejemplo:* `ls -ltr` (Formato largo, ordenado por tiempo, invertido. Muy útil para ver lo último que cambió al final de la lista).
* **`-R` (recursive):** Lista el contenido de los subdirectorios de forma recursiva.
    * *Ejemplo:* `ls -R /proyecto`
* **`-d` (directory):** Muestra información sobre el directorio en sí, no sobre su contenido.
    * *Ejemplo:* `ls -ld /var/log` (Muestra los permisos de la *carpeta* `/var/log`).

***

## `sed` (Stream Editor)

**Propósito:** ✍️ Edita texto "en flujo". Potente para buscar y reemplazar.

**Opciones Útiles:**

* **`-i` (in-place):** Edita el fichero "in-situ" (modifica el fichero original). ⚠️ **¡Peligroso!**
    * *Ejemplo:* `sed -i 's/antiguo/nuevo/g' fichero.txt` (Reemplaza "antiguo" por "nuevo" dentro de `fichero.txt`).
    * **Pro-Tip:** Usa `-i.bak` para crear una copia de seguridad (`fichero.txt.bak`) antes de editar. `sed -i.bak 's/foo/bar/g' file`.
* **`-n` (quiet):** Suprime la salida estándar. `sed` normalmente imprime cada línea. Con `-n`, solo imprime lo que le pidas explícitamente con el comando `p` (print).
    * *Ejemplo:* `sed -n '/patron/p' fichero.txt` (Funciona de forma similar a `grep "patron" fichero.txt`).
* **`-e` (expression):** Permite encadenar múltiples comandos `sed`.
    * *Ejemplo:* `sed -e 's/a/A/g' -e 's/b/B/g' fichero.txt` (Reemplaza 'a' y 'b').
* **`-r` o `-E` (extended-regexp):** Permite usar expresiones regulares extendidas (igual que `grep -E`).
    * *Ejemplo:* `sed -E 's/(gato|perro)/animal/g' texto.txt`

***

## `cut`

**Propósito:** ✂️ Extrae "columnas" de texto.

**Opciones Útiles:**

* **`-d` (delimiter):** Especifica el carácter que separa las columnas (el delimitador).
    * *Ejemplo:* `cut -d":" -f1 /etc/passwd` (Usa `:` como delimitador para extraer el primer campo (nombres de usuario)).
* **`-f` (fields):** Especifica qué campos (columnas) quieres extraer.
    * *Ejemplo:* `cut -d":" -f1,6 /etc/passwd` (Extrae el campo 1 y el 6 (usuario y home dir)).
    * *Rangos:* `cut -f1-3` (campos 1, 2 y 3), `cut -f3-` (del campo 3 hasta el final).
* **`-c` (characters):** Corta por posición de carácter en lugar de por campos.
    * *Ejemplo:* `ls -l | cut -c1-10` (Extrae los 10 primeros caracteres de cada línea, que son los permisos).
* **`--complement`:** Invierte la selección; extrae todo *excepto* lo que has pedido.
    * *Ejemplo:* `cut -d"," -f1 --complement datos.csv` (Muestra todas las columnas menos la primera).

***

## `xargs`

**Propósito:** 👷 Construye y ejecuta comandos a partir de la entrada estándar (STDIN). Es el "pegamento" entre comandos.

**Opciones Útiles:**

* **`-n1` (max-args):** Ejecuta el comando por separado para *cada* ítem de la entrada (máximo 1 argumento a la vez).
    * *Ejemplo:* `cat lista.txt | xargs -n1 touch` (Si `lista.txt` contiene "a", "b", "c", ejecuta `touch a`, luego `touch b`, luego `touch c`).
* **`-I {}` (replace-string):** Trata cada línea de entrada como un ítem completo y lo sustituye donde pongas `{}` (o el string que elijas).
    * *Ejemplo:* `find . -name "*.log" | xargs -I {} mv {} /backup/` (Por cada fichero `.log` encontrado, ejecuta `mv fichero.log /backup/`).
* **`-0` (null-delimiter):** Lee la entrada separada por caracteres nulos, no por espacios/saltos de línea. Es la forma segura de trabajar con ficheros que tienen espacios en el nombre. Se usa casi siempre con `find ... -print0`.
    * *Ejemplo:* `find . -name "*.txt" -print0 | xargs -0 rm` (Borra de forma segura todos los `.txt`, aunque se llamen "mi fichero con espacios.txt").

***

## `rm` (Remove)

**Propósito:** 🗑️ Borra ficheros y directorios.

**Opciones Útiles:**

* **`-i` (interactive):** Pregunta antes de cada borrado. Es un salvavidas.
    * *Ejemplo:* `rm -i *.txt`
* **`-r` o `-R` (recursive):** Borra directorios y todo su contenido de forma recursiva.
    * *Ejemplo:* `rm -r mi_carpeta`
* **`-f` (force):** Fuerza el borrado. Ignora ficheros que no existen y *nunca* pregunta. ⚠️ **¡EL MÁS PELIGROSO!** Combinar `rm -rf /` es el error más famoso de Linux.
    * *Ejemplo:* `rm -f fichero_que_no_existe` (No dará error).
* **`-v` (verbose):** Muestra lo que está borrando.
    * *Ejemplo:* `rm -v *.tmp` (Dirá "removed 'a.tmp'", "removed 'b.tmp'").

***

## `date`

**Propósito:** 🗓️ Muestra o establece la fecha y hora.

**Opciones Útiles:**

* **`+FORMATO`:** Muestra la fecha en un formato personalizado.
    * *Ejemplo:* `date +"%Y-%m-%d_%H-%M-%S"` (Genera `2025-10-19_19-30-00`. Muy útil para crear nombres de fichero únicos para backups).
    * *Ejemplo:* `echo "Log del día: $(date +"%A, %d de %B")"`
* **`+%s` (seconds):** Muestra la fecha como *timestamp* de Unix (segundos desde el 1 de enero de 1970).
    * *Ejemplo:* `date +%s` (Genera `1760875800`).

***

## `cat` (Concatenate)

**Propósito:** 🐈 Muestra, une o crea ficheros.

**Opciones Útiles:**

* **`-n` (number):** Numera todas las líneas de salida.
    * *Ejemplo:* `cat -n fichero.txt`
* **`-b` (number-nonblank):** Numera solo las líneas que no están vacías.
    * *Ejemplo:* `cat -b script.sh`
* **`-s` (squeeze-blank):** Comprime múltiples líneas en blanco consecutivas en una sola.
    * *Ejemplo:* `cat -s fichero_con_espacios.txt`

***

## `echo`

**Propósito:** 🗣️ Muestra un texto en la salida estándar.

**Opciones Útiles:**

* **`-n` (no-newline):** No añade un salto de línea al final del texto.
    * *Ejemplo:* `echo -n "Escribe tu nombre: " ; read nombre` (El cursor se quedará en la misma línea).
* **`-e` (enable-escapes):** Habilita la interpretación de secuencias de escape (como `\n` para salto de línea o `\t` para tabulación).
    * *Ejemplo:* `echo -e "Línea 1\nLínea 2\t¡Tabulada!"`

***

## `tr` (Translate)

**Propósito:** 🔄 Traduce o borra caracteres leídos de STDIN.

**Opciones Útiles:**

* **`-d` (delete):** Borra todos los caracteres especificados.
    * *Ejemplo:* `cat fichero.txt | tr -d " "` (Borra todos los espacios).
* **`-s` (squeeze-repeats):** Comprime caracteres repetidos en uno solo.
    * *Ejemplo:* `echo "Hoooolaaaaa" | tr -s "oa"` (Produce "Hola").
    * *Uso común:* `cat texto.txt | tr -s " "` (Reemplaza múltiples espacios por uno solo).

***

## `less`

**Propósito:** 📄 Paginador interactivo (permite moverse por un texto largo). No son *flags* sino comandos *dentro* de `less`.

**Opciones de Inicio Útiles:**

* **`-N` (line-numbers):** Muestra números de línea.
* **`-i` (ignore-case):** Ignora mayúsculas/minúsculas al buscar.
* **`+G`:** Empieza la vista al final del fichero (útil para logs).

**Comandos Interactivos:**

* `/patrón`: Busca "patrón" hacia adelante.
* `?patrón`: Busca "patrón" hacia atrás.
* `n`: Repite la última búsqueda (siguiente coincidencia).
* `N`: Repite la última búsqueda (anterior coincidencia).
* `g`: Va al inicio del fichero.
* `G`: Va al final del fichero.
* `q`: Sale (quit).

***

## `history`

**Propósito:** 📜 Muestra el historial de comandos (es un *builtin* de la shell).

**Opciones Útiles:**

* La "opción" más útil de `history` no es un flag, sino su uso con tuberías:
    * *Ejemplo:* `history | grep "ssh"` (Busca todos los comandos `ssh` que has usado).
    * *Ejemplo:* `history | grep "rm -rf"` (Para ver si has cometido algún error...).
* **`!N`:** Ejecuta el comando número N del historial. (Ej: `!123`).
* **`!!`:** Repite el último comando (a menudo como `sudo !!`).

***

## `uname` (Unix Name)

**Propósito:** ℹ️ Muestra información del sistema.

**Opciones Útiles:**

* **`-a` (all):** Muestra *toda* la información (nombre kernel, hostname, versión, máquina, etc.).
    * *Ejemplo:* `uname -a` (Produce: `Linux mi-pc 5.15.0-78-generic ... x86_64 ... GNU/Linux`).
* **`-r` (kernel-release):** Muestra solo la versión del kernel.
    * *Ejemplo:* `uname -r` (Produce: `5.15.0-78-generic`).
* **`-m` (machine):** Muestra la arquitectura del hardware.
    * *Ejemplo:* `uname -m` (Produce: `x86_64`).

***

## `tee`

**Propósito:** 分岐 Bifurca la salida: la envía a STDOUT (pantalla) *y* a un fichero.

**Opciones Útiles:**

* **`-a` (append):** Añade la salida al final del fichero, en lugar de sobrescribirlo.
    * *Ejemplo:* `ls -l | tee -a log.txt` (Ves el `ls` en pantalla y además se añade al final de `log.txt`).

***

## `touch`

**Propósito:** ⏱️ Actualiza la fecha de modificación/acceso de un fichero. Si no existe, lo crea vacío.

**Opciones Útiles:**

* **`-c` (no-create):** No crea el fichero si no existe (solo actualiza la fecha si ya existe).
    * *Ejemplo:* `touch -c mi_fichero`
* **`-r FILE` (reference):** Usa la fecha y hora de *otro* fichero para actualizar el fichero objetivo.
    * *Ejemplo:* `touch -r fichero_viejo.txt fichero_nuevo.txt` (Pone la fecha del viejo al nuevo).
* **`-t STAMP` (timestamp):** Permite especificar una fecha y hora exactas (`[[CC]YY]MMDDhhmm[.ss]`).
    * *Ejemplo:* `touch -t 202412312359 fichero_fin_de_año.txt` (Establece la fecha a 31-Dic-2024, 23:59).


***

## `head`

**Propósito:** ⬆️ Muestra las **primeras** líneas de un fichero.

**Opciones Útiles:**

* **`-n <num>` (o `-<num>`):** Especifica el número de líneas a mostrar. Por defecto, son 10.
    * *Ejemplo:* `head -n 5 /var/log/syslog` (Muestra las 5 primeras líneas del syslog).
    * *Ejemplo:* `head -20 fichero.txt` (Muestra las 20 primeras líneas).
* **`-n -<num>`:** Muestra todo el fichero **excepto** las últimas `N` líneas.
    * *Ejemplo:* `head -n -50 log.txt` (Muestra todo el log menos las 50 líneas del final).
* **`-c <bytes>`:** Muestra los primeros `N` **bytes** del fichero, en lugar de líneas.
    * *Ejemplo:* `head -c 1024 /dev/sda` (Lee el primer Kilobyte del disco duro).

***

## `tail`

**Propósito:** ⬇️ Muestra las **últimas** líneas de un fichero. Esencial para monitorizar logs.

**Opciones Útiles:**

* **`-n <num>` (o `-<num>`):** Muestra las últimas `N` líneas. Por defecto, son 10.
    * *Ejemplo:* `tail -n 50 /var/log/syslog` (Muestra las 50 últimas líneas del syslog).
* **`-n +<num>`:** Muestra el fichero **a partir** de la línea `N` hasta el final.
    * *Ejemplo:* `tail -n +101 fichero.txt` (Muestra de la línea 101 en adelante, omitiendo las 100 primeras).
* **`-f` (follow):** 📡 **La opción más importante.** Se "engancha" al fichero y muestra las nuevas líneas que se añaden en tiempo real. Se detiene con `Ctrl+C`.
    * *Ejemplo:* `tail -f /var/log/apache2/access.log` (Monitoriza en vivo quién accede a tu servidor web).

***

## `sort`

**Propósito:** 📊 Ordena las líneas de un fichero o de una entrada (tubería).

**Opciones Útiles:**

* **`-r` (reverse):** Invierte el orden (descendente, Z-A).
    * *Ejemplo:* `ls | sort -r` (Ordena los ficheros en orden alfabético inverso).
* **`-n` (numeric):** Ordena numéricamente. Sin esto, "10" iría *antes* que "2" (porque "1" va antes que "2").
    * *Ejemplo:* `cat numeros.txt | sort -n` (Ordena 1, 2, 10, 20...).
* **`-t <char>` (separator):** Especifica el carácter delimitador de campos (columnas).
* **`-k <num>` (key):** Especifica la columna (`key`) por la que se debe ordenar. Se usa casi siempre con `-t`.
    * *Ejemplo:* `sort -t: -k3n /etc/passwd` (Ordena el fichero de usuarios (`-t:`) por la 3ª columna (`-k3`), numéricamente (`-n`)).
* **`-u` (unique):** Muestra solo una copia de las líneas que son idénticas.
* **`-h` (human-numeric):** Ordena por tamaño legible (1G, 10M, 5K).
    * *Ejemplo:* `ls -lh | sort -k5h` (Ordena el listado `ls` por la 5ª columna (tamaño) de forma humana).

***

## `uniq`

**Propósito:** 🚫 Elimina o cuenta líneas duplicadas **consecutivas**.

⚠️ **Importante:** `uniq` solo funciona con líneas duplicadas que están una al lado de la otra. Por eso, casi siempre se usa después de `sort`: `sort fichero.txt | uniq`.

**Opciones Útiles:**

* **`-c` (count):** 🔢 **La opción más útil.** No elimina las líneas, sino que las agrupa y añade un contador al principio indicando cuántas veces apareció cada una.
    * *Ejemplo:* `cut -d' ' -f1 access.log | sort | uniq -c` (Cuenta cuántas peticiones ha hecho cada IP).
* **`-d` (duplicated):** Muestra *solo* las líneas que están duplicadas (una vez cada una).
* **`-u` (unique):** Muestra *solo* las líneas que **NO** están duplicadas (las que aparecen una sola vez).

***

## `wc` (Word Count)

**Propósito:** 🔢 Cuenta líneas, palabras y caracteres de un fichero o entrada.

**Opciones Útiles:**

* **`-l` (lines):** 📄 Muestra solo el número total de **líneas**.
    * *Ejemplo:* `cat fichero.txt | wc -l` (Te dice cuántas líneas tiene el fichero).
    * *Ejemplo:* `ls -l | wc -l` (Te dice cuántos ficheros/directorios hay).
* **`-w` (words):** ✍️ Muestra solo el número total de **palabras**.
* **`-m` (characters):** Muestra solo el número total de **caracteres**.
* **`-c` (bytes):** Muestra solo el número total de **bytes**.
* **`-L` (max-line-length):** Muestra la longitud (en caracteres) de la **línea más larga** del fichero.

***

## `split`

**Propósito:** 🔪 Parte un fichero muy grande en varios trozos más pequeños.

**Opciones Útiles:**

* **`-l <num>` (lines):** Parte el fichero cada `N` líneas.
    * *Ejemplo:* `split -l 1000 fichero_grande.csv parte_` (Crea `parte_aa`, `parte_ab`... cada uno con 1000 líneas).
* **`-b <size>` (bytes):** 💾 Parte el fichero en trozos de un tamaño específico. Acepta sufijos como `K` (Kilobytes), `M` (Megabytes), `G` (Gigabytes).
    * *Ejemplo:* `split -b 500M video.iso video_part_` (Parte `video.iso` en trozos de 500MB).
* **`-d` (numeric-suffix):** Usa sufijos numéricos (ej: `parte_00`, `parte_01`) en lugar de alfabéticos (`parte_aa`).
* **Para unir los ficheros:** `cat parte_* > fichero_grande.csv`

***

## `paste`

**Propósito:** 🖇️ Une (pega) el contenido de varios ficheros "columna a columna", es decir, horizontalmente.

**Opciones Útiles:**

* **`-d <delimiters>`:** Especifica el carácter delimitador que usará para unir las columnas (por defecto es un tabulador).
    * *Ejemplo:* `paste -d',' nombres.txt apellidos.txt` (Une `nombres` y `apellidos` en un CSV: `nombre,apellido`).
* **`-s` (serial):** Funciona con *un solo* fichero. Toma todas las líneas y las une en una sola línea, separadas por el delimitador (tabulador por defecto).
    * *Ejemplo:* `ls | paste -s -d':'` (Pone todos tus ficheros en una línea separados por `:`).

***

## `join`

**Propósito:** 🔗 Une dos ficheros basándose en un **campo común** (como un JOIN de SQL).

⚠️ **Importante:** Para que `join` funcione correctamente, ambos ficheros *deben estar ya ordenados* por el campo que vas a usar para unirlos.

**Opciones Útiles:**

* **`-t <char>`:** Especifica el delimitador de campos (columnas) de los ficheros.
* **`-1 <num>`:** Especifica qué campo (columna) usar del **primer** fichero para la unión.
* **`-2 <num>`:** Especifica qué campo (columna) usar del **segundo** fichero para la unión.
    * *Ejemplo:* `join -t',' -1 2 -2 1 fichero1.csv fichero2.csv` (Une los ficheros usando la columna 2 del fichero1 y la columna 1 del fichero2, con comas como delimitador).

***

## `nl` (Number Lines)

**Propósito:** #️⃣ Añade números de línea a un fichero. Es más configurable que `cat -n`.

**Opciones Útiles:**

* **`-ba`:** Numera **todas** las líneas (All), incluyendo las líneas vacías.
* **`-bt`:** Numera solo las líneas con texto (Body, es el comportamiento por defecto).
* **`-w <num>`:** Especifica el ancho para los números de línea (ej: `0001` en vez de `1`).
    * *Ejemplo:* `nl -ba -w4 mi_script.sh` (Numera todas las líneas de `mi_script.sh` usando 4 dígitos).

***

## Formateo de Texto (fmt, expand, unexpand)

* **`fmt`:** Reajusta los párrafos de un texto a un ancho de línea específico.
    * *Ejemplo:* `fmt -w 80 quijote.txt` (Formatea el texto para que ninguna línea pase de 80 caracteres).
* **`expand`:** Convierte los caracteres de **tabulación** en el número correspondiente de **espacios**.
    * *Ejemplo:* `expand fichero_con_tabs.py > fichero_con_espacios.py`
* **`unexpand`:** Hace lo contrario: convierte **espacios** en **tabulaciones** (donde sea posible).
    * *Ejemplo:* `unexpand -t4 fichero_con_espacios.py > fichero_con_tabs.py`