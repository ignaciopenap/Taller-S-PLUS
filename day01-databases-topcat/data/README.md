# Datos — Día 1 (no versionados)

## Consulta principal (SDSS, Stripe 82) vía TAPVizieR / ADQL
```sql
SELECT TOP 30000
  RA_ICRS, DE_ICRS,
  "uPmag", "gPmag", "rPmag", "iPmag", "zPmag",
  "e_uPmag", "e_gPmag", "e_rPmag", "e_iPmag", "e_zPmag",
  zsp, e_zsp, spCl
FROM "V/154/sdss16"
WHERE RA_ICRS BETWEEN 320 AND 340
  AND DE_ICRS BETWEEN -1.25 AND 1.25
  AND spCl = 'GALAXY'
  AND zsp > 0.02 AND zsp < 0.2
  AND f_zsp = 0 AND mode = 1 AND clean = 1
```
Resultado esperado: **7539 filas, 15 columnas**.

## Respaldo
`sdss_stripe82_galaxies.vot` del repo del tutorial (mismo resultado que la consulta).
Descargar de: https://github.com/GMontaguth/Virtual_observatoy_class
