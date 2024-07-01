from flask import Blueprint

crafting = Blueprint('crafting', __name__, url_prefix='/crafting/v1')


@crafting.route('/craftSell', methods=['POST'])
def craft_sell():
    return {
        "sparksGained": 0
    }


@crafting.route('/craftBuy', methods=['POST'])
def craft_buy():
    return {
        "sparksSpent": 0
    }
