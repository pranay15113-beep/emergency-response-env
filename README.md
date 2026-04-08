---
title: Emergency Response Env
emoji: 🚨
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "1.30.0"
python_version: "3.10"
app_file: app.py
pinned: false
---
# 🚨 Emergency Response RL Environment

## 🧠 Problem Statement

Design and implement a reinforcement learning environment that simulates emergency response coordination. The agent must allocate limited resources such as ambulances, firetrucks, and police units across multiple incidents, including cascading events, to maximize response effectiveness.

---

## ⚙️ Features

* Multi-incident emergency simulation
* Cascading events (e.g., fire leading to accidents)
* Resource allocation-based decision making
* Reward system based on allocation accuracy
* Lightweight environment for fast evaluation

---

## 🧪 Tasks

* **Easy:** Single incident resource allocation
* **Medium:** Multiple simultaneous incidents
* **Hard:** Cascading emergency scenarios

---

## 🧮 Reward System

* Rewards are calculated based on how closely allocated resources match required resources
* Partial rewards for near-correct allocations
* Over-allocation or under-allocation reduces score
* Final reward is normalized between `0` and `1`

---

## ▶️ How It Works

1. Environment generates emergency incidents
2. Agent observes incident details (type, severity, requirements)
3. Agent allocates resources
4. Environment evaluates allocation using grading logic
5. Reward is returned based on performance

---

## 📁 Project Structure

```
emergency-response-env/
│── data/                # Incident data
│── env/                 # Environment logic
│── tasks/               # Grading and task definitions
│── app.py               # Entry point
│── baseline.py          # Simple agent
│── inference.py         # Testing / evaluation script
│── ui.py                # Optional UI
│── openenv.yaml         # Environment config
│── requirements.txt     # Dependencies
│── Dockerfile           # Deployment config
```

---

## 🚀 Execution

Run locally:

```bash
python app.py
```

Run inference:

```bash
python inference.py
```

---

## 🌐 Deployment

Deployed using **Hugging Face Spaces** with Docker support.

---

## 🧩 Tech Stack

* Python
* OpenEnv framework
* Hugging Face Spaces
* Docker

---

## 📌 Notes

* Designed for reinforcement learning experimentation
* Focuses on realistic emergency scenarios
* Supports scalable task difficulty
fastapi
uvicorn
pydantic

---
