#!/bin/bash

echo "Starting AI Crowd Density & Abnormal Behavior Detection Application"
echo ""

echo "[1/2] Starting Backend Server..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "[2/2] Starting Frontend Server..."
cd frontend
node node_modules/vite/bin/vite.js &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "Application is starting..."
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:5000"
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop both servers"

# Handle Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
