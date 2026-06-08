#!/bin/bash
# ============================================================================
# SCRIPT DE AUTOMATIZACIÓN MAESTRO - Gestión de Apache
# Práctica Docker - 2º ASIR
# ============================================================================
#
# Este script proporciona un menú interactivo para gestionar el servicio Apache
# tanto en Docker como mediante Ansible local.
#
# Uso:
#   ./manage_service.sh              # Menú interactivo
#   ./manage_service.sh install_docker  # Instalación directa con Docker
#   ./manage_service.sh install_ansible # Instalación directa con Ansible
#
# ============================================================================

# Configuración de seguridad: fallar ante cualquier error
set -e

# Variables de configuración
CONTAINER_NAME="mi_apache"
IMAGE_NAME="mi_apache_ubuntu"
HOST_PORT=80
CONTAINER_PORT=80
HTML_DIR="$(pwd)/html"

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # Sin color

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

# Función: Imprimir mensaje de error
error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

# Función: Imprimir mensaje de éxito
success() {
    echo -e "${GREEN}[OK] $1${NC}"
}

# Función: Imprimir mensaje informativo
info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Función: Imprimir advertencia
warning() {
    echo -e "${YELLOW}[AVISO] $1${NC}"
}

# Función: Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado en el sistema."
        echo "Por favor, instala Docker primero."
        return 1
    fi
    return 0
}

# Función: Verificar si Ansible está instalado
check_ansible() {
    if ! command -v ansible-playbook &> /dev/null; then
        error "Ansible no está instalado en el sistema."
        echo "Instala con: sudo apt install ansible"
        return 1
    fi
    return 0
}

# ============================================================================
# FUNCIONES DE INFORMACIÓN
# ============================================================================

# Función: Mostrar información de red
show_network_info() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║         DATOS DE RED DEL SISTEMA          ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    
    echo -e "${YELLOW}Interfaces y direcciones IP:${NC}"
    ip addr show 2>/dev/null | grep 'inet ' | awk '{print "  " $2 " (" $NF ")"}' || \
        hostname -I 2>/dev/null | tr ' ' '\n' | sed 's/^/  /'
    
    echo ""
    echo -e "${YELLOW}Gateway por defecto:${NC}"
    ip route 2>/dev/null | grep default | awk '{print "  " $3}' || echo "  No disponible"
    
    echo ""
}

# Función: Mostrar estado del contenedor
show_container_status() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║       ESTADO DEL CONTENEDOR DOCKER        ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    
    if check_docker; then
        if docker ps -f name=$CONTAINER_NAME --format "{{.Names}}" | grep -q $CONTAINER_NAME; then
            success "Contenedor '$CONTAINER_NAME' está ACTIVO"
            echo ""
            docker ps -f name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        else
            warning "Contenedor '$CONTAINER_NAME' no está en ejecución"
        fi
    fi
    echo ""
}

# Función: Mostrar estado del servicio local
show_service_status() {
    echo ""
    echo -e "${BLUE}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║      ESTADO DEL SERVICIO APACHE LOCAL     ║${NC}"
    echo -e "${BLUE}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    
    if systemctl is-active --quiet apache2 2>/dev/null; then
        success "Servicio Apache2 está ACTIVO"
        systemctl status apache2 --no-pager -l 2>/dev/null | head -10
    else
        warning "Servicio Apache2 no está activo localmente"
    fi
    echo ""
}

# ============================================================================
# FUNCIONES DE INSTALACIÓN
# ============================================================================

