# Covenant Mobile 9.1 – Current System State (Checkpoint)

## Overview
This document captures the exact operational state of the Covenant Mobile 9.1 project as of the latest checkpoint.

---

## 🧩 Project Directory Summary
- **Main Project:** `~/storage/shared/projects/CovenantMobile9.1`
- **Virtual Environment:** `~/.venvs/CovenantMobile9.1`
- **LLaMA Components:**  
  - Model: `~/models/tinyllama-chat-q4km.gguf`  
  - Binary Directory: `~/native/llama.cpp/build/bin/`
  - LLaMA Server Startup Script: `~/scripts/start-llama.sh`
- **Django/Uvicorn Components:**  
  - Django App: `covenant` (inside main project directory)
  - Server Startup Command (Uvicorn):  
    ```bash
    cd ~/storage/shared/projects/CovenantMobile9.1
    source ~/.venvs/CovenantMobile9.1/bin/activate
    export $(grep -v '^#' .env.prod | xargs)
    uvicorn covenant.asgi:application --host 0.0.0.0 --port 8787 --reload
    ```
- **Combined Startup Script:**  
  `~/scripts/start-all.sh` runs both servers sequentially.

---

## 🧠 LLaMA Server Launch Command
```bash
MODEL=~/models/tinyllama-chat-q4km.gguf
~/native/llama.cpp/build/bin/llama-server \
  --model "$MODEL" \
  --host 127.0.0.1 \
  --port 8080 \
  -c 4096 \
  --parallel 2
