# Configuración de Cloud CDN para Imágenes

Esta guía te ayudará a configurar Google Cloud CDN para servir las imágenes de tu aplicación de manera más rápida mediante caché distribuido globalmente.

## ¿Qué es Cloud CDN?

Cloud CDN (Content Delivery Network) es un servicio de Google Cloud que distribuye tu contenido en servidores ubicados alrededor del mundo. Cuando un usuario accede a una imagen, se sirve desde el servidor más cercano a su ubicación, reduciendo significativamente el tiempo de carga.

### Beneficios

- ✅ **Carga más rápida**: Las imágenes se sirven desde servidores cercanos al usuario
- ✅ **Caché inteligente**: Las imágenes se cachean, reduciendo solicitudes al bucket original
- ✅ **Menor latencia**: Reduce el tiempo de respuesta hasta en un 80%
- ✅ **Ahorro de costos**: Menos solicitudes al bucket = menores costos de egreso
- ✅ **Escalabilidad**: Maneja picos de tráfico automáticamente

## Requisitos Previos

1. **Google Cloud SDK instalado**: Verifica con `gcloud --version`
2. **Autenticación configurada**: `gcloud auth login`
3. **Proyecto configurado**: `gcloud config set project TU_PROJECT_ID`
4. **Permisos necesarios**: Debes tener rol de `Editor` o `Owner` en el proyecto
5. **Bucket existente**: El bucket `img-web` debe existir con tus imágenes

## Instalación Automática (Recomendado)

### Opción 1: Usando Git Bash en Windows

```bash
# Navegar al directorio del proyecto
cd /c/Users/kevin/OneDrive/Escritorio/Tienda-Carrito

# Dar permisos de ejecución al script
chmod +x setup-cdn.sh

# Ejecutar el script
./setup-cdn.sh
```

### Opción 2: Usando PowerShell en Windows

```powershell
# Navegar al directorio del proyecto
cd C:\Users\kevin\OneDrive\Escritorio\Tienda-Carrito

# Ejecutar con Git Bash
bash setup-cdn.sh
```

El script automáticamente:
1. ✓ Verifica que el bucket existe
2. ✓ Configura permisos públicos
3. ✓ Crea una IP estática global
4. ✓ Configura el backend bucket con CDN
5. ✓ Crea el URL map y proxies necesarios
6. ✓ Configura las reglas de forwarding

## Instalación Manual

Si prefieres ejecutar los comandos manualmente:

### 1. Verificar el bucket

```bash
gsutil ls -b gs://img-web
```

### 2. Hacer el bucket público

```bash
gsutil iam ch allUsers:objectViewer gs://img-web
```

### 3. Crear dirección IP estática

```bash
gcloud compute addresses create cdn-static-ip \
    --ip-version=IPV4 \
    --global
```

### 4. Crear backend bucket con CDN

```bash
gcloud compute backend-buckets create cdn-backend-img-web \
    --gcs-bucket-name=img-web \
    --enable-cdn \
    --cache-mode=CACHE_ALL_STATIC \
    --default-ttl=3600 \
    --max-ttl=86400 \
    --client-ttl=3600
```

### 5. Crear URL map

```bash
gcloud compute url-maps create cdn-url-map \
    --default-backend-bucket=cdn-backend-img-web
```

### 6. Crear target HTTP proxy

```bash
gcloud compute target-http-proxies create cdn-target-proxy \
    --url-map=cdn-url-map
```

### 7. Crear forwarding rule

```bash
gcloud compute forwarding-rules create cdn-forwarding-rule \
    --address=cdn-static-ip \
    --global \
    --target-http-proxy=cdn-target-proxy \
    --ports=80
```

## Obtener la IP del CDN

```bash
gcloud compute addresses describe cdn-static-ip --global --format="get(address)"
```

## Actualizar la Aplicación

Una vez que tengas la IP del CDN, debes actualizar las URLs en `backend/products.py`:

