# Gobierno de Datos, Software, Identidades y Estándares de Integración
> **Copyright (c) 2026 [Centro Internacional de Cosmiatria]. Todos los derechos reservados.**

Este repositorio sirve como el estándar maestro para cualquier desarrollo contratado o interno. El objetivo principal es garantizar la **interoperabilidad total y la soberanía tecnológica**, sin importar si la aplicación reside en servidores propios o plataformas de terceros como Meta, TikTok, Amazon o Google.

## 1. Soberanía de Identidades y Gestión de Secretos
El control de las credenciales y accesos es una facultad exclusiva de la empresa.

* **Ambiente de Desarrollo (DEV):** Se permite el uso de archivos `.env` locales para agilidad del desarrollador (siempre basados en el archivo `.env.example`). Estos archivos tienen estrictamente prohibido ser subidos al repositorio.
* **Ambientes de Test y Producción (PRD):** El control es absoluto del **Centro Internacional de Cosmiatría**. Queda prohibido el uso de archivos físicos `.env` en estos entornos. Las identidades se gestionarán mediante **Secret Managers** (ej. Google Secret Manager) y el código debe ser diseñado para consumir estas variables inyectadas directamente por el sistema.
* **Aislamiento y Auditoría:** Cada solución (TikTok, Amazon, SAP, etc.) deberá utilizar una identidad de servicio única para garantizar la trazabilidad y auditoría de accesos.

## 2. Estándares por Lenguaje y Ecosistema (Reglas de "Caja Negra")
Sin importar el lenguaje de programación, se deben cumplir las siguientes normas de calidad:

* **.NET (C# / F#):** Uso obligatorio de archivos `appsettings.json` para configuración de desarrollo y **User Secrets** para evitar credenciales locales. El código debe seguir las convenciones de diseño de Microsoft y utilizar inyección de dependencias nativa para la gestión de servicios.
* **Python (Backend/IA):** Uso obligatorio de entornos virtuales y cumplimiento riguroso del estándar de estilo PEP8.
* **Node.js (Web/Apps):** Gestión estricta de dependencias en el archivo `package.json` y prevención activa de vulnerabilidades mediante la ejecución periódica de `npm audit`.
* **Java (Enterprise):** Uso de Maven o Gradle para la gestión de dependencias y cumplimiento de los estándares de codificación de Google o Oracle.
* **PHP (Legacy/Web):** Uso obligatorio de Composer para dependencias y cumplimiento de los estándares PSR (PHP Standards Recommendations).
* **Desarrollo Móvil (Swift/Kotlin):** Gestión de dependencias mediante gestores oficiales (CocoaPods/Swift Package Manager o Gradle) y aislamiento estricto de llaves de API en archivos de configuración no versionados.
* **Integraciones de Redes Sociales (Meta/TikTok/Otras):** Toda la lógica de tokens (OAuth) debe seguir flujos de refresco automático y almacenamiento cifrado. Queda estrictamente prohibido el "Hardcoding" de App IDs, Client Secrets o cualquier tipo de llave de acceso.

## 3. API First y Documentación Universal (Modelo C4)
Para garantizar que equipos de diferentes lenguajes y plataformas se entiendan perfectamente:

* **Contratos JSON:** Todas las respuestas de la API deben seguir el formato estandarizado definido en este template (ej. el esquema de OData utilizado para las integraciones con SAP).
* **Modelo C4 Obligatorio:** Es mandatorio que todo proveedor entregue y mantenga actualizados los diagramas de **Contexto (Nivel 1)** y **Contenedores (Nivel 2)** en formato fuente `.puml` y su exportación funcional `.svg` dentro de la carpeta `docs/images/`.
## 4. Propiedad Intelectual y "Zero Trust"
* **Titularidad:** El Centro Internacional de Cosmiatría es el único titular de los derechos de autor de cualquier línea de código generada bajo contrato. No se aceptarán esquemas de "código cerrado" que impidan la auditoría, edición o mantenimiento interno.
* **Encabezados:** Todo módulo de código fuente debe incluir el bloque de Copyright oficial en las primeras líneas del archivo.

## 5. Checklist de Entrega para Proveedores
Para que una entrega sea considerada válida y proceda al pago, debe cumplir con:

1. [ ] ¿El archivo README incluye el Copyright oficial y la descripción técnica del proyecto?
2. [ ] ¿Se entregaron los diagramas .puml y .svg (Modelo C4) actualizados y son legibles directamente en el repositorio?
3. [ ] ¿El código está libre de credenciales expuestas y utiliza inyección de variables para los entornos de producción?
4. [ ] ¿La documentación de la API es compatible con estándares como Swagger/OpenAPI?
5. [ ] ¿El código fuente completo reside en el repositorio oficial asignado por la empresa?