"""
Copyright (c) 2026 [Centro Internacional de Cosmiatría / Farmapiel©]
Autor: Equipo de Sistemas (Basado en Estándar de Resiliencia y Monitoreo)
Descripción: Carga idempotente SAP -> BigQuery con Telemetría Avanzada (Logging, UTC, Duración)
"""

import logging
import pendulum
from datetime import datetime, timezone
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

# =============================================================================
# 1. CONFIGURACIÓN DE LOGGING Y TELEMETRÍA
# =============================================================================
logger = logging.getLogger("cic_data_platform")

def on_task_start(context):
    """Captura el inicio exacto de la tarea en UTC"""
    ti = context['task_instance']
    start_time = pendulum.now('UTC')
    logger.info(f"[INI] Tarea: {ti.task_id} | DAG: {ti.dag_id} | Run ID: {context['run_id']}")
    logger.info(f"Timestamp (UTC): {start_time.isoformat()}")

def on_task_success(context):
    """Captura el éxito, calcula la duración y registra el fin en UTC"""
    ti = context['task_instance']
    end_time = pendulum.now('UTC')
    # Airflow guarda el start_date en la base de datos de Task Instance
    start_time = ti.start_date 
    duration_seconds = (end_time - start_time).total_seconds()
    
    logger.info(f"[ÉXITO] Tarea: {ti.task_id} completada.")
    logger.info(f"Timestamp Fin (UTC): {end_time.isoformat()}")
    logger.info(f"Duración Total: {duration_seconds:.2f} segundos ({duration_seconds/60:.2f} minutos)")

def on_task_failure(context):
    """Captura el error crítico para disparar alertas"""
    ti = context['task_instance']
    fail_time = pendulum.now('UTC')
    exception = context.get('exception')
    logger.error(f"[ERROR] Tarea: {ti.task_id} falló a las {fail_time.isoformat()}")
    logger.error(f"Detalle del error: {str(exception)}")

# =============================================================================
# 2. DEFINICIÓN DEL DAG
# =============================================================================
# Usamos 'pendulum' para forzar que el cronómetro del DAG esté 100% en UTC
DEFAULT_ARGS = {
    'owner': 'sistemas_cic',
    'depends_on_past': False,
    'email_on_failure': False, # Aquí puedes poner tu correo a futuro
    'email_on_retry': False,
    'retries': 2, # Se reintenta 2 veces si falla la red
}

with DAG(
    dag_id='comercial_sap_oinv_to_bronze', 
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"), 
    schedule_interval='@daily',
    default_args=DEFAULT_ARGS,
    catchup=False,
    tags=['sap', 'comercial', 'ingesta', 'monitoreo_activo']
) as dag:

    # =========================================================================
    # 3. TAREA DE INGESTA CON AUDITORÍA (MERGE + DATAPLEX LABELS + LOGS)
    # =========================================================================
    load_fact_invoice = BigQueryInsertJobOperator(
        task_id='merge_invoices_sap',
        on_execute_callback=on_task_start,   # Dispara el log de inicio
        on_success_callback=on_task_success, # Dispara el log de duración/éxito
        on_failure_callback=on_task_failure, # Dispara el log de error
        configuration={
            "query": {
                "query": """
                    MERGE `proyecto.dm_comercial.fact_ventas` T
                    USING `proyecto.stg_sap.oinv_external` S
                    ON T.DocEntry = S.DocEntry AND T.DocDate = S.DocDate
                    WHEN MATCHED THEN
                      UPDATE SET T.DocTotal = S.DocTotal, T.UpdateTime = CURRENT_TIMESTAMP()
                    WHEN NOT MATCHED THEN
                      INSERT (DocEntry, DocDate, CardCode, DocTotal) 
                      VALUES (S.DocEntry, S.DocDate, S.CardCode, S.DocTotal)
                """,
                "useLegacySql": False,
            },
            # Etiquetas para Gobernanza en Dataplex
            "labels": {
                "dominio": "comercial",
                "origen": "sap_b1",
                "proveedor": "vendor_template",
                "dag_id": "comercial_sap_oinv_to_bronze",
                "entorno": "prod"
            }
        }
    )

    # Si tuvieras más tareas, se encadenarían aquí:
    # load_fact_invoice >> siguiente_tarea