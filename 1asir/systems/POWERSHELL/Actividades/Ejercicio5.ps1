# Realiza un script que nos pida el nombre de un directorio y un número 
# correspondiente al tamaño de los ficheros que queremos buscar en él.
# a. Si el directorio no existe el programa debe sacar un mensaje de error.
# b. Si el directorio existe buscará dentro de él todos los ficheros cuyo
# tamaño sea mayor o igual que el indicado ordenados por tamaño de 
# archivo.
# c. En cualquiera de los dos casos, después debe preguntarnos si deseamos 
# volver a intentarlo y en caso afirmativo repetir la ejecución del script 
# desde el principio.
do{
    $nombre=Read-Host "ingrese el nombre de un directorío"
    $tamaño=Read-Host "ingrese el tamaño de archivos que quieres buscar como mínimo"
    $directorio=Get-ChildItem -file ..\$nombre | Where-Object Length -ge $tamaño | Sort-Object Length -Descending
    if(($directorio).count -ge 1){
        $directorio
    }else{
        Write-Host "error ese directorio no existe, escrive uno desde el escritorio"
    }
    $repetir=read-Host "¿Quieres repetirlo S/N?"   
}while($repetir -eq "S")
