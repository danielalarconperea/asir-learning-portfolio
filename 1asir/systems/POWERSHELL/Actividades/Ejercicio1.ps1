while ($true) {
    $nombre=Read-Host "dime el nombre de un fichero"
    if (-Not (Test-Path ".\powershell\$nombre")) {
        New-Item .\powershell\$nombre
        read-host "Escribe algo que desees guardar dentro del archivo" >> .\powershell\$nombre
        break
    }
    Get-ChildItem .\powershell\$nombre
    Get-Content .\powershell\$nombre
}