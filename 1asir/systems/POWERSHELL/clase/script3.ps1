for($n=1;$n -le 5;$n++){
    mkdir "dir$n"
}

for($n=1;$n -le 5;$n++){
    Remove-Item "dir$n"
}

$collection = Get-LocalUser
foreach($elemento in $collection){
    if ($elemento.Enabled){
        Write-Host "El usuario $($elemento.Name) está habilitado"
    } else {
        $respuesta = Read-Host "¿Quieres habilitar el usuario $($elemento.Name)? (S/N)"
        if ($respuesta -eq "S" -or $respuesta -eq "s"){
            Enable-LocalUser -Name $elemento.Name
        }
    }
}

$ficheros=Get-ChildItem -file ..\*.*
foreach($elemento in $ficheros){
    Write-Host "---------------------------------------"
    Write-Host "nombre: $($elemento.Name)"
    Write-Host "tamaño: $($elemento.length) bytes"
}