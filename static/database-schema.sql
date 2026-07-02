CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  usuario TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  rol TEXT NOT NULL CHECK (rol IN ('admin', 'operador')),
  activo INTEGER NOT NULL DEFAULT 1,
  creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  telefono TEXT NOT NULL,
  direccion TEXT,
  notas TEXT,
  creado_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  categoria TEXT NOT NULL,
  descripcion TEXT,
  precio_base REAL NOT NULL DEFAULT 0,
  imagen TEXT,
  activo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE inventario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  producto_id INTEGER NOT NULL,
  stock REAL NOT NULL DEFAULT 0,
  unidad TEXT NOT NULL DEFAULT 'und',
  stock_minimo REAL NOT NULL DEFAULT 0,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE pedidos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  codigo_rastreo TEXT NOT NULL UNIQUE,
  cliente_id INTEGER NOT NULL,
  tipo_trabajo TEXT NOT NULL CHECK (tipo_trabajo IN ('venta', 'reparacion', 'confeccion', 'instalacion')),
  descripcion TEXT NOT NULL,
  estado TEXT NOT NULL CHECK (estado IN ('recibido', 'en_proceso', 'listo', 'entregado', 'cancelado')),
  total REAL NOT NULL DEFAULT 0,
  adelanto REAL NOT NULL DEFAULT 0,
  saldo REAL NOT NULL DEFAULT 0,
  fecha_ingreso TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_entrega_estimada TEXT,
  notas TEXT,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE pedido_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  producto_id INTEGER,
  descripcion TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 1,
  precio_unitario REAL NOT NULL DEFAULT 0,
  subtotal REAL NOT NULL DEFAULT 0,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE pagos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  monto REAL NOT NULL,
  metodo TEXT NOT NULL CHECK (metodo IN ('efectivo', 'yape', 'transferencia', 'otro')),
  fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nota TEXT,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

CREATE TABLE movimientos_inventario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  producto_id INTEGER NOT NULL,
  tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'salida', 'ajuste')),
  cantidad REAL NOT NULL,
  motivo TEXT NOT NULL,
  pedido_id INTEGER,
  fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id),
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

CREATE TABLE tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pedido_id INTEGER NOT NULL,
  numero_ticket TEXT NOT NULL UNIQUE,
  contenido TEXT NOT NULL,
  impreso INTEGER NOT NULL DEFAULT 0,
  fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
