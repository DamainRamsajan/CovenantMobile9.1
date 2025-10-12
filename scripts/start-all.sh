#!/data/data/com.termux/files/usr/bin/bash
set -e

# Activate wake lock
termux-wake-lock 2>/dev/null || true

# Start LLaMA server in background
echo "Starting LLaMA server..."
MODEL=~/storage/shared/projects/CovenantMobile9.1/data/models/tinyllama-chat-q4km.gguf
cd ~/native/llama.cpp
./build/bin/llama-server --model "$MODEL" --host 127.0.0.1 --port 8080 -c 4096 --parallel 2 > ~/storage/shared/projects/CovenantMobile9.1/logs/llama.log 2>&1 &

# Wait a few seconds to ensure it's running
sleep 5

# Start Django (Uvicorn)
echo "Starting Covenant Mobile..."
source ~/.venvs/CovenantMobile9.1/bin/activate
cd ~/storage/shared/projects/CovenantMobile9.1
export $(cat .env.prod | xargs)
uvicorn covenant.asgi:application --host 0.0.0.0 --port 8787 --workers 1
