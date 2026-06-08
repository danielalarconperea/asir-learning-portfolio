Get-LocalGroup | Format-Table
$grupo=read-host "dime el nombre de un grupo"
if ((Get-LocalGroup $grupo -ErrorAction SilentlyContinue).count -ne 0){
    $usuarios=Get-LocalGroupMember $grupo | Where-Object objectclass -eq 'usuario'
    $nºusarios=($usuarios).count 
    Write-Host "El grupo tiene"$nºusarios" usuarios asociados"
}else{
    Write-Host "el nombre del grupo no existe"
}
