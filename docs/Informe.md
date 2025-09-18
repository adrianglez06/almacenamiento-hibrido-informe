# Informe Técnico de Negocio y Tecnología sobre Soluciones de Almacenamiento

## Resumen Ejecutivo
El objetivo es balancear coste, rendimiento y escalabilidad bajo restricciones de latencia y cumplimiento. HDD ofrece buen coste por capacidad con rendimiento medio; SSD maximiza velocidad con mayor coste; cinta minimiza coste para archivo a largo plazo con latencia elevada; la nube aporta elasticidad y OPEX predecible a cambio de dependencia de red/proveedor. [Inference] Ninguna tecnología cubre todo; la solución es híbrida: SSD on-prem para cargas críticas, HDD como segunda capa activa, cinta para archivo, nube para elasticidad y DR. Métricas de éxito: SLA de latencia, coste total anual, RPO/RTO, y cumplimiento GDPR.

---

## 1. Descripción del escenario
- Necesidades: datos estructurados/no estructurados, baja latencia para OLTP, capacidad de archivo y analítica periódica.
- Restricciones: latencia <10 ms para críticos [Inference], presupuesto CAPEX limitado, OPEX controlado, GDPR (residencia UE).
- Cargas: OLTP, BI batch, backups y archivo.
- Crecimiento esperado: **[Inference]** volumen inicial 100 TB, crecimiento anual 20 %.
- Supuestos clave: valores de rendimiento y coste son promedios de mercado; donde no hay fuente directa se indica **[Unverified]**.

---

## 2. Criterios de evaluación
- Velocidad (MB/s): lectura/escritura. Impacto directo en SLA y productividad.
- Capacidad (TB): volumen utilizable. Impacto en continuidad y expansión.
- Costo por GB (USD): afecta CAPEX/OPEX y TCO.
- Fiabilidad (MTBF, horas): riesgo operativo y de pérdida de datos.
- Consumo (W): OPEX energético y densidad.
- Seguridad (1–5): cifrado, control de acceso, logging, cumplimiento.
- Escalabilidad (1–5): facilidad para crecer horizontal/vertical y elasticidad.
Medición: pruebas sintéticas y especificaciones de proveedor. Impacto: SLA, TCO, riesgo de incumplimiento.

---

## 3. Comparación de tecnologías (tabla)
> Fuente de valores: `data/supuestos.csv`. Etiquetas de veracidad:
> - MTBF HDD/SSD/cinta: **[Unverified]** como promedios de referencia.
> - Rendimiento nube e incluso “MTBF” nube: **[Inference]/[Unverified]**; la nube no expone MTBF por volumen, sino SLA por servicio.

| Tecnología | Lectura (MB/s) | Escritura (MB/s) | Capacidad (TB) | Costo/GB (USD) | Fiabilidad (MTBF h) | Consumo (W) | Seguridad (1–5) | Escalabilidad (1–5) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HDD | 200 | 170 | 20 | 0.035 | 1,200,000 [Unverified] | 8 | 3 | 3 |
| SSD | 2,500 | 1,800 | 8 | 0.15 | 1,500,000 [Unverified] | 4 | 4 | 3 |
| Cinta | 250 | 200 | 30 | 0.008 | 2,000,000 [Unverified] | 7 | 2 | 2 |
| Nube | 300 [Unverified] | 250 [Unverified] | ~ilimitada | 0.025 [Unverified] | N/A | N/A | 5 | 5 |

**Lectura ejecutiva.** SSD domina en rendimiento a mayor coste; HDD equilibra coste/capacidad; cinta optimiza archivo frío; la nube aporta elasticidad y servicios gestionados con dependencia de conectividad y política de proveedor.

---

