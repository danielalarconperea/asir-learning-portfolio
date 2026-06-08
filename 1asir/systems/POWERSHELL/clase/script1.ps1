$nombre=read-host("dime cual es su nombre de usuario") 
Write-Host "su nombre de Usuario es: $nombre"
$nombre.GetType()
[int]$edad=read-host("dime su edad") 
Write-Host "su nombre de Usuario es: $edad"
$edad.GetType()
$años = $edad +5
Write-Host $años
if($edad -gt 35){
write-host "eres un viejo"
}else{
Write-Host "disfruta la vida"
}
$fecha=(get-childitem .\downloads | Sort-Object LastAccessTime -Descending | Select-Object -first 1).lastwritetime
if ($fecha -gt (get-date).AddMinutes(-2)){
    write_host "el último fichero ha sido descargado hace 2 min"
}else{
Write-Host "El último archivo fue descargado el: $fecha"
}
Get-LocalUser | Format-Table name, description
