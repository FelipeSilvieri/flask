import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

doses = ["FANTA", "COCA", "GUARANA", "VODKA"]

LIMIT = 60

drinks = [
    {
        "id": 1,
        "bt_id": 1,
        "name": "FantosaCoquissima",
        "price": 20,
        "dose_A": "Fanta",
        "dose_B": "Coca",
        "qty_A": 2,
        "qty_B": 2,
        "img_url": "https://p2.trrsf.com/image/fget/cf/1200/1200/middle/images.terra.com/2013/11/30/cocacoaacucar.jpg",
        "description": "Muito oba oba"
    },
    {
        "id": 2,
        "bt_id": 1,
        "name": "FantosaGuaraníssima",
        "price": 20,
        "dose_A": "Fanta",
        "dose_B": "Guarana",
        "qty_A": 2,
        "qty_B": 2,
        "img_url": "https://p2.trrsf.com/image/fget/cf/1200/1200/middle/images.terra.com/2013/11/30/cocacoaacucar.jpg",
        "description": "Uma explosão de frutas tropicais"
    }
]

bottles = [
    {
        "id": 1,
        "drink_name": "Fanta",
        "actual_level": 61,
        "rele_pin_number": 25,
        "moisture_pin_number": 17
    },
    {
        "id": 2,
        "drink_name": "Coca",
        "actual_level": 80,
        "rele_pin_number": 23,
        "moisture_pin_number": 27
    },
    {
        "id": 3,
        "drink_name": "Guarana",
        "actual_level": 70,
        "rele_pin_number": 24,
        "moisture_pin_number": 22
    },
]


@app.route('/get_all_drinks', methods=['GET'])
def get_all_drinks():
    return jsonify(drinks)


@app.route('/get_all_by_bt_id', methods=['GET'])
def get_all_by_bt_id():
    bt_id = request.args.get('bt_id')

    if bt_id == '1':
        drinks_same_bt_id = [drink for drink in drinks if drink["bt_id"] == 1]
    elif bt_id == '2':
        drinks_same_bt_id = drinks
    else:
        return jsonify({"error": "bt_id inválido"}), 400

    if drinks_same_bt_id:
        drinks_info = [{"id": drink["id"], "name": drink["name"], "price": drink["price"],
                        "img_url": drink["img_url"]} for drink in drinks_same_bt_id]
        return jsonify(drinks_info)
    else:
        return jsonify({"error": "Nenhuma bebida encontrada com o bt_id fornecido"}), 404


@app.route('/get_detail_by_id', methods=['GET'])
def get_detail_by_id():
    id = request.args.get('id')
    drinks_same_id = [drink for drink in drinks if drink["id"] == int(id)]
    if drinks_same_id:
        drinks_info = [{key: value for key, value in drink.items() if key not in [
            "bt_id"]} for drink in drinks_same_id]
        return jsonify(drinks_info)
    else:
        return jsonify({"error": "Nenhuma bebida encontrada com o id fornecido"}), 404


@app.route('/create_drink', methods=['POST'])
def create_drink():
    data = request.get_json()
    new_drink = {
        "id": len(drinks) + 1,
        "bt_id": data["bt_id"],
        "name": data["name"],
        "price": data["price"],
        "dose_A": data["dose_A"],
        "dose_B": data["dose_B"],
        "qty_A": data["qty_A"],
        "qty_B": data["qty_B"],
        "img_url": data["img_url"],
        "description": data["description"]

    }
    drinks.append(new_drink)
    return jsonify({"message": "Bebida criada com sucesso"}), 201


@app.route('/verify_drink', methods=['GET'])
def verify_drink():
    id = request.args.get('id')
    drink = next((d for d in drinks if d["id"] == int(id)), None)
    if drink:
        if drink["dose_A"].upper() in doses and drink["dose_B"].upper() in doses:
            return jsonify({"result": True})
        else:
            return jsonify({"result": False})
    else:
        return jsonify({"error": "Nenhuma bebida encontrada com o id fornecido"}), 404


@app.route('/verify-doses', methods=['GET'])
def verify_doses():
    dose_A = request.args.get('dose_A').upper()
    dose_B = request.args.get('dose_B').upper()
    array = []
    for bottle in bottles:
        if (bottle["drink_name"].upper() == dose_A):
            array.append(bottle["actual_level"] > LIMIT)
        if (bottle["drink_name"].upper() == dose_B):
            array.append(bottle["actual_level"] > LIMIT)

    if False not in array:
        return jsonify(True), 200
    else:
        return jsonify(False), 404

def on_publish(client, userdata, mid):
  print("ID Solicitação: "+str(mid))

# @app.route('/make-order', methods=['POST'])
# def make_order():
#     dose_A = request.args.get('dose_A').upper()
#     qtd_A = int(request.args.get('qtd_A'))
#     dose_B = request.args.get('dose_B').upper()
#     qtd_B = int(request.args.get('qtd_B'))
#     rele_pin_a = 0
#     adc_pin_a = 0
#     rele_pin_b = 0
#     adc_pin_b = 0
#     for bottle in bottles:
#         if (bottle["drink_name"].upper() == dose_A):
#             rele_pin_a = int(bottle["rele_pin_number"])
#             adc_pin_a = int(bottle["moisture_pin_number"])
#         if (bottle["drink_name"].upper() == dose_B):
#             rele_pin_b = int(bottle["rele_pin_number"])
#             adc_pin_b = int(bottle["moisture_pin_number"])

#     client = mqtt.Client()            
#     client.on_publish = on_publish
#     client.connect("broker.hivemq.com",1883)
#     # outro broker pode ser : test.mosquitto.org
#     client.loop_start()
    

#     try:
#         time.sleep(2)
#         for _ in range(1):
#             jsonData = {
#                         "rele_pin_a": rele_pin_a,
#                         "rele_pin_b": rele_pin_b,
#                         "qtd_A": qtd_A,
#                         "qtd_B": qtd_B
#                         }
   
#             jsonOut = json.dumps(jsonData)
#             (rc, mid) = client.publish("microcontroladores/t3",jsonOut, 0)
#     except:
#         print('Byebye')
    
#     client.disconnect()

#     if (rele_pin_a == 0 and adc_pin_a == 0 and rele_pin_b == 0 and adc_pin_b == 0):
#         return jsonify("Erro ao realizar a bebida"), 400
#     else:
#         return jsonify("Sucesso"), 200

  
if __name__ == '__main__':
    app.run(debug=True)
