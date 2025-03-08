import subprocess
import threading
import os
import time
import webbrowser
import sys
import signal

# Define commands to run FastAPI and Streamlit
fastapi_cmd = ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# Add --no-browser flag to prevent Streamlit from automatically opening a browser window
streamlit_cmd = ["streamlit", "run", "streamlit_app.py", "--server.headless", "true"]

processes = []

def run_command(cmd, name):
    """Run a command in a subprocess"""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    processes.append(process)
    
    print(f"\n[{name}] Starting process...")
    
    for line in process.stdout:
        print(f"[{name}] {line.strip()}")
    
    process.wait()
    if process.returncode != 0:
        print(f"[{name}] Process exited with code {process.returncode}")

def signal_handler(sig, frame):
    """Handle termination signals"""
    print("\nShutting down all processes...")
    for process in processes:
        process.terminate()
    sys.exit(0)

def open_browser():
    """Open browser after a delay to ensure Streamlit server is ready"""
    time.sleep(3)  # Wait a bit longer to ensure Streamlit is fully ready
    print("Opening browser to Streamlit UI...")
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_command, args=(fastapi_cmd, "FastAPI"))
    fastapi_thread.daemon = True
    fastapi_thread.start()
    
    # Give FastAPI time to start
    time.sleep(2)
    
    # Start Streamlit in a separate thread
    streamlit_thread = threading.Thread(target=run_command, args=(streamlit_cmd, "Streamlit"))
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Open browser in yet another thread with a delay
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        for process in processes:
            process.terminate()
