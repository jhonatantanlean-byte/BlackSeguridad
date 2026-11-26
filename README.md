# Sistema Black Seguridad

## Descripción del proyecto

Sistema de gestión y asignación de turnos de vigilancia desarrollado en Python para el curso de Fundamentos de Programación de la Universidad Privada del Norte.

## Funcionalidades principales

- Registro de agentes de seguridad con generación automática de códigos.
- Validación de datos personales y mayoría de edad.
- Registro de puestos de vigilancia.
- Creación de turnos diurnos y nocturnos.
- Asignación de agentes con detección de conflictos horarios.
- Consulta de turnos pendientes de cobertura.
- Búsqueda de agentes por nombres o apellidos.
- Conteo recursivo de turnos sin asignar.
- Almacenamiento y recuperación de información mediante JSON.

## Ejecución

El programa requiere Python 3.

Para iniciarlo, ejecutar:

`python main.py`

## Organización del proyecto

- `main.py`: menú principal.
- `registro.py`: registro y validación de información.
- `turnos.py`: creación y asignación de turnos.
- `datos.py`: consultas y persistencia de información.

## Control de versiones

Proyecto gestionado mediante Git y GitHub, utilizando ramas para el desarrollo y revisión de mejoras.
