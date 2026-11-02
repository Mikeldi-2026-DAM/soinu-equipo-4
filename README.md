# Muro de mensajes

Semana 1 de Python (2.º DAM). Una web con FastAPI y Jinja2 donde se escribe un nombre y un mensaje y todos los mensajes
salen en la portada.

> Rellena este README a lo largo de la semana: qué hace el muro, cómo se arranca, qué has ampliado y quién puede borrar.
SOINU EQUIPO 4

## Cómo se arranca

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre <http://127.0.0.1:8000/> y, para probar la API, <http://127.0.0.1:8000/docs>.

## Qué he ampliado

(Bloque 5.)


## Seccion entradas

Datos de cada tipo

-Abono general: id, nombre, descripcion, precio, fecha inicio, fecha fin, zonas de acceso, estado
-Day Pass: id, nombre, descripcion, precio, fecha_validez, zonas de acceso, estado
-Vip: id, nombre, descripcion, precio, fecha inicio, fecha fin, zonas de acceso, estado
-Abono + parcela: id, nombre, descripcion, precio, fecha inicio, fecha fin, zonas de acceso, estado


Datos de cada compra

-Compra: codigo, nombre_entrada, fecha, cantidad total de entradas, total a pagar, nombre, apellido, correo, fecha_compra


Reglas

-Minimo 1 entrada y maximo 6 entradas por compra
-Si un usuario pide mas entradas que plazas libres no se procesa la compra
-si se agotan las plazas de una entrada el estado cambia a agotado
-se valida la estrucutra de los correos para rechazar dominios inválidos
-aplicar siempre .trim().toLowerCase() antes de validar y guardar, eliminando espacios en blanco accidentales que el usuario haya colado al copiar y pegar.
-el total lo calcula el servidor, no con el precio que lelga del formulario
-en los formularios de compra
