# 🧵 Simulador de Procesos con Hilos y Algoritmo de la Panadería (Bakery Algorithm)

---

## 📘 Descripción

Este proyecto implementa un **simulador de procesos concurrentes en Python**, utilizando:

- **Hilos (`threading`)**
- **Bloques PCB (Process Control Block)**
- **Colas de estado**
- **Algoritmo de la Panadería (Bakery Algorithm)** para exclusión mutua sin locks tradicionales.

El programa simula un **sistema operativo básico** donde cada proceso se ejecuta en un 
**hilo independiente**, mostrando en consola cada transición de estado en tiempo real.

También incluye:

- Monitor de estado del sistema.
- Reinicio completo del entorno.
- Menú interactivo.
- Colores ANSI para visualizar claramente los cambios.
- Modo con retardos para apreciar todas las transiciones.

---

## ⚙️ Características Principales

### 🔹 **Hilos independientes por proceso**

> Cada proceso se ejecuta en un `thread` separado, simulando un scheduler real.

### 🔹 **Algoritmo de la Panadería**

> Garantiza exclusión mutua estricta sin usar dependencias externas:

- Manejo seguro de la sección crítica.
- Orden justo en la adquisición del turno.
- Evita condiciones de carrera.

### 🔹 **Transiciones de estado tipo SO real**

> Los procesos muestran:

- **NEW → READY**  
- **READY → RUNNING**  
- **RUNNING → TERMINATED**  

> Con pausas entre estados para una visualización clara.

### 🔹 **Opciones del menú**

1. Simular nuevos procesos (cada uno en un hilo independiente).  
2. Mostrar estado del sistema (en un hilo separado).  
3. Reiniciar el sistema por completo (en un hilo separado).  
4. Salir del programa.

### 🔹 **Sistema de Colas**

- `READY QUEUE`
- `TERMINATED QUEUE`
- `RUNNING THREADS`

### 🔹 **Colores en consola**

> Logs y transiciones diferenciadas con colores ANSI.

---

## 🚀 Ejecución del Proyecto

### **Requisitos**

- Python 3.10 o superior
- No requiere dependencias externas
- Sistema compatible con colores ANSI (Linux/macOS)  
  *(funciona en Windows con PowerShell moderno)*

### **Pasos**

1. Clona el repositorio:

```bash
git clone https://github.com/Cristianco9/univalle-taller-3-so.git
```

2. Entra al directorio del proyecto:

```bash
cd univalle-taller-3-so
```

3. Ejecuta el programa:

```bash
python3 src/main.py
```

---

## 🧠 Algoritmo de la Panadería

El Bakery Algorithm de Lamport es un mecanismo clásico para exclusión mutua que 
simula una panadería donde cada proceso toma un número y espera su turno.

**Ventajas**

- No requiere primitivas de sincronización del sistema operativo.

- Proporciona orden FIFO justo.

- Evita condiciones de carrera.

- Correcto incluso en sistemas distribuidos.

- Uso en el proyecto

**Se emplea para:**

- Controlar la transición de estados.

- Proteger estructuras globales:

    - READY QUEUE

    - TERMINATED LIST

    - RUNNING THREADS

---

## 📊 Ejemplo de salida real

```csharp
MULTI THREAD SIMULATION - BAKERY ALGORITHM

[PCB] 1: NEW -> READY
[PCB] 2: NEW -> READY
[PCB] 3: NEW -> READY

Process executing in independent threads.
Waiting for them to finish...

[DEBUG] PID 1 executing in Thread Thread-1
[PCB] 1: READY -> RUNNING

[DEBUG] PID 2 executing in Thread Thread-2
[PCB] 2: READY -> RUNNING

[DEBUG] PID 3 executing in Thread Thread-3
[PCB] 3: READY -> RUNNING

[PCB] 1: RUNNING -> TERMINATED
[DEBUG] PID 1 finish execution.

[PCB] 2: RUNNING -> TERMINATED
[DEBUG] PID 2 finish execution.

[PCB] 3: RUNNING -> TERMINATED
[DEBUG] PID 3 finish execution.

All process have been finished.
Press ENTER to return...
```

--- 

## 🧩 Arquitectura del Sistema

#### Clases Principales

**🔸 Process**

> Representa un PCB con:

- PID

- Estado

- Burst time

- Prioridad

- Hilo asociado

- Bakery ID


**🔸 System**

> Administra:

- Ready queue

- Terminated list

- Running threads

- Asignación de PID

- IDs para Bakery Algorithm

**🔸 Scheduler**

> Ejecuta los procesos en hilos independientes.

---

## 📚 Temas aplicados

- Programación concurrente con hilos.

- Exclusión mutua sin locks utilizando Bakery Algorithm.

- Simulación de sistemas operativos.

- PCB, colas de procesos y estados.

- Visualización clara de estados con colores ANSI.

- Diseño modular para sistemas multi-hilo.

---

## 👨‍💻 Autor

**Cristian Camilo Cortes Ortiz**

Desarrollador de Software

202478542

