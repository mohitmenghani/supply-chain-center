#!/bin/bash

# Terminate existing background infrastructure if active
echo "🧹 Cleaning active port allocations (8000, 8501)..."
fuser -k 8000/tcp 2>/dev/null
fuser -k 8501/tcp 2>/dev/null

echo "🚀 Launching Unified AMD ROCm Operational Supply Chain System..."

# Initialize dataset generation loop if missing
if [ ! -f "synthetic_intelligent_supply_chain.csv" ]; then
    echo "⚙️ Base data ledger missing. Executing synthesizer pipeline..."
    python3 generate_data.py
fi

# Run backend engine as a background daemon
echo "🖥️ Booting Uvicorn Compute Service (FastAPI + vLLM Framework)..."
python3 server.py > backend_runtime.log 2>&1 &
BACKEND_PID=$!

echo "⏳ Pausing for 15 seconds to allow vLLM to instantiate and bind VRAM pools..."
sleep 15

# Launch the Streamlit presentation portal
echo "🎨 Starting Streamlit User Portal..."
streamlit run app.py --server.port 8501 --server.address 127.0.0.1

# Trap exits to ensure the environment does not orphan backend resources
trap "echo 'Stopping background workers...'; kill $BACKEND_PID" EXIT