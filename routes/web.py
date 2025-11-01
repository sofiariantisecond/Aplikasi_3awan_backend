from flask import Blueprint
from controllers.menu_controller import get_all_menu, add_menu, update_menu, delete_menu
from controllers.category_controller import get_all_category, add_category, update_category, delete_category
from controllers.cart_controller import get_all_cart, add_cart, update_cart, delete_cart
from controllers.order_detail_controller import get_all_order_detail, add_order_detail, update_order_detail, delete_order_detail
from controllers.order_controller import get_all_orders, add_order, update_order, delete_order
from controllers.user_controller import get_all_users, add_user, update_user, delete_user
from controllers.payments_controller import get_all_payments, add_payment, update_payment, delete_payment

web = Blueprint("web", __name__)
# Endpoint API
web.route("/", methods=["GET"])(get_all_menu)
web.route("/menu/insert", methods=["POST"])(add_menu)
web.route("/menu/update/<int:id_menu>", methods=["PUT"])(update_menu)
web.route("/menu/delete/<int:id_menu>", methods=["DELETE"])(delete_menu)

web.route("/category", methods=["GET"])(get_all_category)
web.route("/category/insert", methods=["POST"])(add_category)
web.route("/category/update/<int:id_category>", methods=["PUT"])(update_category)
web.route("/category/delete/<int:id_category>", methods=["DELETE"])(delete_category)

web.route("/cart", methods=["GET"])(get_all_cart)
web.route("/cart/insert", methods=["POST"])(add_cart)
web.route("/cart/update/<int:id_cart>", methods=["PUT"])(update_cart)
web.route("/cart/delete/<int:id_cart>", methods=["DELETE"])(delete_cart)

web.route("/order_details", methods=["GET"])(get_all_order_detail)
web.route("/order_details/insert", methods=["POST"])(add_order_detail)
web.route("/order_details/update/<int:id_detail>", methods=["PUT"])(update_order_detail)
web.route("/order_details/delete/<int:id_detail>", methods=["DELETE"])(delete_order_detail)

web.route("/orders", methods=["GET"])(get_all_orders)
web.route("/orders/insert", methods=["POST"])(add_order)
web.route("/orders/update/<int:id_order>", methods=["PUT"])(update_order)
web.route("/orders/delete/<int:id_order>", methods=["DELETE"])(delete_order)

web.route("/users", methods=["GET"])(get_all_users)
web.route("/users/insert", methods=["POST"])(add_user)
web.route("/users/update/<int:id_user>", methods=["PUT"])(update_user)
web.route("/users/delete/<int:id_user>", methods=["DELETE"])(delete_user)

web.route("/payments", methods=["GET"])(get_all_payments)
web.route("/payments/insert", methods=["POST"])(add_payment)
web.route("/payments/update/<int:id_payment>", methods=["PUT"])(update_payment)
web.route("/payments/delete/<int:id_payment>", methods=["DELETE"])(delete_payment)