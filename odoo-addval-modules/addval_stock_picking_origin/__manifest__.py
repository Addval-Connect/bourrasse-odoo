{
    "name": "addval_stock_picking_origin",
    "summary": "Vincula expediciones con sus pedidos de venta.",
    "description": """
        Módulo de Odoo v15.0 que muestra el campo sale_id (Many2one) que apunta
        al pedido de venta mencionado en el campo origin (Text) en el modelo
        stock.picking, para vincular cada expedición con su respectivo pedido
        de venta (de existir).
    """,
    "author": "Addval Connect",
    "website": "https://addval.cl",
    "category": "Warehouse Management",
    "version": "15.0.1",
    "license": "Other proprietary",
    "depends": ["base", "stock", "sale", "sale_management"],
    "data": [
        # "views/stock_picking.xml",
        # "views/sale_order.xml"
    ],
    "license": "Other proprietary",
    "application": True,
    "maintainer": "Ángel Ramírez Isea <angel.ramirez.isea@yandex.com>",
}
