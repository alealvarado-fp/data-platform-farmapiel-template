"""
Copyright (c) 2026 [Centro Internacional de Cosmiatría / Farmapiel(c) ]
Autor: Equipo de Sistemas (Basado en Estándar de Resiliencia)
Descripción: Ejemplo de carga incremental idempotente SAP -> BigQuery
"""
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime

# ESTÁNDAR: El nombre del DAG debe incluir el dominio
with DAG(dag_id='comercial_sap_oinv_to_bronze', 
         start_date=datetime(2026, 1, 1), 
         schedule_interval='@daily',
         catchup=False) as dag:

    # USAMOS MERGE EN LUGAR DE INSERT PARA EVITAR DUPLICADOS (IDEMPOTENCIA)
    load_fact_invoice = BigQueryInsertJobOperator(
        task_id='merge_invoices_sap',
        configuration={
            "query": {
                "query": """
                    MERGE `proyecto.dm_comercial.fact_ventas` T
                    USING `proyecto.stg_sap.oinv_external` S
                    ON T.DocEntry = S.DocEntry
                    WHEN MATCHED THEN
                      UPDATE SET T.DocTotal = S.DocTotal, T.UpdateTime = CURRENT_TIMESTAMP()
                    WHEN NOT MATCHED THEN
                      INSERT (DocEntry, DocDate, CardCode, DocTotal) 
                      VALUES (S.DocEntry, S.DocDate, S.CardCode, S.DocTotal)
                """,
                "useLegacySql": False,
            }
        }
    )