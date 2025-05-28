from flask import Flask, request, jsonify
import redis
import threading
import pika
import json

app = Flask(__name__)

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_KEY = 'event-list'

RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'critical-events'

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

event_list = []

cached = redis_client.get(REDIS_KEY)
if cached:
    event_list = json.loads(cached)

# Endpoint POST /event
@app.route('/event', methods=['POST'])
def add_event():
    event = request.get_json()
    if not event:
        return jsonify({'error': 'Corpo inválido'}), 400

    event_list.append(event)
    redis_client.set(REDIS_KEY, json.dumps(event_list))
    return jsonify({'message': 'Evento registrado com sucesso'}), 201

# Endpoint GET /events
@app.route('/events', methods=['GET'])
def get_events():
    try:
        cached_data = redis_client.get(REDIS_KEY)
        if cached_data:
            print("[Redis] Retornando eventos do cache")
            return jsonify(json.loads(cached_data)), 200
        else:
            print("[Redis] Cache vazio, retornando lista da memória")
            return jsonify(event_list), 200
    except Exception as e:
        print(f"[Erro Redis] {e}")
        return jsonify({'error': 'Erro ao acessar o cache'}), 500

def consume_rabbitmq():
    def callback(ch, method, properties, body):
        try:
            msg = json.loads(body)
            print("[RabbitMQ] Mensagem recebida:", msg)
            event_list.append(msg)
            redis_client.set(REDIS_KEY, json.dumps(event_list))
        except Exception as e:
            print(f"[RabbitMQ] Erro ao processar mensagem: {e}")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
        print("[RabbitMQ] Consumidor iniciado na fila 'critical-events'")
        channel.start_consuming()
    except Exception as e:
        print(f"[RabbitMQ] Erro ao conectar: {e}")

threading.Thread(target=consume_rabbitmq, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
