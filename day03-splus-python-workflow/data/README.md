# Datos — Día 3 (no versionados)

Catálogo e imágenes de S-PLUS traídos con `splusdata`. Binarios grandes → fuera de git.

## Proveniencia (plantilla)
```python
import splusdata
conn = splusdata.connect()            # pide usuario/clave de splus.cloud

# Consulta de catálogo (ADQL contra la base de S-PLUS):
query = """
SELECT TOP 1000 ...
FROM idr6...
WHERE ...
"""
tab = conn.query(query)

# Imagen (stamp) de un objeto:
img = conn.stamp(ra=<RA>, dec=<DEC>, size=<pix>, band='R')
```
Completar con la consulta y los parámetros reales usados en clase.

## Credenciales
NUNCA subir usuario/clave. Usar variables de entorno o un archivo ignorado (`.splus_credentials`).
