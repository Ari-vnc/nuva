# Optimización de Carga de Imágenes

Esta guía te ayudará a optimizar la velocidad de carga de imágenes configurando headers de caché en Google Cloud Storage, sin necesidad de configurar Cloud CDN.

## ¿Cómo funciona?

Cuando configuras headers de caché apropiados en tus imágenes:
- **Primera visita**: La imagen se descarga normalmente
- **Visitas posteriores**: La imagen se carga **instantáneamente** desde el caché del navegador
- **Sin configuración compleja**: Solo un comando simple

## Beneficios ✨

- ✅ **Carga instantánea** en visitas repetidas
- ✅ **Fácil de implementar** (1 comando)
- ✅ **Sin costos adicionales**
- ✅ **Ahorro de ancho de banda** (menos solicitudes al servidor)
- ✅ **Mejor experiencia de usuario**

## Requisitos

Solo necesitas tener **gsutil** instalado (viene con Google Cloud SDK).

Verifica que funcione:
```bash
gsutil ls
```

## Instalación (1 minuto) ⚡

### Paso 1: Ejecutar el script

Abre **Git Bash** o **PowerShell** y ejecuta:

```bash
bash optimizar-imagenes.sh
```

Eso es todo! 🎉

### ¿Qué hace el script?

El script configura automáticamente estos headers en todas tus imágenes:

```
Cache-Control: public, max-age=31536000
```

Esto significa:
- `public`: El caché puede ser usado por cualquiera (navegadores, proxies)
- `max-age=31536000`: Cachear durante 1 año (365 días)

## Verificación

### 1. Verificar headers de una imagen

```bash
curl -I https://storage.googleapis.com/img-web/sharki-1g.jpg.avif
```

Deberías ver en la respuesta:
```
Cache-Control: public, max-age=31536000
```

### 2. Probar en el navegador

1. Abre la consola del navegador (F12)
2. Ve a la pestaña **Network**
3. Carga tu página
4. Recarga la página (F5)
5. Verás que las imágenes aparecen como `(from disk cache)` o `(from memory cache)`

## Optimizaciones Adicionales

### Para nuevas imágenes

Cuando subas nuevas imágenes al bucket, configura los headers automáticamente:

```bash
gsutil -h "Cache-Control:public, max-age=31536000" cp imagen.avif gs://img-web/
```

### Configurar caché por defecto en el bucket

Para que TODAS las imágenes futuras tengan caché automáticamente:

```bash
gsutil defstorageclass set STANDARD gs://img-web
gsutil setmeta -h "Cache-Control:public, max-age=31536000" gs://img-web
```

## Tiempos de Caché Recomendados

Según el tipo de contenido:

| Tipo | Tiempo | Valor `max-age` |
|------|--------|-----------------|
| Imágenes de productos (estáticas) | 1 año | 31536000 |
| Imágenes que cambian ocasionalmente | 1 mes | 2592000 |
| Imágenes que cambian frecuentemente | 1 día | 86400 |
| Imágenes en tiempo real | 1 hora | 3600 |

Para tu caso (imágenes de productos), **1 año es perfecto**.

## Actualizar una imagen

Si necesitas actualizar una imagen que ya está cacheada:

**Opción 1: Cambiar el nombre del archivo** (recomendado)
```bash
# En products.py cambia:
# 'sharki-1g.jpg.avif' -> 'sharki-1g-v2.jpg.avif'
```

**Opción 2: Esperar que expire el caché** (31536000 segundos = 1 año)

**Opción 3: Los usuarios pueden forzar recarga** (Ctrl + F5 en el navegador)

## Comparación con Cloud CDN

| Característica | Caché en Navegador | Cloud CDN |
|----------------|-------------------|-----------|
| Velocidad (2da visita) | ⚡ Instantánea | ⚡⚡ Casi instantánea |
| Velocidad (1ra visita) | Normal | 🚀 Muy rápida |
| Configuración | ✅ 1 minuto | ⚠️ 15-30 minutos |
| Costo adicional | ✅ Gratis | 💰 ~$5-10/mes |
| Complejidad | ✅ Muy simple | ⚠️ Media |
| Cobertura global | ❌ No | ✅ Sí |

**Recomendación**: 
- Para **tiendas pequeñas/medianas**: Caché en navegador (esta opción)
- Para **tiendas grandes con tráfico internacional**: Cloud CDN

## Troubleshooting

### Error: "gsutil: command not found"

Necesitas instalar Google Cloud SDK:
1. Descarga desde: https://cloud.google.com/sdk/docs/install
2. Sigue las instrucciones de instalación
3. Ejecuta: `gcloud init`

### Las imágenes no se cachean

1. Verifica los headers con:
   ```bash
   curl -I https://storage.googleapis.com/img-web/sharki-1g.jpg.avif
   ```

2. Limpia el caché del navegador (Ctrl + Shift + Delete)

3. Vuelve a cargar la página

### Error de permisos

Asegúrate de estar autenticado:
```bash
gcloud auth login
```

## Siguiente Paso: Optimizar el Tamaño

Si quieres mejorar aún más la velocidad, considera:

1. **Comprimir imágenes**: Usa herramientas como `squoosh.app`
2. **Formato WebP/AVIF**: Ya lo estás usando ✓
3. **Lazy loading**: Cargar imágenes solo cuando son visibles
4. **Responsive images**: Diferentes tamaños para diferentes dispositivos

¿Quieres que te ayude con alguna de estas optimizaciones adicionales?
