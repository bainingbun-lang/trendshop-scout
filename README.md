# trendshop-scout

Cruza tu lista de productos (costo y precio) con las tendencias de Google Trends y te dice cuáles coinciden y cuál es el margen. Python sin dependencias.

## Uso

Tu CSV necesita las columnas `name`, `cost` y `price`:

```csv
name,cost,price
Mini proyector portátil,40,79
Lámpara LED de escritorio,8,22
```

```bash
python3 scout.py products.csv --geo MX
```

Los productos con tendencia aparecen primero y dentro de cada grupo se ordenan por margen.

## Cómo funciona

Toma el feed RSS público de tendencias diarias de Google Trends y busca coincidencias de palabras (de más de 3 letras) entre el nombre del producto y los términos en tendencia.

## Limitaciones

- Una coincidencia con tendencia no garantiza ventas.
- Solo mira las tendencias del día, no histórico.
- No consulta marketplaces ni tiendas. Esas fuentes van contra sus términos de uso.
