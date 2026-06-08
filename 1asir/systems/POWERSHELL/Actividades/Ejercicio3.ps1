# Si tenemos un comando “Get-Service” que nos devuelve los servicios instalados 
# en el sistema, pedir al usuario el nombre de un servicio y mostrar un menú en 
# el que podamos:
# E - Saber estado del servicio y su descripción
# P - Parar el servicio (Stop-Service)
# I - Iniciar el servicio (Start-Service)
# S - Salir
# (La opción “P” solo nos debe salir si el servicio está iniciado y la “I” en 
# caso de que esté parado)

$serv = Read-Host "Dime el nombre de un servicio instalado"
do {
    # Obtener el estado actual del servicio
    $servicio = Get-Service -Name $serv
    $estado = $servicio.Status

    Write-Host "----------------------------------------------"
    Write-Host "E - Saber estado del servicio y su descripción"

    if ($estado -eq "Running") {
        Write-Host "P - Parar el servicio (Stop-Service)"
    } elseif ($estado -eq "Stopped") {
        Write-Host "I - Iniciar el servicio (Start-Service)"
    }
    
    Write-Host "S - Salir"
    Write-Host "----------------------------------------------"
    $valor = Read-Host "Dime una opción"
    switch ($valor) {
        "E" { 
            Get-Service $serv | Select-Object Name, Status, DisplayName 
        }
        "P" { 
            if ($estado -eq "Running") {
                Stop-Service $serv
                Write-Host "Servicio detenido."
                $estado = (Get-Service -Name $serv).Status
            } else {
                Write-Host "El servicio no está en ejecución."
            }
        }
        "I" { 
            if ($estado -eq "Stopped") {
                Start-Service $serv 
                Write-Host "Servicio iniciado."
                $estado = (Get-Service -Name $serv).Status
            } else {
                Write-Host "El servicio ya está en ejecución."
            }
        }
        "S" { 
            Write-Host "Hasta luego" 
        }
        Default { 
            Write-Host "Te has equivocado, esa opción no existe" 
        }
    }
} while ($valor -ne "S")
