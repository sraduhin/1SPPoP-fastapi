#!/bin/bash

echo " >>>> Running api"
uvicorn main:app --host 0.0.0.0 --port 8000