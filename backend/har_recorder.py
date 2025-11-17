from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import threading
import queue

app = Flask(__name__)

task_queue = queue.Queue()
worker_thread = None

HAR_FILE = "session.har"

def playwright_worker(url):
    print(f"[Worker] Starting Playwright for URL: {url}")

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)

    context = browser.new_context(
        record_har_path=HAR_FILE,
        record_har_content="embed"
    )

    page = context.new_page()

    # 🔥 THIS IS THE URL THAT OPENS — NO HARDCODED SAUCEDEMO
    page.goto(url)

    print("[Worker] Browser opened:", url)

    while True:
        if task_queue.get() == "STOP":
            break

    print("[Worker] Stopping...")

    context.close()
    browser.close()
    pw.stop()


@app.route("/start", methods=["POST"])
def start_recording():
    global worker_thread

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL missing!"}), 400

    if worker_thread and worker_thread.is_alive():
        return jsonify({"status": "already recording"})

    worker_thread = threading.Thread(target=playwright_worker, args=(url,))
    worker_thread.start()

    return jsonify({"status": "started", "url": url})


@app.route("/stop", methods=["POST"])
def stop_recording():
    if not worker_thread or not worker_thread.is_alive():
        return jsonify({"error": "Not recording right now"}), 400

    task_queue.put("STOP")
    worker_thread.join()

    return jsonify({"status": "stopped", "har_file": HAR_FILE})


if __name__ == "__main__":
    app.run(port=5001)
