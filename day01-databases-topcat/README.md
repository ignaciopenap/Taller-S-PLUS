# Día 1 — Bases de datos astronómicas y TOPCAT

**Lunes 20/07** · Mendes de Oliveira · Demarco · Montaguth

## Objetivos
- Manejar SIMBAD, VizieR, Aladin, ds9 y TOPCAT.
- Consultar un servicio TAP con ADQL; hacer crossmatch local y con CDS.
- Construir submuestras, graficar, y desarrollar el "hábito de sospecha" sobre los datos.

## Qué hice
<completar: consultas que corrí, muestra que armé, gráficos, hallazgos>

## Conceptos clave
VO, TAP, ADQL, VOTable, UCD, cone search, crossmatch. Ver `../reference/glossary.md`.
PSF vs Petrosian vs model. Bimodalidad: secuencia roja / nube azul / green valley.

## Cómo reproducir
1. Abrir TOPCAT (`java -jar topcat-full.jar`).
2. `VO → TAP Query` → TAPVizieR → la consulta ADQL en `data/README.md`.
3. Si el servidor va lento, cargar el `.vot` de respaldo (ver `data/`).

## Dudas / pendientes
<completar>

## Referencias
Tutorial: https://github.com/GMontaguth/Virtual_observatoy_class · Hogg (2000) · Chilingarian (2010) · Lintott et al. (2011).
