Clear-Host

$nombre=read-host("dime cual es su nombre de usuario") 
$num=(Get-LocalUser -Name $nombre -ErrorAction SilentlyContinue).count

if ($num -eq 1){
    Write-Host("el usuario administrador existe")
}else{
    Write-Host("el usuario administrador no existe")
}

$nombr=read-host("dime el nombre de un fichero") 
if(Test-Path $nombr -PathType Leaf) {
    Get-Content $nombr
}else{
    Write-Host 'el nombre del archivo no existe'
}

$nomb=read-host("dime el nombre de un fichero o un archivo") 
if(Test-Path $nomb -PathType Leaf) {
    Get-content $nomb
}elseif(Test-Path $nomb -PathType Container){
    Get-ChildItem $nomb
}else{
    Write-Host 'el nombre del archivo no existe'
}

while ($valor -ne "0"){
    Write-Host "menu de opciones"
    Write-Host "----------------"
    Write-Host "1.- Mostrar fecha"
    Write-Host "2.- Saludar"
    Write-Host "3.- Listado"
    Write-Host "0.- Salir"
    $valor=Read-Host("dime una opción")
    switch ($valor) {
        "1" { Get-Date }
        "2" { Write-Host "hola" }
        "3" { Get-ChildItem }
        "0" { Write-Host "adiós" }
        Default { Write-Host "te has equivocado esa opción no existe" }
    }
} 

do{
    Write-Host "menu de opciones"
    Write-Host "----------------"
    Write-Host "1.- Mostrar fecha"
    Write-Host "2.- Saludar"
    Write-Host "3.- Listado"
    $valor=Read-Host("dime una opción")
    switch ($valor) {
        "1" { Get-Date }
        "2" { Write-Host "hola" }
        "3" { Get-ChildItem }
        "0" { Write-Host "adiós" }
        Default { Write-Host "te has equivocado esa opción no existe" }
    }
    $respuesta=Read-Host "¿quieres repetir? S/N"
} while ($respuesta -eq "S" -or $respuesta -eq "s")

do{
    $usuario=read-host "dime un nombre de usuario"
    $noexiste=(Get-LocalUser -Name $usuario -ErrorAction SilentlyContinue).count -eq 0
    if($noexiste){
        Write-Host "El usuario no es correcto"}
}while($noexiste)
Get-LocalUser -Name $usuario -ErrorAction SilentlyContinue | Select-Object lastlogon

do{
    do{
        $usuario=read-host "dime un nombre de usuario"
        $noexiste=(Get-LocalUser -Name $usuario -ErrorAction SilentlyContinue).count -eq 0
        if($noexiste){
            Write-Host "El usuario no es correcto"}
    }while($noexiste)
    Get-LocalUser -Name $usuario -ErrorAction SilentlyContinue | Select-Object lastlogon
    $respuesta=Read-Host "¿quieres repetir? S/N"
} while ($respuesta -eq "S" -or $respuesta -eq "s")