## 4. Análisis gráfico comparativo (especificación)
- Barras 1: velocidades de lectura por tecnología.
- Barras 2: velocidades de escritura por tecnología.
- Barras 3: coste por GB por tecnología.
- Radar: fiabilidad (MTBF normalizada 1–5), escalabilidad (1–5) y seguridad (1–5).
Normalización MTBF a escala 1–5: asignar 1 al mínimo MTBF observado y 5 al máximo; interpolar linealmente los intermedios. La nube no se incluye en MTBF y se omite o se marca como N/A en el radar para Fiabilidad.

Implementación: **matplotlib**, un gráfico por figura, sin fijar colores.

---

## 5. Simulación de rendimiento (especificación)
- Parámetros: volumen inicial (TB), crecimiento anual (%), horizonte (años).
- Cálculo: `volumen_n = V0 * (1 + g)^n`.
- Tiempo aproximado por tecnología en horas: `tiempo = (volumen_TB * 1e6 MB/TB) / (lectura_MB_s) / 3600`. **[Inference]** Se usa velocidad de lectura como proxy y operación secuencial sin paralelismo ni caché.
- Salida: tabla con columnas `Año, Volumen (TB), Tiempo HDD (h), Tiempo SSD (h), Tiempo Cinta (h), Tiempo Nube (h)`.
- Limitaciones: ignora paralelismo, colas de IO, compresión, caché, y efectos de red en nube; resultados orientativos.

**Interpretación ejecutiva:** a partir de 3–5 años, los tiempos con HDD/cinta crecen y comprometen SLA para cargas intensivas; SSD mantiene tiempos bajos pero encarece el TCO si se usa como única capa; la nube absorbe picos con latencia dependiente de red.

---

## 6. Guía/diagrama de arquitectura propuesta (texto)
Patrón híbrido recomendado:
- Ingesta y OLTP: SSD on-prem para baja latencia; RAID10 o RAID1 según perfil de riesgo.
- Capa activa: HDD on-prem (RAID6 o erasure coding en SDS) para datasets grandes.
- Archivo: cinta LTO para >12 meses y retención legal.
- Elasticidad y DR: nube para picos y recuperación ante desastres con replicación cruzada y almacenamiento de backups críticos.
Flujo de datos: ingesta → transaccional → replicación a HDD → ETL/analítica → backups a nube/cinta.
RPO/RTO: definir objetivos por servicio; pruebas de DR semestrales.
Seguridad: cifrado at-rest y in-transit, IAM mínimo privilegio, MFA, logs inmutables.
Cumplimiento: residencia UE para datos personales, DPA con proveedor cloud.

Herramientas de diagrama: draw.io, Lucidchart, Visio.

---

## 7. Riesgos, mitigaciones y oportunidades
- Riesgos: CAPEX SSD alto; desgaste SSD en escrituras intensivas; dependencia de conectividad y lock-in cloud; cumplimiento transfronterizo.
- Mitigaciones: arquitectura híbrida; over-provisioning y monitoreo de TBW; multizona/multicloud y dos ISP; cifrado E2E y políticas de residencia.
- Oportunidades: elasticidad y pago por uso; OPEX reducido con cinta en archivo; mejora de tiempos con SSD; continuidad de negocio y menor RTO.

---

## 8. Conclusiones y recomendación
Recomendación: solución híbrida con SSD para críticos, HDD como capa activa, cinta para archivo y nube para elasticidad y DR. Próximos pasos: PoC, validación de costes reales con proveedores, pruebas de carga, plan de migración por fases y métricas de éxito (SLA, TCO, RPO/RTO).

---

## 9. Apéndices
- Glosario: RPO, RTO, MTBF.
- Supuestos numéricos: ver `data/supuestos.csv` y notas **[Inference]/[Unverified]** en esta sección.
- Referencias (APA7):
  - Amazon Web Services. (2024). Storage services overview. https://aws.amazon.com/products/storage/ [Unverified]
  - IBM. (2023). Tape storage for long-term data retention. https://www.ibm.com [Unverified]
  - Seagate. (2023). Enterprise HDD specifications. https://www.seagate.com [Unverified]
  - IDC. (2023). Worldwide storage forecast. IDC Research. [Unverified]
