#!/bin/bash

# Script para obtener la IP del CDN y generar las URLs actualizadas

set -e

IP_NAME="cdn-static-ip"

echo "=== Obteniendo información del CDN ==="
echo ""

# Obtener la IP
if gcloud compute addresses describe $IP_NAME --global &> /dev/null; then
    IP_ADDRESS=$(gcloud compute addresses describe $IP_NAME --global --format="get(address)")
    echo "✓ IP del CDN: $IP_ADDRESS"
    echo ""
    
    echo "=== URLs para actualizar en products.py ==="
    echo ""
    echo "Reemplaza las URLs actuales con estas:"
    echo ""
    echo "sharki-1g.jpg.avif:"
    echo "  http://$IP_ADDRESS/sharki-1g.jpg.avif"
    echo ""
    echo "sharki-2g.jpg.avif:"
    echo "  http://$IP_ADDRESS/sharki-2g.jpg.avif"
    echo ""
    
    echo "=== Comandos de verificación ==="
    echo ""
    echo "Probar imagen 1:"
    echo "  curl -I http://$IP_ADDRESS/sharki-1g.jpg.avif"
    echo ""
    echo "Probar imagen 2:"
    echo "  curl -I http://$IP_ADDRESS/sharki-2g.jpg.avif"
    echo ""
    echo "Abrir en navegador:"
    echo "  http://$IP_ADDRESS/sharki-1g.jpg.avif"
    echo ""
else
    echo "✗ Error: La IP $IP_NAME no existe"
    echo "Primero ejecuta: ./setup-cdn.sh"
    exit 1
fi
