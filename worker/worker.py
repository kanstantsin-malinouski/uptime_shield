import pika, redis, requests, json, time

r = redis.Redis(host='redis', port=6379, decode_responses=True)

def check_site(ch, method, properties, body):
    url = body.decode()
    print(f"Checking: {url}")
    try:
        start = time.time()
        
        res = requests.get(url, timeout=3) 
        ms = round((time.time() - start) * 1000)
        status = "Online" if res.status_code == 200 else f"Error {res.status_code}"
    except:
        status = "Offline"
        ms = 0

    data = {"url": url, "status": status, "ms": ms, "time": time.strftime("%H:%M:%S")}
    r.lpush(f"stats:{url}", json.dumps(data))
    r.ltrim(f"stats:{url}", 0, 4) 
    r.set(f"last:{url}", status)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    time.sleep(10) 
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    ch = conn.channel()
    ch.queue_declare(queue='urls')
    ch.basic_consume(queue='urls', on_message_callback=check_site)
    print("Worker is active and waiting for URLs...")
    ch.start_consuming()

if __name__ == "__main__":
    main()