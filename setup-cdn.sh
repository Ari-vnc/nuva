#!/bin/bash

# Script para configurar Cloud CDN con Google Cloud Storage
# Este script automatiza la configuración de CDN para mejorar la velocidad de carga de imágenes

set -e

echo "=== Configuración de Cloud CDN para Google Cloud Storage ==="
echo ""

# Variables de configuración
PROJECT_ID=$(gcloud config get-value project)
BUCKET_NAME="img-web"
BACKEND_BUCKET_NAME="cdn-backend-img-web"
URL_MAP_NAME="cdn-url-map"
TARGET_PROXY_NAME="cdn-target-proxy"
FORWARDING_RULE_NAME="cdn-forwarding-rule"
IP_NAME="cdn-static-ip"

echo "Proyecto: $PROJECT_ID"
echo "Bucket: $BUCKET_NAME"
echo ""

# Paso 1: Verificar que el bucket existe
echo "Paso 1: Verificando que el bucket existe..."
if gsutil ls -b gs://$BUCKET_NAME &> /dev/null; then
    echo "✓ Bucket $BUCKET_NAME encontrado"
else
    echo "✗ Error: El bucket $BUCKET_NAME no existe"
    exit 1
fi

# Paso 2: Hacer el bucket público (si no lo está ya)
echo ""
echo "Paso 2: Configurando permisos del bucket..."
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
echo "✓ Bucket configurado como público"

# Paso 3: Reservar una dirección IP estática global
echo ""
echo "Paso 3: Reservando dirección IP estática global..."
if gcloud compute addresses describe $IP_NAME --global &> /dev/null; then
    echo "✓ La dirección IP $IP_NAME ya existe"
    IP_ADDRESS=$(gcloud compute addresses describe $IP_NAME --global --format="get(address)")
else
    gcloud compute addresses create $IP_NAME \
        --ip-version=IPV4 \
        --global
    IP_ADDRESS=$(gcloud compute addresses describe $IP_NAME --global --format="get(address)")
    echo "✓ Dirección IP creada: $IP_ADDRESS"
fi

# Paso 4: Crear backend bucket
echo ""
echo "Paso 4: Creando backend bucket..."
if gcloud compute backend-buckets describe $BACKEND_BUCKET_NAME &> /dev/null; then
    echo "✓ Backend bucket $BACKEND_BUCKET_NAME ya existe"
    echo "  Actualizando configuración..."
    gcloud compute backend-buckets update $BACKEND_BUCKET_NAME \
        --gcs-bucket-name=$BUCKET_NAME \
        --enable-cdn \
        --cache-mode=CACHE_ALL_STATIC \
        --default-ttl=3600 \
        --max-ttl=86400 \
        --client-ttl=3600
else
    gcloud compute backend-buckets create $BACKEND_BUCKET_NAME \
        --gcs-bucket-name=$BUCKET_NAME \
        --enable-cdn \
        --cache-mode=CACHE_ALL_STATIC \
        --default-ttl=3600 \
        --max-ttl=86400 \
        --client-ttl=3600
    echo "✓ Backend bucket creado con CDN habilitado"
fi

# Paso 5: Crear URL map
echo ""
echo "Paso 5: Creando URL map..."
if gcloud compute url-maps describe $URL_MAP_NAME &> /dev/null; then
    echo "✓ URL map $URL_MAP_NAME ya existe"
else
    gcloud compute url-maps create $URL_MAP_NAME \
        --default-backend-bucket=$BACKEND_BUCKET_NAME
    echo "✓ URL map creado"
fi

# Paso 6: Crear target HTTP proxy
echo ""
echo "Paso 6: Creando target HTTP proxy..."
if gcloud compute target-http-proxies describe $TARGET_PROXY_NAME &> /dev/null; then
    echo "✓ Target HTTP proxy $TARGET_PROXY_NAME ya existe"
else
    gcloud compute target-http-proxies create $TARGET_PROXY_NAME \
        --url-map=$URL_MAP_NAME
    echo "✓ Target HTTP proxy creado"
fi

# Paso 7: Crear forwarding rule
echo ""
echo "Paso 7: Creando forwarding rule..."
if gcloud compute forwarding-rules describe $FORWARDING_RULE_NAME --global &> /dev/null; then
    echo "✓ Forwarding rule $FORWARDING_RULE_NAME ya existe"
else
    gcloud compute forwarding-rules create $FORWARDING_RULE_NAME \
        --address=$IP_NAME \
        --global \
        --target-http-proxy=$TARGET_PROXY_NAME \
        --ports=80
    echo "✓ Forwarding rule creado"
fi

# Resumen
echo ""
echo "=== Configuración Completada ==="
echo ""
echo "Tu CDN está configurado y listo para usar!"
echo ""
echo "Dirección IP del CDN: $IP_ADDRESS"
echo "URL base del CDN: http://$IP_ADDRESS"
echo ""
echo "Ejemplos de URLs:"
echo "  - http://$IP_ADDRESS/sharki-1g.jpg.avif"
echo "  - http://$IP_ADDRESS/sharki-2g.jpg.avif"
echo ""
echo "IMPORTANTE: Puede tomar hasta 15 minutos para que el CDN esté completamente activo."
echo ""
echo "Para verificar el estado del CDN:"
echo "  gcloud compute backend-buckets describe $BACKEND_BUCKET_NAME"
echo ""
echo "Para probar una imagen:"
echo "  curl -I http://$IP_ADDRESS/sharki-1g.jpg.avif"
echo ""