# Función: Instalar con Docker
install_docker() {
    info "Iniciando instalación con Docker..."
    
    if ! check_docker; then
        return 1
    fi
    
    # Crear directorio html si no existe
    if [ ! -d "$HTML_DIR" ]; then
        mkdir -p "$HTML_DIR"
        info "Directorio $HTML_DIR creado"
    fi
    
    # Crear página de prueba si no existe
    if [ ! -f "$HTML_DIR/index.html" ]; then
        cat > "$HTML_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apache en Docker - 2º ASIR</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
            max-width: 600px;
        }
        h1 { color: #764ba2; }
        .success { color: #27ae60; font-size: 48px; }
        .info { color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✅</div>
        <h1>¡Apache Funcionando!</h1>
        <p>Servidor Docker con Ubuntu 22.04</p>
        <div class="info">
            <p><strong>Práctica:</strong> Administración de Sistemas</p>
            <p><strong>Curso:</strong> 2º ASIR</p>
        </div>
    </div>
</body>
</html>
EOF
        success "Página de prueba creada en $HTML_DIR/index.html"
    fi
    
    # Detener contenedor existente si hay alguno
    if docker ps -a -f name=$CONTAINER_NAME --format "{{.Names}}" | grep -q $CONTAINER_NAME; then
        warning "Deteniendo contenedor existente..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
    fi
    
    # Construir imagen
    info "Construyendo imagen Docker..."
    docker build -t $IMAGE_NAME .
    
    # Ejecutar contenedor
    info "Iniciando contenedor..."
    docker run -d \
        -p $HOST_PORT:$CONTAINER_PORT \
        -v "$HTML_DIR:/var/www/html" \
        --name $CONTAINER_NAME \
        $IMAGE_NAME
    
    success "Contenedor '$CONTAINER_NAME' iniciado correctamente"
    info "Accede a: http://localhost:$HOST_PORT"
    
    show_container_status
}

# Función: Instalar con Ansible
install_ansible() {
    info "Iniciando instalación con Ansible..."
    
    if ! check_ansible; then
        return 1
    fi
    
    if [ ! -f "install_apache.yml" ]; then
        error "Archivo install_apache.yml no encontrado"
        return 1
    fi
    
    ansible-playbook install_apache.yml --ask-become-pass
    
    success "Instalación con Ansible completada"
    show_service_status
}

# ============================================================================
# FUNCIONES DE GESTIÓN DE CONTENEDOR
# ============================================================================

# Función: Ver logs del contenedor
show_logs() {
    if ! check_docker; then return 1; fi
    
    if docker ps -f name=$CONTAINER_NAME --format "{{.Names}}" | grep -q $CONTAINER_NAME; then
        info "Mostrando logs del contenedor (Ctrl+C para salir)..."
        docker logs -f $CONTAINER_NAME
    else
        error "El contenedor '$CONTAINER_NAME' no está en ejecución"
    fi
}

# Función: Detener contenedor
stop_container() {
    if ! check_docker; then return 1; fi
    
    info "Deteniendo contenedor..."
    docker stop $CONTAINER_NAME 2>/dev/null && success "Contenedor detenido" || error "Error al detener"
}

# Función: Iniciar contenedor
start_container() {
    if ! check_docker; then return 1; fi
    
    info "Iniciando contenedor..."
    docker start $CONTAINER_NAME 2>/dev/null && success "Contenedor iniciado" || error "Error al iniciar"
}

# Función: Reiniciar contenedor
restart_container() {
    if ! check_docker; then return 1; fi
    
    info "Reiniciando contenedor..."
    docker restart $CONTAINER_NAME 2>/dev/null && success "Contenedor reiniciado" || error "Error al reiniciar"
}

# Función: Eliminar contenedor e imagen
cleanup() {
    if ! check_docker; then return 1; fi
    
    warning "Esto eliminará el contenedor y la imagen. ¿Continuar? (s/n)"
    read -r respuesta
    if [[ "$respuesta" =~ ^[Ss]$ ]]; then
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
        docker rmi $IMAGE_NAME 2>/dev/null || true
        success "Limpieza completada"
    else
        info "Operación cancelada"
    fi
}

# Función: Acceder al shell del contenedor
shell_access() {
    if ! check_docker; then return 1; fi
    
    if docker ps -f name=$CONTAINER_NAME --format "{{.Names}}" | grep -q $CONTAINER_NAME; then
        info "Accediendo al shell del contenedor (escribe 'exit' para salir)..."
        docker exec -it $CONTAINER_NAME /bin/bash
    else
        error "El contenedor '$CONTAINER_NAME' no está en ejecución"
    fi
}

# ============================================================================
# MENÚ INTERACTIVO
# ============================================================================

show_menu() {
    clear
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║          🐳 GESTOR DE APACHE - PRÁCTICA DOCKER 🐳           ║"
    echo "║                      2º ASIR                                 ║"
    echo "║                                                              ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                      INSTALACIÓN                             ║"
    echo "║  1) Instalar con Docker                                      ║"
    echo "║  2) Instalar con Ansible (local)                             ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                      GESTIÓN                                 ║"
    echo "║  3) Iniciar contenedor                                       ║"
    echo "║  4) Detener contenedor                                       ║"
    echo "║  5) Reiniciar contenedor                                     ║"
    echo "║  6) Ver logs                                                 ║"
    echo "║  7) Acceder al shell del contenedor                          ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                     INFORMACIÓN                              ║"
    echo "║  8) Ver estado del contenedor                                ║"
    echo "║  9) Ver estado del servicio local                            ║"
    echo "║ 10) Ver información de red                                   ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║                      LIMPIEZA                                ║"
    echo "║ 11) Eliminar contenedor e imagen                             ║"
    echo "╠══════════════════════════════════════════════════════════════╣"
    echo "║  0) Salir                                                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

# Manejo de parámetros directos
if [ $# -gt 0 ]; then
    case "$1" in
        install_docker)
            install_docker
            ;;
        install_ansible)
            install_ansible
            ;;
        logs)
            show_logs
            ;;
        start)
            start_container
            ;;
        stop)
            stop_container
            ;;
        restart)
            restart_container
            ;;
        status)
            show_container_status
            ;;
        network)
            show_network_info
            ;;
        shell)
            shell_access
            ;;
        cleanup)
            cleanup
            ;;
        *)
            echo "Uso: $0 {install_docker|install_ansible|logs|start|stop|restart|status|network|shell|cleanup}"
            echo ""
            echo "  install_docker  - Construir imagen y ejecutar contenedor"
            echo "  install_ansible - Instalar Apache con Ansible"
            echo "  logs            - Ver logs del contenedor"
            echo "  start           - Iniciar contenedor"
            echo "  stop            - Detener contenedor"
            echo "  restart         - Reiniciar contenedor"
            echo "  status          - Ver estado del contenedor"
            echo "  network         - Ver información de red"
            echo "  shell           - Acceder al shell del contenedor"
            echo "  cleanup         - Eliminar contenedor e imagen"
            exit 1
            ;;
    esac
    exit 0
fi

# Menú interactivo
while true; do
    show_menu
    read -p "Selecciona una opción: " opcion
    
    case $opcion in
        1) install_docker ;;
        2) install_ansible ;;
        3) start_container ;;
        4) stop_container ;;
        5) restart_container ;;
        6) show_logs ;;
        7) shell_access ;;
        8) show_container_status ;;
        9) show_service_status ;;
        10) show_network_info ;;
        11) cleanup ;;
        0) 
            info "¡Hasta luego!"
            exit 0
            ;;
        *)
            error "Opción no válida"
            ;;
    esac
    
    echo ""
    read -p "Presiona ENTER para continuar..."
done
