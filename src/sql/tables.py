import os
import sqlite3
from typing import Optional

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "appdata",
)
db_path = os.path.join(data_path, "prod_info.db")


def get_connection(readonly: bool = False) -> sqlite3.Connection:
    """Return a SQLite connection to the app database.

    If readonly is True, open database in immutable mode when possible.
    Ensures foreign_keys PRAGMA is enabled for every connection.
    """
    os.makedirs(data_path, exist_ok=True)
    if readonly:
        uri = f"file:{db_path}?mode=ro"
        conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    else:
        conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def initialize_schema(conn: Optional[sqlite3.Connection] = None) -> None:
    """Create database schema if it does not already exist."""
    owns_connection = False
    if conn is None:
        conn = get_connection()
        owns_connection = True

    try:
        cursor = conn.cursor()

        # Entities
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
                cod_cli TEXT PRIMARY KEY,
                name TEXT,
                city TEXT,
                country TEXT,
                phone TEXT,
                email TEXT
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                cod_sup TEXT PRIMARY KEY,
                name TEXT,
                city TEXT,
                country TEXT,
                phone TEXT,
                email TEXT
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS materials (
                id TEXT PRIMARY KEY,
                description TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                unit_price REAL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                description TEXT,
                quantity INTEGER NOT NULL DEFAULT 0,
                selling_price REAL
            );
            """
        )

        # Bill of Materials (BOM): N-N between products and materials
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS product_materials (
                product_id TEXT,
                material_id TEXT,
                quantity_per_unit REAL,
                PRIMARY KEY (product_id, material_id),
                FOREIGN KEY (product_id) REFERENCES products(id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (material_id) REFERENCES materials(id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
            """
        )

        # Movements
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movements_in (
                movement_nr INTEGER PRIMARY KEY AUTOINCREMENT,
                material_id TEXT,
                quantity INTEGER,
                total_price REAL,
                cod_sup TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (material_id) REFERENCES materials(id)
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY (cod_sup) REFERENCES suppliers(cod_sup)
                    ON UPDATE CASCADE ON DELETE SET NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movements_out (
                movement_nr INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                quantity INTEGER,
                total_price REAL,
                cod_cli TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (product_id) REFERENCES products(id)
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY (cod_cli) REFERENCES clients(cod_cli)
                    ON UPDATE CASCADE ON DELETE SET NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS production (
                production_nr INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id TEXT,
                quantity_produced INTEGER,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (product_id) REFERENCES products(id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
            """
        )

        # Indexes for common lookups
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_materials_description ON materials(description);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_products_description ON products(description);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_mov_in_material ON movements_in(material_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_mov_out_product ON movements_out(product_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_pm_product ON product_materials(product_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_pm_material ON product_materials(material_id);"
        )

        conn.commit()
    finally:
        if owns_connection and conn is not None:
            conn.close()


# Initialize schema on module import to ensure tables exist for the app
initialize_schema()
