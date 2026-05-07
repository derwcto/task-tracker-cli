# Task Tracker CLI

Una herramienta sencilla de línea de comandos para gestionar tareas, construida en Python sin dependencias externas.

## Características
- Agregar, actualizar y eliminar tareas.
- Cambiar el estado a `in-progress` o `done`.
- Filtrar tareas por estado.
- Almacenamiento persistente en JSON.

## Cómo usar
1. **Agregar:** `python task_cli.py add "Mi tarea"`
2. **Listar:** `python task_cli.py list`
3. **Marcar como hecha:** `python task_cli.py mark-done [ID]`