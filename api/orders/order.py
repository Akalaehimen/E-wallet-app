from flask.views import MethodView
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_smorest import Blueprint, abort
from utils import db
from flask import request, jsonify
from api.models.order import OrderModel
from api.models.data import DataModel
from api.models.cable import CableModel
from api.models.elect import ElectModel
from api.models.cryptos import CryptosModel
from api.models.crypto import CryptoModel
from schema import AirtimeSchema
from schema import DataSchema
from schema import CableSchema
from schema import CryptoSchema
from schema import ElectricitySchema
from datetime import datetime
import random
import string


blp = Blueprint("Orders", "orders", description="Operations on Orders")

# Place an order for airtime


@blp.route('/airtime/purchase', methods=['POST'])
@blp.arguments(AirtimeSchema)
@jwt_required()
def purchase_airtime(self):
    data = request.json

    phone_number = data.get('phone_number')
    amount = data.get('amount')

    # Check phone number length and network provider
    network_provider = get_network_provider(phone_number)
    if not network_provider:
        return jsonify({'message': 'Invalid phone number'}), 400

    # Check amount
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'message': 'Invalid amount'}), 400
    if amount <= 99.9:
        return jsonify({'message': 'Amount must be greater than hundred'}), 400

    # Check if phone number has made any previous purchases
    recent_orders = OrderModel.query.filter_by(
        phone_number=phone_number).order_by(
        OrderModel.created_at.desc()).limit(1).all()
    if recent_orders:
        last_order = recent_orders[0]
        time_since_last_order = datetime.utcnow() - last_order.created_at
        if time_since_last_order.total_seconds() < 60:
            return jsonify(
                {'message': 'Please wait for a minute before making another purchase'}), 400

    # Generate order ID
    order_id = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for _ in range(6))

    # Process airtime purchase (not implemented)
    new_order = OrderModel(
        amount=amount,
        phone_number=phone_number,
        order_id=order_id)
    db.session.add(new_order)
    db.session.commit()

    # Process airtime purchase (not implemented)
    return jsonify(
        {'message': 'Airtime purchased successfully', 'order_id': order_id}), 200


def get_network_provider(phone_number):
    if len(phone_number) != 11:
        return None
    prefix = phone_number[:4]
    if prefix in (
        '0802',
        '0808',
        '0701',
        '0708',
        '0812',
        '0902',
        '0907',
            '0912'):
        return 'Airtel'
    elif prefix in ('0809', '0817', '0818', '0909', '0908'):
        return '9mobile'
    elif prefix in ('0805', '0705', '0905', '0807', '0811', '0815'):
        return 'Glo'
    elif prefix in ('080', '081', '090', '0703', '0704', '0706', '0803', '0806', '07025', '07026', '07027', '07028'):
        return 'MTN'
    else:
        return None


# Purchase data plan
@blp.route('/data/purchase', methods=['POST'])
@blp.arguments(DataSchema)
@jwt_required()
def purchase_data(self):
    data = request.json

    phone_number = data.get('phone_number')
    data_plan = data.get('data_plan')

    # Check phone number length and network provider
    network_provider = get_network_provider(phone_number)
    if not network_provider:
        return jsonify({'message': 'Invalid phone number'}), 400

    # Check data plan
    data_plans = {
        'Airtel': {'1gb': 300, '2gb': 500, '3gb': 1000},
        'MTN': {'1gb': 350, '2gb': 600, '3gb': 1200},
        'Glo': {'1gb': 400, '2gb': 700, '3gb': 1300},
        '9mobile': {'1gb': 500, '2gb': 800, '3gb': 1500}
    }
    if network_provider not in data_plans:
        return jsonify({'message': 'Invalid network provider'}), 400
    if data_plan not in data_plans[network_provider]:
        return jsonify({'message': 'Invalid data plan'}), 400

    # Get data plan cost
    plan_size = data_plan.lower()
    cost = data_plans[network_provider][plan_size]

    # Generate order ID
    order_id = ''.join(
        random.choice(
            string.ascii_uppercase +
            string.digits) for _ in range(6))

    # Create order in database
    order = DataModel(
        data_plan=data_plan,
        phone_number=phone_number,
        order_id=order_id)
    db.session.add(order)
    db.session.commit()

    # Process data purchase (not implemented)
    return jsonify({'message': 'Data purchased successfully',
                   'cost': cost, 'order_id': order_id}), 200


def get_network_provider(phone_number):
    if len(phone_number) != 11:
        return None
    prefix = phone_number[:4]
    if prefix in (
        '0802',
        '0808',
        '0701',
        '0708',
        '0812',
        '0902',
        '0907',
            '0912'):
        return 'Airtel'
    elif prefix in ('0809', '0817', '0818', '0909', '0908'):
        return '9mobile'
    elif prefix in ('0805', '0705', '0905', '0807', '0811', '0815'):
        return 'Glo'
    elif prefix in ('080', '081', '090', '0703', '0704', '0706', '0803', '0806', '07025', '07026', '07027', '07028'):
        return 'MTN'
    else:
        return None


