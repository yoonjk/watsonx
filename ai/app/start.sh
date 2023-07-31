#!/bin/bash

PORT=8000
uvicorn --host=0.0.0.0 --port $PORT  main:app --reload

