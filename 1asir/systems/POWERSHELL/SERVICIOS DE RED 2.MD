```powershell
# Ejemplo para SRV1 (Ajusta 'Ethernet')

$interfaceName = "Ethernet 2" 
$ipAddress = "192.168.1.10"
$prefixLength = 24
$gateway = "192.168.1.1"
$dns1 = "192.168.1.1"
$dns2 = "8.8.8.8"

# Quitar configuración DHCP si existe
# Set-NetIPInterface -InterfaceAlias $interfaceName -Dhcp Disabled

# Quitar IPs previas si es necesario (cuidado si tienes varias IPs)
# Get-NetIPAddress -InterfaceAlias $interfaceName | Remove-NetIPAddress -Confirm:$false

# Configurar IP Estática
New-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $ipAddress -PrefixLength $prefixLength -DefaultGateway $gateway

# Configurar DNS (Inicial)
Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses ($dns1) # Añade $dns2 entre paréntesis si lo usas: ($dns1, $dns2)

Write-Host "Configuración de red estática aplicada a $interfaceName en SRV1 (IP: $ipAddress)."
# Recuerda cambiar el DNS después de instalar AD a 127.0.0.1 o la IP del propio servidor.

$interfaceName = "Ethernet 2"
$ipAddress = "192.168.1.11"
$prefixLength = 24
$gateway = "192.168.1.1"
$dns1 = "192.168.1.1"

# Configurar IP Estática
New-NetIPAddress -InterfaceAlias $interfaceName -IPAddress $ipAddress -PrefixLength $prefixLength -DefaultGateway $gateway

# Configurar DNS (Inicial)
Set-DnsClientServerAddress -InterfaceAlias $interfaceName -ServerAddresses ($dns1)

Write-Host "Configuración de red estática aplicada a $interfaceName en SRV2 (IP: $ipAddress)."
# Recuerda cambiar el DNS después de unir SRV2 al dominio a la IP de SRV1.
