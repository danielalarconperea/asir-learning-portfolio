# Realizar un menú de opciones que nos permita hacer lo siguiente en cada caso:
# a. Buscar ficheros más grandes de un tamaño y ruta indicado por el 
# usuario
# b. Pedir una fecha y mostrar los logs del sistema de tipo Security de id 
# 4624 (inicios de sesión).
# c. Mostrar la Memoria del sistema (sin el resto de información)

do{ 
    Write-Host "Menu de opciones"
    Write-Host "------------------------------------------------"
    Write-Host "1__Buscar ficheros"
    Write-Host "2__Ver logs del sistema de tipo Security de id 4624"
    Write-Host "3__Ver Memoria del sistema"
    Write-Host "0__Salir"
    Write-Host "------------------------------------------------"
    $opcion=Read-Host "Dime una opción 0-3"
    switch ($opcion) {
        "1" {
            $nombre=Read-Host "ingrese el nombre de un directorío"
            $tamaño=Read-Host "ingrese el tamaño de archivos que quieres buscar como mínimo"
            $directorio=Get-ChildItem -file ..\$nombre | Where-Object Length -ge $tamaño | Sort-Object Length -Descending
            if(($directorio).count -ge 1){
                $directorio
            }else{
                Write-Host "error ese directorio no existe, escrive uno desde el escritorio"
            }
        }
        "2" {
            $fecha=Read-Host "Introduce una fecha (YYYY-MM-DD)"
            $fechaInicio = Get-Date $fecha
            Get-WinEvent -LogName "Security" | Where-Object {
                $_.Id -eq 4624 -and $_.TimeCreated -ge $fechaInicio
            } | Select-Object name, logname, starttime, TimeCreated, Id, Message
        }
        "3" {
            Get-ComputerInfo | Select-Object CsTotalPhysicalMemory, OsTotalVisibleMemorySize, OsFreePhysicalMemory
        }
        "0" {Write-Host "Hasta pronto"}
        Default {}
    }
}while($opcion -ne 0)