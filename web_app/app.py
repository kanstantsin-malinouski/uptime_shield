from flask import Flask, render_template, request, jsonify
import pika, redis, json, threading, time

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

def send_to_queue(url):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='urls')
        channel.basic_publish(exchange='', routing_key='urls', body=url)
        connection.close()
    except Exception as e:
        print(f"Queue Error: {e}")

def scheduler():
    while True:
        urls = r.smembers("monitored_urls")
        for url in urls:
            send_to_queue(url)
        time.sleep(30) 

threading.Thread(target=scheduler, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_url():
    url = request.json.get('url', '').strip()
    if not url: return jsonify({"status": "error"})
    if not url.startswith('http'): url = 'https://' + url
    
    r.sadd("monitored_urls", url)
    send_to_queue(url) 
    return jsonify({"status": "added"})

@app.route('/data')
def get_data():
    urls = r.smembers("monitored_urls")
    results = []
    for url in urls:
        last_status = r.get(f"last:{url}")
        history = [json.loads(x) for x in r.lrange(f"stats:{url}", 0, -1)]
        results.append({
            "url": url, 
            "status": last_status if last_status else "Checking...", 
            "history": history
        })
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)