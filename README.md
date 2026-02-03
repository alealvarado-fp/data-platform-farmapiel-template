# ¡Bienvenido al Ecosistema de Datos!
**Centro Internacional de Cosmiatría / Farmapiel©**

Para empezar, no necesitas perder tiempo configurando infraestructura ni permisos. Nosotros ya hemos preparado la "carretera" para ti:

### Tus Recursos Asignados
* **Dataset de Pruebas:** `dm_[tu_dominio]_dev` (BigQuery)
* **Data Lake (Landing Zone):** `gs://cic-landing-[tu_dominio]` (Cloud Storage para tus archivos Parquet)
* **Gestión de Secretos:** Nunca guardes contraseñas en código. Solicita a Sistemas el nombre de la variable de entorno ya configurada en Google Secret Manager.

---

### Tu Flujo de Trabajo (Git Flow)

Para garantizar la calidad y la continuidad operativa, trabajamos bajo un esquema **Code-First**:

1. **Nueva Rama:** Crea una rama desde `master` con la nomenclatura `feat/nombre-kpi`.
2. **Desarrollo:**
   * Sube tu código de BigQuery a la carpeta `/sql`.
   * Sube tus procesos de orquestación a la carpeta `/dags`.
3. **Revisión (Pull Request):** Abre un PR hacia `master`. El equipo de Sistemas revisará:
   * Cumplimiento de la guía de estilo PEP8.
   * Idempotencia de los DAGs (cero duplicidad de datos).
4. **Despliegue:** Una vez aprobado el PR, **Sistemas hará el Merge**. Nuestro CI/CD automatizado se encargará de desplegar tu código a producción.

> ** Regla de Oro:** "Si no está en Git, no existe". Queda prohibido el uso de la consola de GCP para crear o modificar tablas y procesos productivos.