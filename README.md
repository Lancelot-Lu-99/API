# Clone the repository
git clone https://github.com/Lancelot-Lu-99/API.git

# Navigate to the project directory
cd API

# Update package lists
sudo apt update

# Install essential packages and PostgreSQL dependencies
sudo apt install -y build-essential python3-dev libpq-dev

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install -r requirements.txt

# Set up environment variables and run the application
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=5000

# After initial configuration, only the following steps are required to run the application
# Start virtual environment
source venv/bin/activate

# Run the application
flask run --host=0.0.0.0 --port=5000
# OR
python3 run.py
