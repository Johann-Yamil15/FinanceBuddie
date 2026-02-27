# Finance Buddie 💰

Aplicación web para el control de gastos y finanzas personales, construida con Python (Django) y SQL Server.

## 🚀 Características Principales

* **Dashboard Financiero:** Visualización de balance total, ingresos y gastos.
* **Gestión de Transacciones:** Registro de nuevos ingresos y gastos categorizados.
* **Filtros Dinámicos:** Visualización del historial de movimientos filtrado por periodos y tipos.
* **Arquitectura:** Modelos de datos manuales (POJOs/DTOs) conectados mediante procedimientos/consultas directas a SQL Server.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django
* **Base de Datos:** Microsoft SQL Server
* **Conector DB:** `pymssql` / `mssql-django`
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Iconos de Lucide

## comandos

* **Comando para ejecutar:** python manage.py runserver

## ⚙️ Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:
* Python 3.10+
* Microsoft SQL Server (Local o en la nube)
* ODBC Driver 17 for SQL Server (o superior)

## 🗄️ Script de Base de Datos

Para levantar el entorno de desarrollo, ejecuta el siguiente script en SQL Server Management Studio (SSMS) o Azure Data Studio. Este script crea la base de datos, las tablas y añade datos de prueba:

```sql
-- 1. Crear la base de datos
CREATE DATABASE FinanceBuddie;
GO

-- 2. Usar la base de datos
USE FinanceBuddie;
GO

-- 3. Crear tabla de Usuarios
CREATE TABLE Usuarios (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    ApellidoP VARCHAR(100) NOT NULL,
    ApellidoM VARCHAR(100) NULL,
    Email VARCHAR(150) UNIQUE NOT NULL,
    FechaNacimiento DATE NULL,
    PasswordHash VARCHAR(255) NOT NULL
);
GO

-- 4. Crear tabla de Categorías
CREATE TABLE Categorias (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL UNIQUE
);
GO

-- 5. Crear tabla de Transacciones
CREATE TABLE Transacciones (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioId INT NOT NULL,
    CategoriaId INT NOT NULL,
    Tipo VARCHAR(20) NOT NULL CHECK (Tipo IN ('ingreso', 'gasto')),
    Monto DECIMAL(18,2) NOT NULL,
    Fecha DATETIME DEFAULT GETDATE(),
    
    -- Llaves foráneas
    CONSTRAINT FK_Transaccion_Usuario FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Transaccion_Categoria FOREIGN KEY (CategoriaId) REFERENCES Categorias(Id)
);
GO

-- ==========================================
-- TABLA PARA METAS DE AHORRO
-- ==========================================
CREATE TABLE MetasAhorro (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioId INT NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    MontoObjetivo DECIMAL(18,2) NOT NULL,
    MontoActual DECIMAL(18,2) DEFAULT 0.00,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    
    -- Opcional: Si ya tienes una tabla de Usuarios, puedes descomentar la siguiente línea
    CONSTRAINT FK_Metas_Usuarios FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
);
GO

-- ==========================================
-- TABLA PARA EL HISTORIAL DEL CHAT (IA)
-- ==========================================
CREATE TABLE ChatMensajes (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioId INT NOT NULL,
    Remitente NVARCHAR(20) NOT NULL, -- Guardará 'usuario' o 'ia'
    Mensaje NVARCHAR(MAX) NOT NULL,  -- NVARCHAR(MAX) porque las respuestas de IA pueden ser largas
    Fecha DATETIME DEFAULT GETDATE(),
    
    -- Opcional: Si ya tienes una tabla de Usuarios, puedes descomentar la siguiente línea
    CONSTRAINT FK_Chat_Usuarios FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
);
GO

-- ==========================================
-- DATOS DE PRUEBA
-- ==========================================

INSERT INTO Categorias (Nombre) VALUES 
('Comida'), ('Compras'), ('Entretenimiento'), ('Transporte'), 
('Servicios'), ('Salud'), ('Educación'), ('Honorarios');
GO

INSERT INTO Usuarios (Nombre, ApellidoP, ApellidoM, Email, FechaNacimiento, PasswordHash) 
VALUES ('Johann', 'Yamil', 'Pérez', 'johann@correo.com', '1995-05-20', 'hash_falso_123');
GO

INSERT INTO Transacciones (UsuarioId, CategoriaId, Tipo, Monto) VALUES 
(1, 8, 'ingreso', 2400.00),
(1, 2, 'gasto', 85.00),
(1, 1, 'gasto', 15.00);
GO