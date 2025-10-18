from PySide6.QtSql import QSqlDatabase, QSqlQuery

from sql.tables import db_path


def create_connection() -> QSqlDatabase:
    path = db_path

    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(path)

    if not db.isOpen():
        if not db.open():
            raise RuntimeError("Failed to open database")
    return db


def recalc_product_quantities():
    """Recalculate PRODUCTS.QUANTITY as produced minus sold."""
    sql = """
        UPDATE products
        SET quantity = MAX(0,
            COALESCE((
                SELECT SUM(production.quantity_produced)
                FROM production
                WHERE production.product_id = products.id
            ), 0)
            -
            COALESCE((
                SELECT SUM(movements_out.quantity)
                FROM movements_out
                WHERE movements_out.product_id = products.id
            ), 0)
        );
    """
    query = QSqlQuery()
    if not query.exec(sql):
        print("Error recalculating product quantities:", query.lastError().text())
    else:
        print("Product quantities recalculated.")


def recalc_material_quantities():
    """Recalculate MATERIALS.QUANTITY as received minus consumed in production.

    Consumption is computed via BOM table (product_materials.quantity_per_unit)
    multiplied by produced quantities per product.
    """
    sql = """
        UPDATE materials
        SET quantity = CAST(ROUND(MAX(0,
            COALESCE((
                SELECT SUM(mi.quantity)
                FROM movements_in mi
                WHERE mi.material_id = materials.id
            ), 0)
            -
            COALESCE((
                SELECT SUM(pm.quantity_per_unit * pr.quantity_produced)
                FROM product_materials pm
                JOIN production pr ON pr.product_id = pm.product_id
                WHERE pm.material_id = materials.id
            ), 0)
        )) AS INTEGER);
    """
    query = QSqlQuery()
    if not query.exec(sql):
        print("Error recalculating material quantities:", query.lastError().text())
    else:
        print("Material quantities recalculated.")


def recalc_all_quantities():
    """Recalculate both material and product quantities in a single call."""
    # Recalculate materials first so dependent views are consistent if any
    recalc_material_quantities()
    recalc_product_quantities()


def recalc_movements_in_total_prices():
    """Recalculate movements_in.total_price = quantity * materials.unit_price (rounded 2dp)."""
    sql = """
        UPDATE movements_in
        SET total_price = ROUND(
            COALESCE((
                SELECT unit_price FROM materials m WHERE m.id = movements_in.material_id
            ), 0) * quantity, 2
        );
    """
    query = QSqlQuery()
    if not query.exec(sql):
        print("Error recalculating movements_in total_price:", query.lastError().text())
    else:
        print("movements_in total prices recalculated.")


def recalc_movements_out_total_prices():
    """Recalculate movements_out.total_price = quantity * products.selling_price (rounded 2dp)."""
    sql = """
        UPDATE movements_out
        SET total_price = ROUND(
            COALESCE((
                SELECT selling_price FROM products p WHERE p.id = movements_out.product_id
            ), 0) * quantity, 2
        );
    """
    query = QSqlQuery()
    if not query.exec(sql):
        print("Error recalculating movements_out total_price:", query.lastError().text())
    else:
        print("movements_out total prices recalculated.")


def recalc_all_totals():
    """Recalculate total_price for both movements_in and movements_out."""
    recalc_movements_in_total_prices()
    recalc_movements_out_total_prices()
