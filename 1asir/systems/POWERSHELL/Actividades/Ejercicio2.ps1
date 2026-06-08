# Obtener la lista de usuarios del sistema y mostrarla por pantalla indicando si 
# están activos o si no y su fecha de última conexión. Pedir un nombre de usuario 
# que queremos modificar y si queremos activarlo o desactivarlo. Después 
# preguntar al usuario si deseamos repetir

do {
    Get-LocalUser | Select-Object Name, Enabled, Lastlogon | format-table
    $nombre = Read-Host "Dime un nombre de usuario que quieras activar/desactivar"
    $usuario = Get-LocalUser -Name $nombre
    if ($usuario) {
        $accion = Read-Host "¿Quieres activarlo (A) o desactivarlo (D)?"
        switch ($accion) {
            "A" {
                Enable-LocalUser -Name $nombre
                Write-Host "El usuario $nombre ha sido activado."
            }
            "D" {
                Disable-LocalUser -Name $nombre
                Write-Host "El usuario $nombre ha sido desactivado."
            }
            Default {
                Write-Host "Opción no válida. Inténtalo de nuevo."
            }
        }
    } else {
        Write-Host "El usuario $nombre no existe. Inténtalo de nuevo."
    }
    $rep = Read-Host "¿Quieres repetir S/N?" 
} while ($rep -eq "S")
