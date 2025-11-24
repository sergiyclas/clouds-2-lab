import requests
import threading
import time
import random

BASE_URL = "http://clouds-lab-2-2-2-2-alb-2046982737.eu-north-1.elb.amazonaws.com/"
ENDPOINTS = [
    {"method": "get", "url": "customers"},
    {"method": "post", "url": "customers", "json": {"customer_name": "Test User", "email": "test@example.com", "phone": "1234567890"}},
    {"method": "post", "url": "create/tables"},
    {"method": "post", "url": "customers/noname", "json": {"start": "2024-01-01", "end": "2024-12-31"}},
    {"method": "get", "url": "customers/1"},
    {"method": "put", "url": "customers/1", "json": {"customer_name": "Updated User", "email": "upd@example.com", "phone": "1112223333"}},
    {"method": "delete", "url": "customers/1"},
    {"method": "get", "url": "customers/1/accounts"},
    {"method": "post", "url": "insert", "json": {"table_name": "transactions", "column_list": ["amount", "transaction_date"], "value_list": [100, "2024-07-01"]}},
    {"method": "post", "url": "login", "json": {"username": "admin", "password": "123456"}}
]

CONCURRENCY = 100
DURATION = 3600
TIMEOUT = 15

stop_flag = False
lock = threading.Lock()
ok = 0
err = 0

def worker(thread_id):
    global ok, err
    session = requests.Session()

    while not stop_flag:
        ep = random.choice(ENDPOINTS)
        url = BASE_URL + ep["url"]
        started = time.time()

        try:
            if ep["method"] == "get":
                resp = session.get(url, timeout=TIMEOUT)
            elif ep["method"] == "post":
                resp = session.post(url, json=ep.get("json", {}), timeout=TIMEOUT)
            elif ep["method"] == "put":
                resp = session.put(url, json=ep.get("json", {}), timeout=TIMEOUT)
            elif ep["method"] == "delete":
                resp = session.delete(url, timeout=TIMEOUT)
            else:
                continue

            elapsed = time.time() - started

            with lock:
                if 200 <= resp.status_code < 300:
                    ok += 1
                    print(f"[Thread-{thread_id}] {ep['method'].upper()} {url} ({resp.status_code}) {elapsed*1000:.1f}ms")
                else:
                    err += 1
                    print(f"[Thread-{thread_id}] ⚠ {ep['method'].upper()} {url} ({resp.status_code}) {elapsed*1000:.1f}ms")

        except Exception as e:
            elapsed = time.time() - started
            with lock:
                err += 1
                print(f"[Thread-{thread_id}] {ep['method'].upper()} {url} ERROR after {elapsed*1000:.1f}ms ({e})")

threads = []
print(f"Start load test for {DURATION}s with {CONCURRENCY} threads")
start = time.time()
print("...")

for i in range(CONCURRENCY):
    t = threading.Thread(target=worker, args=(i + 1,))
    t.start()
    threads.append(t)

time.sleep(DURATION)
stop_flag = True

for t in threads:
    t.join()

total = ok + err
elapsed = time.time() - start
print(f"\nDone in {elapsed:.1f}s")
print(f"Total requests: {total}")
print(f"OK: {ok}")
print(f"ERR: {err}")
print(f"RPS: {total / elapsed:.1f}")
