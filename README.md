# Artemis 2 Simulation

## Get started

```bash
git clone https://gitlab.com/LeZ.fr/artemis2-simulation.git 
cd artemis2-simulation
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pip-tools
pip-sync
python main.py
```

## Rotation 

The moon rotates on itself at 16.7 km/h. ( rotation of 1 in the application so we use a factor of 16 )

The earth rotates on itself at 1600.0 km/h.

Whereas, the earth rotates roughly 97 times faster than the moon.

## Position 

The earth moon distance is roughly 384 400 kilometers.

In the application in the application, the distance between each is 4.

