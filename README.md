# Sensor Client

Questa applicazione consente di ricevere dati dai sensori di un dispositivo mobile, convertirli in valori di Roll, Pitch e Yaw (RPY), e visualizzarli in tempo reale tramite un'interfaccia grafica intuitiva.

**Nota:** Questo progetto fa parte di un'iniziativa più ampia sul monitoraggio del cedimento strutturale dei ponti. Per maggiori informazioni, visita il repository GitHub corrispondente: [Monitoraggio Cedimento Strutturale dei Ponti](https://github.com/tuo-username/progetto-cedimento-ponti).


## Prerequisiti

- Python 3.x
- Ambiente virtuale Python (consigliato)

## Installazione

1. **Clona questo repository:**

   ```bash
   git clone https://github.com/tuo-username/sensor_client.git
   ```

2. **Naviga nella cartella del progetto:**
   
   ```bash
   cd sensor_client
   ```

3. **Crea un ambiente virtuale:**

   ```bash
   python -m venv venv
   ```

4. **Attiva l'ambiente virtuale:**

   Su Windows:
     
     ```bash
     venv\Scripts\activate
     ```

   Su Linux/MacOs:
    
    ```bash
    source venv/bin/activate
    ```

5. **Installa le librerie richieste:**

   ```bash
   pip install -r requirements.txt
   ```

## Esecuzione dell'Applicazione

1. **Assicurati che il tuo dispositivo mobile sia connesso e stia trasmettendo i dati dei sensori.**

2. **Esegui l'applicazione:**

   ```bash
   python src/main.py
   ```

3. **Inserisci l'indirizzo IP del dispositivo e i valori ENU richiesti nell'interfaccia grafica.**

## Note

- L'ambiente virtuale non è incluso nel repository ed è ignorato grazie al file ```.gitignore```.

- Se riscontri problemi con le librerie, verifica di aver attivato correttamente l'ambiente virtuale e di aver installato tutte le dipendenze.

## Progetto Principale
Questo progetto è parte di un'iniziativa più ampia per il monitoraggio e l'analisi del cedimento strutturale dei ponti. Il progetto principale include sistemi di acquisizione dati, analisi strutturale e altre funzionalità avanzate.

Monitoraggio Cedimento Strutturale dei Ponti: https://github.com/tuo-username/progetto-cedimento-ponti

## Licenza
Questo progetto è rilasciato sotto la licenza MIT.
