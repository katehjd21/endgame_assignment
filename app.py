from flask import Flask,render_template, request, url_for, redirect
from controllers.duties_controller import DutiesController, duties_store
from controllers.coin_controller import CoinController

app = Flask(__name__)

@app.route('/')
def landing_page():
    coins = CoinController().fetch_all_coins()
    return render_template("coins.html", coins=coins)

@app.route('/automate', methods=['GET'])
def automate_page():
    duties = DutiesController.fetch_all_duties()
    return render_template("automate_duties.html", duties=duties) 

@app.route('/automate', methods=['POST'])
def add_automate_duty():
    number = request.form.get('number')
    description = request.form.get('description')
    ksbs = request.form.get('ksbs')
    ksbs_list = []

    if ksbs:
        items = ksbs.split(',')
        for item in items:
            stripped_item = item.strip()
            ksbs_list.append(stripped_item)

    DutiesController.create_duty(number, description, ksbs_list)

    return redirect(url_for('automate_page'))

@app.route('/reset_duties', methods=['POST'])
def reset_duties():
    duties_store._duties.clear()
    return "Duties Store Cleared!"


    