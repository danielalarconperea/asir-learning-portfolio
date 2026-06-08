# Buscar el comando para crear usuarios en el sistema y crear un script que 
# permita crear 5 usuarios:
# a. Con el prefijo que nos indique por teclado el usuario
# b. Si el usuario ya existe no debe crearlo. Debe mostrarnos un mensaje de 
# error por pantalla antes de intentar crearlo y seguir con el siguiente. 
# c. Si el usuario no existe le pondrá una contraseña y lo creará.

do{
    $prefijo=read-host "dime un prefijo para los usuarios"
    for($i=1;$i -le 5; $i++){
        $usuario = Get-LocalUser | Where-Object { $_.Name -ne "$prefijo$i"}
        if(($usuario)){
            New-LocalUser $prefijo$i
        }else{
            Write-Host "ERROR. El usuario ya existe"
        }
    }
}while (Get-LocalUser | Where-Object { $_.Name -eq "$prefijo$i"})
Remove-LocalUser $prefijo$i