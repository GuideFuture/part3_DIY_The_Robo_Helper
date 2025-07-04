# Smart AI Predictor
# Συνδέεται με Arduino και εκπαιδεύει μοντέλο AI (Linear Regression)
# για πρόβλεψη θερμοκρασίας από απόσταση
# Δημιουργός: Greg Ios 

import serial
import time
from sklearn.linear_model import LinearRegression

# Serial Port Ρύθμιση
PORT = 'COM3'  # άλλαξε σε /dev/ttyUSB0 για Linux
BAUDRATE = 9600

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"[✔] Συνδέθηκε στο {PORT}")
except:
    print(f"[✘] Δεν μπόρεσα να συνδεθώ στο {PORT}")
    exit()

time.sleep(2)  # περιμένουμε το Arduino να ξεκινήσει

# Λίστα δεδομένων
data = []

print("[ℹ] Ανάγνωση δεδομένων και εκπαίδευση μοντέλου...")

try:
    while True:
        line = ser.readline().decode().strip()
        
        if "distance" in line:
            try:
                parts = line.split(",")
                distance = int(parts[0].split(":")[1])
                temperature = int(parts[1].split(":")[1])

                data.append([distance, temperature])
                print(f"📡 Απόσταση: {distance} cm | 🌡 Θερμοκρασία: {temperature}°C")

                # Αφού μαζέψουμε τουλάχιστον 20 δείγματα
                if len(data) >= 20:
                    X = [[d[0]] for d in data]
                    y = [d[1] for d in data]

                    model = LinearRegression().fit(X, y)

                    # Προβλέπει θερμοκρασία για κάποια απόσταση
                    test_distance = 30  # cm
                    prediction = model.predict([[test_distance]])[0]
                    print(f"🤖 AI Προβλέπει Θερμοκρασία στους {test_distance}cm: {prediction:.2f}°C")

            except (IndexError, ValueError):
                print("[!] Σφάλμα στην ανάλυση των δεδομένων:", line)

        time.sleep(0.3)

except KeyboardInterrupt:
    print("\n[⏹] Τερματισμός από χρήστη.")
    ser.close()
