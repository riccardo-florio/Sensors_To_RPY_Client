# Sensor to RPY Client

Questa applicazione consente di ricevere dati dai sensori di un dispositivo mobile, convertirli in valori di Roll, Pitch e Yaw (RPY), e visualizzarli in tempo reale tramite un'interfaccia grafica intuitiva.

**Nota:** Questo progetto fa parte di un'iniziativa più ampia sul monitoraggio del cedimento strutturale dei ponti. Per maggiori informazioni, visita il repository GitHub corrispondente: [Monitoraggio Cedimento Strutturale dei Ponti](https://github.com/tuo-username/progetto-cedimento-ponti).

## Prerequisiti

- Python 3.x

## Installazione

1. **Clona questo repository:**

   ```bash
   git clone https://github.com/riccardo-florio/Sensors_To_RPY_Client.git
   ```

2. **Naviga nella cartella del progetto:**

   ```bash
   cd Sensors_To_RPY_Client
   ```

3. **Crea un ambiente virtuale:**

   ```bash
   python -m venv venv
   ```

4. **Attiva l'ambiente virtuale:**

   - Su **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - Su **Linux/MacOS**:

     ```bash
     source venv/bin/activate
     ```

5. **Installa le librerie richieste:**

   ```bash
   pip install -r requirements.txt
   ```

## Esecuzione dell'Applicazione

1. **Scarica e installa l'app server per trasmettere i dati:**

   - Scarica l'app **Sensor Server** dal seguente link: [Sensor Server Releases](https://github.com/umer0586/SensorServer/releases)
   - Installa l'app sul tuo dispositivo mobile Android.

2. **Ottieni i valori ENU (East, North, Up):**

   - **Premi il pulsante "Ottieni i dati ENU"** nell'interfaccia grafica del Sensor Client.
   - Verrai reindirizzato al sito web [NOAA Magnetic Field Calculators](https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml#igrfwmm).
   - **Inserisci il CAP (Codice di Avviamento Postale)** nella casella **"Location:"** sul sito web.
   - Premi **"Get & Add Lat / Lon"** per ottenere le coordinate geografiche.
   - Scorri verso il basso e premi **"Calculate"**.
   - Dopo il calcolo, nella sezione dei risultati, **copia i valori** corrispondenti alla **prima riga** e alle colonne **"North Comp"**, **"East Comp"** e **"Vertical Comp"**.
   - **Nota:** I valori saranno espressi in **nanoTesla (nT)**. Per convertirli in **microTesla (µT)**, **dividi ciascun valore per 1000** (ad esempio, 22,848.9 nT diventa 22.8489 µT).
   - **Incolla i valori copiati** nei campi **E**, **N** e **U** nell'interfaccia del Sensor Client, **facendo attenzione a eliminare i punti e mantenere le virgole** (ad esempio, "22,848.9" diventa "22,8489").

3. **Avvia il server sul dispositivo mobile:**

   - Apri l'app **Sensor Server** sul tuo dispositivo mobile.
   - Premi il pulsante per **avviare il server**.
   - L'app visualizzerà l'**indirizzo IP** del dispositivo. **Annota questo indirizzo IP**, poiché dovrai inserirlo nel Sensor Client.

4. **Esegui l'applicazione Sensor Client:**

   - Nel tuo ambiente di sviluppo, esegui l'applicazione:

     ```bash
     python src/main.py
     ```

   - Nella GUI del Sensor Client, **inserisci l'indirizzo IP** del dispositivo mobile (visualizzato dall'app Sensor Server) nel campo **"Inserisci l'IP del dispositivo:"**.

5. **Avvia la ricezione dei dati:**

   - Dopo aver inserito l'indirizzo IP e i valori ENU, premi il pulsante **"Start"** nell'interfaccia del Sensor Client.
   - L'applicazione inizierà a ricevere i dati dai sensori del dispositivo mobile e visualizzerà in tempo reale i grafici di Roll, Pitch e Yaw.

6. **Regola il filtro β se necessario:**

   - Utilizza lo **slider "Filter β"** per regolare l'effetto del filtro sui dati:
     - **β→1**: Maggiore effetto filtrante (dati più smussati).
     - **β→0**: Minore effetto filtrante (dati più reattivi).

## Note

- L'ambiente virtuale non è incluso nel repository ed è ignorato grazie al file `.gitignore`.
- Se riscontri problemi con le librerie, verifica di aver attivato correttamente l'ambiente virtuale e di aver installato tutte le dipendenze.
- Assicurati che il tuo dispositivo mobile e il computer siano **connessi alla stessa rete** per permettere la comunicazione tra il Sensor Server e il Sensor Client.

## Progetto Principale

Questo progetto è parte di un'iniziativa più ampia per il monitoraggio e l'analisi del cedimento strutturale dei ponti. Il progetto principale include sistemi di acquisizione dati, analisi strutturale e altre funzionalità avanzate.

Monitoraggio Cedimento Strutturale dei Ponti: [https://github.com/tuo-username/progetto-cedimento-ponti](https://github.com/tuo-username/progetto-cedimento-ponti)

## Licenza

Questo progetto è rilasciato sotto la licenza MIT.
