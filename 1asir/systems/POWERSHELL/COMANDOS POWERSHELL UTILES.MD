# Ejemplo para SRV1 (Ajusta 'Ethernet')
```powershell
$interfaceName = "Ethernet 2" 
$ipAddress = "192.168.1.10"
$prefixLength = 24
$gateway = "192.168.1.1"
$dns1 = "192.168.1.1"
$dns2 = "8.8.8.8"
```
# Quitar configuración DHCP si existe
# Set-NetIPInterface -InterfaceAlias $interfaceName -Dhcp Disabled

# Quitar IPs previas si es necesario (cuidado si tienes varias IPs)
# Get-NetIPAddress -InterfaceAlias $interfaceName | Remove-NetIPAddress -Confirm:$false

# Configurar IP Estática
```powershell
New-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $ipAddress -PrefixLength $prefixLength -DefaultGateway $gateway
```
# Configurar DNS (Inicial)
```powershell
Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses ($dns1, $dns2)
```


# Cambiar el nombre del ordenador
```powershell
Rename-Computer -NewName "PC1" -Restart
```


# Instalar Rol AD DS y DNS en S1
```powershell
Install-WindowsFeature AD-Domain-Services, DNS -IncludeManagementTools

# Una vez se ha descargado

Import-Module ADDSDeployment
Install-ADDSForest `
    -CreateDnsDelegation:$false `
    -DatabasePath "C:\Windows\NTDS" `
    -DomainMode "WinThreshold" `  
    -DomainName "dominio2.es" `
    -DomainNetbiosName "DOMINIO2" ` 
    -ForestMode "WinThreshold" `  
    -InstallDns:$true `
    -LogPath "C:\Windows\NTDS" `
    -NoRebootOnCompletion:$false `
    -SysvolPath "C:\Windows\SYSVOL" `
    -Force:$true 


Set-DnsClientServerAddress -InterfaceAlias "Ethernet 2" -ServerAddresses ("127.0.0.1")
```
# Se pedirá la contraseña DSRM de forma segura


# Unir al Dominio s2
```powershell
# Introduce DOMINIO1\Administrador y contraseña
$domainCred = Get-Credential 
Add-Computer -DomainName "dominio1.es" -Credential $domainCred -Restart
```