# Castle Chess Tournament Manager

A Python console application built following MVC (Model-View-Controller) principles and Object-Oriented Programming (OOP) best practices to run chess tournaments using Swiss-system matchmaking.

---

## Technical Specifications & Features
* **Offline Operation:** Operates locally using JSON files for persistent storage (`data/clubs/` and `data/tournaments/`).
* **Swiss-System Matchmaking:** Dynamically pairs players for rounds based on cumulative scores while avoiding repeat matchups.
* **Player & Tournament Management:** Supports searching players by Chess ID or case-insensitive name substrings.
* **Reports:** Renders player rankings sorted descending by points and full round-by-round match histories.
* **PEP 8 Compliance:** Formatted strictly within the 119-character line limit.

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/Saumya20-p/castle_chess.git](https://github.com/Saumya20-p/castle_chess.git)
   cd castle_chess

2.  Set Up Python Virtual Environment:
   ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Install Dependencies:
    ```bash
    pip install -r requirements.txt

---

## How to Run the Application

Launch the main controller application from your terminal:
    ```bash
    python main.py

---

## Generating the Flake8 Quality Report

1. To audit code quality and generate the official HTML report:
    ```bash
    flake8 --format=html --htmldir=flake8_report

2. To view the generated report on macOS:
    ```bash
    open flake8_report/index.html