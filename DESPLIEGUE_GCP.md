# 🚀 Guía Completa de Despliegue en Google Cloud Platform

Esta guía te llevará paso a paso para desplegar tu aplicación **Tienda-Carrito** en Google Cloud Platform usando **Cloud Run**.

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Google Cloud CLI](#instalación-de-google-cloud-cli)
3. [Configuración Inicial de GCP](#configuración-inicial-de-gcp)
4. [Despliegue Manual con Cloud Run](#despliegue-manual-con-cloud-run)
5. [Despliegue Automatizado (Opcional)](#despliegue-automatizado-opcional)
6. [Configuración de Dominio Personalizado](#configuración-de-dominio-personalizado)
7. [Monitoreo y Logs](#monitoreo-y-logs)
8. [Actualizar la Aplicación](#actualizar-la-aplicación)
9. [Solución de Problemas](#solución-de-problemas)

---

## 1. Requisitos Previos

Antes de comenzar, asegúrate de tener:

- ✅ Una cuenta de Google (Gmail)
- ✅ Tarjeta de crédito/débito (para verificación, pero hay $300 USD gratis para nuevos usuarios)
- ✅ Git instalado en tu computadora
- ✅ Este proyecto descargado localmente

### 💰 Costos Estimados

- **Nivel gratuito**: Cloud Run ofrece 2 millones de solicitudes gratis al mes
- **Nuevos usuarios**: $300 USD de crédito gratis por 90 días
- **Costo real**: Para una tienda pequeña, probablemente **$0-5 USD/mes**

---

## 2. Instalación de Google Cloud CLI

### Para Windows:

1. **Descarga el instalador**:
   - Ve a: https://cloud.google.com/sdk/docs/install
   - Descarga el instalador de Windows (GoogleCloudSDKInstaller.exe)

2. **Ejecuta el instalador**:
   - Sigue las instrucciones del instalador
   - Marca la opción "Run 'gcloud init'" al finalizar

3. **Verifica la instalación**:
   ```bash
   gcloud --version
   ```

### Para Mac/Linux:

```bash
# Descarga e instala
curl https://sdk.cloud.google.com | bash

# Reinicia tu terminal y ejecuta
exec -l $SHELL

# Verifica
gcloud --version
```

---

## 3. Configuración Inicial de GCP

### Paso 3.1: Crear una Cuenta de GCP

1. Ve a: https://console.cloud.google.com
2. Inicia sesión con tu cuenta de Google
3. Acepta los términos de servicio
4. Configura la información de facturación (necesaria para activar los $300 USD gratis)

### Paso 3.2: Crear un Proyecto

1. En la consola de GCP, haz clic en el selector de proyectos (arriba a la izquierda)
2. Haz clic en **"Nuevo Proyecto"**
3. Nombre del proyecto: `tienda-carrito` (o el que prefieras)
4. Haz clic en **"Crear"**
5. Espera a que se cree el proyecto y selecciónalo

### Paso 3.3: Inicializar gcloud CLI

Abre tu terminal y ejecuta:

```bash
# Inicializar gcloud
gcloud init

# Sigue las instrucciones:
# 1. Selecciona "Log in with a new account"
# 2. Se abrirá tu navegador para autenticarte
# 3. Selecciona el proyecto que acabas de crear
# 4. Selecciona una región (recomendado: us-central1)
```

### Paso 3.4: Habilitar APIs Necesarias

```bash
# Habilitar Cloud Run API
gcloud services enable run.googleapis.com

# Habilitar Container Registry API
gcloud services enable containerregistry.googleapis.com

# Habilitar Cloud Build API (opcional, para CI/CD)
gcloud services enable cloudbuild.googleapis.com
```

---

## 4. Despliegue Manual con Cloud Run

### Paso 4.1: Navega a tu Proyecto

```bash
cd c:\Users\kevin\OneDrive\Escritorio\Tienda-Carrito
```

### Paso 4.2: Configurar el Proyecto de GCP

```bash
# Establece tu proyecto (reemplaza con tu ID de proyecto)
gcloud config set project tienda-carrito

# Establece la región
gcloud config set run/region us-central1
```

### Paso 4.3: Desplegar a Cloud Run

Este es el comando más importante. Cloud Run construirá tu Docker image y la desplegará automáticamente:

```bash
gcloud run deploy tienda-carrito \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Explicación de los parámetros**:
- `tienda-carrito`: nombre de tu servicio
- `--source .`: usa el código del directorio actual
- `--platform managed`: usa Cloud Run completamente administrado
- `--region us-central1`: región donde se desplegará
- `--allow-unauthenticated`: permite acceso público sin autenticación

### Paso 4.4: Espera el Despliegue

El proceso tomará unos 2-5 minutos. Verás algo como:

```
Building using Dockerfile and deploying container to Cloud Run service [tienda-carrito]
✓ Creating Container Repository...
✓ Uploading sources...
✓ Building Container...
✓ Deploying to Cloud Run...
✓ Setting IAM Policy...
Done.
Service [tienda-carrito] revision [tienda-carrito-00001-xxx] has been deployed
and is serving 100 percent of traffic.
Service URL: https://tienda-carrito-xxxxx-uc.a.run.app
```

### Paso 4.5: ¡Accede a tu Aplicación!

Copia la URL que aparece al final (Service URL) y ábrela en tu navegador. 

**¡Tu tienda ya está en línea! 🎉**

---

## 5. Despliegue Automatizado (Opcional)

Si quieres que tu aplicación se despliegue automáticamente cada vez que hagas cambios en Git:

### Paso 5.1: Conectar con GitHub

1. Ve a la consola de GCP: https://console.cloud.google.com/run
2. Haz clic en tu servicio `tienda-carrito`
3. Haz clic en **"SET UP CONTINUOUS DEPLOYMENT"**
4. Conecta tu repositorio de GitHub
5. Selecciona la rama (main o master)
6. Cloud Build usará el archivo `cloudbuild.yaml` que ya creamos

### Paso 5.2: Configurar Trigger

```bash
# Crear un trigger de Cloud Build
gcloud builds triggers create github \
  --repo-name=Tienda-Carrito \
  --repo-owner=TU_USUARIO_GITHUB \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml
```

Ahora, cada vez que hagas `git push`, tu aplicación se desplegará automáticamente.

---

## 6. Configuración de Dominio Personalizado

Si tienes un dominio propio (ej: `www.mitienda.com`):

### Paso 6.1: Mapear el Dominio

1. Ve a Cloud Run en la consola: https://console.cloud.google.com/run
2. Haz clic en tu servicio
3. Haz clic en **"MANAGE CUSTOM DOMAINS"**
4. Haz clic en **"ADD MAPPING"**
5. Selecciona tu servicio
6. Ingresa tu dominio
7. Sigue las instrucciones para verificar el dominio

### Paso 6.2: Configurar DNS

Agrega estos registros en tu proveedor de DNS:

```
Tipo: CNAME
Nombre: www
Valor: ghs.googlehosted.com
```

---

## 7. Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
# Ver logs de tu aplicación
gcloud run services logs read tienda-carrito --limit=50

# Seguir logs en tiempo real
gcloud run services logs tail tienda-carrito
```

### Ver Métricas en la Consola

1. Ve a: https://console.cloud.google.com/run
2. Haz clic en tu servicio `tienda-carrito`
3. Haz clic en la pestaña **"METRICS"**

Aquí verás:
- Número de solicitudes
- Latencia
- Uso de memoria
- Errores

---

## 8. Actualizar la Aplicación

Cuando hagas cambios en tu código:

### Opción A: Despliegue Manual

```bash
# Navega a tu proyecto
cd c:\Users\kevin\OneDrive\Escritorio\Tienda-Carrito

# Despliega la nueva versión
gcloud run deploy tienda-carrito \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Opción B: Con Git (si configuraste CI/CD)

```bash
git add .
git commit -m "Actualización de la tienda"
git push
```

Cloud Run desplegará automáticamente.

---

## 9. Solución de Problemas

### Problema: "Permission denied"

**Solución**:
```bash
# Verifica que estés autenticado
gcloud auth login

# Verifica el proyecto
gcloud config get-value project
```

### Problema: "API not enabled"

**Solución**:
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Problema: La aplicación no carga

**Solución**:
```bash
# Ver los logs para encontrar el error
gcloud run services logs read tienda-carrito --limit=100
```

### Problema: Error de puerto

**Solución**: Cloud Run requiere que la aplicación escuche en el puerto definido por la variable de entorno `PORT`. El Dockerfile ya está configurado correctamente para esto.

### Problema: "Build failed"

**Solución**:
1. Verifica que `requirements.txt` tenga todas las dependencias
2. Verifica que el `Dockerfile` esté en la raíz del proyecto
3. Revisa los logs de build:
   ```bash
   gcloud builds list --limit=5
   gcloud builds log [BUILD_ID]
   ```

---

## 🎯 Comandos Útiles de Referencia Rápida

```bash
# Ver servicios desplegados
gcloud run services list

# Describir un servicio
gcloud run services describe tienda-carrito

# Ver revisiones (versiones)
gcloud run revisions list

# Eliminar un servicio
gcloud run services delete tienda-carrito

# Ver uso y costos
gcloud billing accounts list
```

---

## 📞 Recursos Adicionales

- **Documentación oficial de Cloud Run**: https://cloud.google.com/run/docs
- **Precios de Cloud Run**: https://cloud.google.com/run/pricing
- **Soporte de GCP**: https://cloud.google.com/support

---

## ✅ Checklist Final

Antes de considerar el despliegue completo, verifica:

- [ ] La aplicación carga correctamente en la URL de Cloud Run
- [ ] Puedes ver los productos
- [ ] El carrito funciona correctamente
- [ ] Los botones de WhatsApp y Email funcionan
- [ ] No hay errores en los logs
- [ ] La aplicación es accesible públicamente

---

## 🎉 ¡Felicidades!

Tu tienda ya está desplegada en Google Cloud Platform y accesible desde cualquier parte del mundo.

**Próximos pasos recomendados**:
1. Configurar un dominio personalizado
2. Configurar alertas de monitoreo
3. Implementar una base de datos (Cloud SQL o Firestore) si necesitas persistencia
4. Configurar backups automáticos
5. Implementar HTTPS personalizado (Cloud Run ya incluye HTTPS gratis)

---

**¿Necesitas ayuda?** Revisa la sección de [Solución de Problemas](#solución-de-problemas) o consulta los logs de tu aplicación.