# Purchase cable tv
@blp.route('/cable/purchase', methods=['POST'])
@blp.arguments(CableSchema)
@jwt_required()
def purchase_cable(self):

    data = request.json

    subscriber_number = data.get('subscriber_number')
    package_name = data.get('package_name')

    # Check subscriber number length and cable provider
    cable_provider = get_cable_provider(subscriber_number)
    if not cable_provider:
        return jsonify({'message': 'Invalid subscriber number'}), 400

    # Check package name for the prices
    package_prices = {
        'DStv': {
            'Access': 2000,
            'Family': 4000,
            'Compact': 6800,
            'Premium': 15800},
        'GOtv': {
            'Lite': 400,
            'Value': 1250,
            'Plus': 1900,
            'Max': 3200},
        'StarTimes': {
            'Basic': 1200,
            'Classic': 2400,
            'Super': 3800}}
    if cable_provider not in package_prices:
        return jsonify({'message': 'Invalid cable provider'}), 400
    if package_name not in package_prices[cable_provider]:
        return jsonify({'message': 'Invalid package name'}), 400

    # Get package cost
    cost = package_prices[cable_provider][package_name]

    # Create order in database
    order_id = ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits,
            k=6))

    order = CableModel(
        order_id=order_id,
        subscriber_number=subscriber_number,
        package_name=package_name)
    db.session.add(order)
    db.session.commit()

    # Process cable package purchase (not implemented)
    return jsonify({'message': 'Cable package purchased successfully',
                   'cost': cost, 'order_id': order_id}), 200


def get_cable_provider(subscriber_number):
    if len(subscriber_number) != 10:
        return None
    prefix = subscriber_number[:3]
    if prefix == '401':
        return 'DStv'
    elif prefix == '403':
        return 'GOtv'
    elif prefix == '402':
        return 'StarTimes'
    else:
        return None


# Purchase electricity
@blp.route('/electricity/purchase', methods=['POST'])
@blp.arguments(ElectricitySchema)
@jwt_required()
def purchase_electricity(self):

    data = request.json

    provider = data.get('provider')
    meter_number = data.get('meter_number')
    amount = float(data.get('amount'))
    payment_mode = data.get('payment_mode')

    # Check if payment mode is valid
    if payment_mode not in ['prepaid', 'postpaid']:
        return jsonify({'message': 'Invalid payment mode.'}), 400

    # Determine the electricity provider
    if provider == 'eko':
        if payment_mode == 'prepaid':
            service_charge = 20
        else:
            service_charge = 50
    elif provider == 'ikeja':
        if payment_mode == 'prepaid':
            service_charge = 30
        else:
            service_charge = 70
    elif provider == 'abuja':
        if payment_mode == 'prepaid':
            service_charge = 25
        else:
            service_charge = 60
    else:
        return jsonify({'message': 'Invalid electricity provider.'}), 400

    # Calculate the total amount to be paid
    total_amount = amount + service_charge

    # Create order in database
    order_id = ''.join(
        random.choices(
            string.ascii_uppercase +
            string.digits,
            k=6))

    # Create a new electricity purchase order
    order = ElectModel(
        order_id=order_id,
        meter_number=meter_number,
        amount=amount,
        provider=provider,
        service_charge=service_charge,
        payment_mode=payment_mode
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Electricity purchase successful!',
                   'cost + charges': total_amount})


# Recieving cryptocurrency
@blp.route('/recievecrypto', methods=['GET'])
@jwt_required()
def get():
    # Define the characters that can appear in the random string
    characters = string.ascii_lowercase + string.digits
    # Choose the first character randomly from uppercase letters
    first_char = random.choice(string.ascii_uppercase)
    # Choose the remaining characters randomly from lowercase letters and
    # digits
    rest_chars = ''.join(random.choices(characters, k=21))
    # Concatenate the first character and the remaining characters
    random_string = first_char + rest_chars

   # Create a new instance of the Wallet model and set its address attribute
   # to the generated string
    wallet = CryptoModel(address=random_string)
   # Add the new instance to the database session and commit the changes
    db.session.add(wallet)
    db.session.commit()

    # Return a message containing the generated string
    return f"This is your wallet_address: {random_string}"


# Sending cryptocurrency
@blp.route('/cryptos', methods=['POST'])
@blp.arguments(CryptoSchema)
@jwt_required()
def generate_random_number(self):

    data = request.json

    number = data.get('number')
    if number is None:
        # Check if entered a wallet address
        return jsonify({'error': 'Please provide a wallet address.'}), 400
    else:
        # Check if the number entered is exactly 22 characters
        if len(number) != 22:
            return jsonify({'error': 'Check the wallet address.'}), 400
        # Check if the first character of the number entered is a capital
        # letter
        if not number[0].isupper():
            return jsonify({'error': 'Check the wallet address.'}), 400
    # Create a new Number object with the generated or user-entered number and
    # save it to the database
    new_number = CryptosModel(number=number)
    db.session.add(new_number)
    db.session.commit()
    return jsonify({'The user wallet addres is': number})


# Getting the history of the wallet
@blp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    airtime_orders = OrderModel.query.all()
    data_orders = DataModel.query.all()
    cable_tv_orders = CableModel.query.all()
    electricity_orders = ElectModel.query.all()

    # Combine the orders into a single list
    all_orders = airtime_orders + data_orders + cable_tv_orders + electricity_orders

    if not all_orders:
        # If no orders are found, return a 404 error response
        return jsonify({'error': 'No orders found for this user.'}), 404

    # Serialize the orders into JSON
    orders_json = [order.to_json() for order in all_orders]

    return jsonify(orders_json)
