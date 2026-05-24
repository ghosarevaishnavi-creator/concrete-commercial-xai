#!/bin/bash
# Simple entrypoint to run both Streamlit and Uvicorn in background for demo.
# For production use a proper process manager.

export PYTHONUNBUFFERED=1

# Start uvicorn API
uvicorn batch_api:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Start streamlit
streamlit run app.py --server.port 8501 --server.headless true &
STREAM_PID=$!

wait $API_PID $STREAM_PID