**Antes:**
```python
'image': 'https://storage.cloud.google.com/img-web/sharki-1g.jpg.avif'
```

**Después:**
```python
'image': 'http://TU_IP_CDN/sharki-1g.jpg.avif'
```

> **Nota**: Reemplaza `TU_IP_CDN` con la IP que obtuviste del comando anterior.

## Verificación

### 1. Verificar que el CDN está habilitado

```bash
gcloud compute backend-buckets describe cdn-backend-img-web
```

Deberías ver `enableCdn: true` en la salida.

### 2. Probar acceso a una imagen

```bash
curl -I http://TU_IP_CDN/sharki-1g.jpg.avif
```

Busca estos headers en la respuesta:
- `X-Cache: MISS` (primera vez) o `X-Cache: HIT` (desde caché)
- `Cache-Control: public, max-age=3600`

### 3. Probar en el navegador

Abre en tu navegador:
```
http://TU_IP_CDN/sharki-1g.jpg.avif
```

La imagen debería cargar correctamente.

## Configuración de Caché

El CDN está configurado con estos tiempos de caché:

- **Default TTL**: 1 hora (3600 segundos)
- **Max TTL**: 24 horas (86400 segundos)
- **Client TTL**: 1 hora (3600 segundos)

### Modificar tiempos de caché

Si necesitas ajustar los tiempos:

```bash
gcloud compute backend-buckets update cdn-backend-img-web \
    --default-ttl=7200 \
    --max-ttl=172800 \
    --client-ttl=7200
```

## Limpiar Caché

Si actualizas una imagen y necesitas que se refleje inmediatamente:

```bash
gcloud compute url-maps invalidate-cdn-cache cdn-url-map \
    --path="/sharki-1g.jpg.avif"
```

Para limpiar todo el caché:

```bash
gcloud compute url-maps invalidate-cdn-cache cdn-url-map \
    --path="/*"
```

## Costos Estimados

Cloud CDN tiene costos muy bajos:

- **Caché hit**: ~$0.02 - $0.08 por GB (dependiendo de la región)
- **Caché invalidation**: $0.005 por solicitud
- **IP estática**: ~$0.01 por hora (~$7.30/mes)

Para una tienda pequeña con tráfico moderado, el costo mensual suele ser menor a $10 USD.

## Troubleshooting

### Error: "Permission denied"

Verifica que tienes los permisos necesarios:
```bash
gcloud projects get-iam-policy $(gcloud config get-value project)
```

### Las imágenes no cargan

1. Verifica que el bucket es público
2. Espera 10-15 minutos después de la configuración
3. Verifica que la IP del forwarding rule está activa

### Caché no funciona

Verifica los headers de la respuesta:
```bash
curl -I http://TU_IP_CDN/sharki-1g.jpg.avif
```

## Configuración HTTPS (Opcional)

Para usar HTTPS necesitas un dominio propio. Si tienes uno:

1. Crear un certificado SSL
2. Crear target HTTPS proxy
3. Actualizar forwarding rule para usar puerto 443

Consulta la [documentación oficial](https://cloud.google.com/cdn/docs/setting-up-cdn-with-bucket) para más detalles.

## Recursos Adicionales

- [Documentación oficial de Cloud CDN](https://cloud.google.com/cdn/docs)
- [Mejores prácticas de caché](https://cloud.google.com/cdn/docs/best-practices)
- [Monitoreo de Cloud CDN](https://cloud.google.com/cdn/docs/monitoring)

## Deshacer Cambios

Si necesitas eliminar la configuración de CDN:

```bash
# Eliminar forwarding rule
gcloud compute forwarding-rules delete cdn-forwarding-rule --global

# Eliminar target proxy
gcloud compute target-http-proxies delete cdn-target-proxy

# Eliminar URL map
gcloud compute url-maps delete cdn-url-map

# Eliminar backend bucket
gcloud compute backend-buckets delete cdn-backend-img-web

# Liberar IP estática
gcloud compute addresses delete cdn-static-ip --global
```
