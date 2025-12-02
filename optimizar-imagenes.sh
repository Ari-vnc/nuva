#!/bin/bash

# Script para configurar el alias de Python y ejecutar la optimización

echo "=== Configurando Python para gcloud ==="
echo ""

# Crear alias temporal de python a py
alias python='py'
alias python3='py'

# Exportar para que esté disponible en subshells
export CLOUDSDK_PYTHON=$(which py)

echo "✓ Python configurado"
echo ""

# Ahora ejecutar la optimización
echo "=== Optimización de Carga de Imágenes ==="
echo ""

BUCKET_NAME="img-web"

echo "Configurando headers de caché para el bucket: $BUCKET_NAME"
echo ""

# Configurar metadata de caché para todas las imágenes
echo "Paso 1: Configurando Cache-Control en las imágenes..."

# Para archivos .avif
gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" \
    -h "Content-Type:image/avif" \
    gs://$BUCKET_NAME/*.avif

echo "✓ Headers de caché configurados para archivos .avif"

# Para archivos .jpg (si existen)
if gsutil ls gs://$BUCKET_NAME/*.jpg 2>/dev/null; then
    gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" \
        -h "Content-Type:image/jpeg" \
        gs://$BUCKET_NAME/*.jpg
    echo "✓ Headers de caché configurados para archivos .jpg"
fi

# Para archivos .png (si existen)
if gsutil ls gs://$BUCKET_NAME/*.png 2>/dev/null; then
    gsutil -m setmeta -h "Cache-Control:public, max-age=31536000" \
        -h "Content-Type:image/png" \
        gs://$BUCKET_NAME/*.png
    echo "✓ Headers de caché configurados para archivos .png"
fi

echo ""
echo "=== Configuración completada ==="
echo ""
echo "Las imágenes ahora se cachearán en el navegador durante 1 año (31536000 segundos)"
echo ""
echo "Beneficios:"
echo "  ✓ Primera carga: normal"
echo "  ✓ Cargas siguientes: instantáneas (desde caché del navegador)"
echo "  ✓ Ahorro de ancho de banda"
echo "  ✓ Mejor experiencia de usuario"
echo ""
echo "Para verificar los headers:"
echo "  curl -I https://storage.googleapis.com/img-web/sharki-1g.jpg.avif"
echo ""
