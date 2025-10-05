# 📚 CampusLands ERP – Sistema de Gestión Académica  

Este proyecto es un **sistema ERP académico en Python** diseñado para la gestión de **campers, trainers y coordinadores** en un entorno educativo. Su objetivo es **automatizar procesos clave** dentro de CampusLands, garantizando un flujo de información centralizado, confiable y fácil de usar.  

## 🎯 Características principales  

- **Gestión de usuarios**: Registro y administración de campers, trainers y coordinadores.  
- **Rutas de aprendizaje**: Creación y organización de rutas académicas con módulos de programación, bases de datos y tecnologías backend.  
- **Matrículas**: Asignación de campers a rutas con control de capacidad, horarios y salones de entrenamiento.  
- **Notas académicas**: Registro y cálculo automático de calificaciones por módulo (teórica, práctica y quiz).  
- **Reportes dinámicos**: Listado de campers por estado, trainers asignados, módulos aprobados/reprobados y control de rutas activas.  
- **Roles diferenciados**:  
  - **Coordinador** → administración general de usuarios, rutas y asignaciones.  
  - **Trainer** → gestión de campers en sus rutas y registro de notas.  
  - **Camper** → consulta de su estado académico y resultados.  

## 🛠️ Tecnologías utilizadas  

- **Lenguaje**: Python  
- **Persistencia de datos**: Archivos JSON para almacenar información estructurada.  
- **Modular**: Programación modular para mantener un código organizado y escalable.  

## 📂 Estructura del proyecto  

Proyecto_Python_GamboaJuan/
│── data/ # Archivos JSON (campers, trainers, rutas, etc.)
│── modules/ # sistema dividido en módulos 
│ ├── coordinador.py
│ ├── trainer.py
│ ├── camper.py
│ ├── login.py
│ ├── utils.py
│ └── messages.py
│── campus.py # Punto de entrada principal
│── README.md # Documentación


## 🚀 Objetivo del proyecto  

Este proyecto busca **simular un ERP académico real** donde se gestionan procesos administrativos y académicos de forma digital, reforzando conceptos de:  

- Manejo de estructuras de datos en Python.  
- Validación y persistencia de información en JSON.  
- Separación por roles y responsabilidades en el software.  
- Uso de programación modular para escalabilidad.  

