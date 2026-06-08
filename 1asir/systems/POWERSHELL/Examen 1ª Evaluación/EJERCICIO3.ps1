$tarjetasdelsis=Get-CimInstance -Class Win32_NetworkAdapterConfiguration | Select-Object servicename | Format-Table
$tarjetasdelsis
$nombretarjeta=read-host "dime una tarjeta del sistema"
$tarjeta=Get-CimInstance -Class Win32_NetworkAdapterConfiguration | Where-Object ServiceName -like "$nombretarjeta" | Select-Object IPAddress, IPSubnet, DefaultIPGateway, DNSDomain
if(($tarjeta).count -ne 0){
    $tarjeta
}else{
    write-host "la tarjeta del sistema que has nombrado no existe"
}