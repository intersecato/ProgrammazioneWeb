import mysql.connector
import random
from datetime import datetime, timedelta

# Configurazione
NUM_FILM = 300
NUM_SALE = 10
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2025, 12, 31)

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="user",
        password="password",
        database="cinema"
    )
    cur = conn.cursor()

    with open("film.txt", "r", encoding="utf-8") as f:
        titoli = [line.strip() for line in f if line.strip()]

    # Popolazione Film
    lingue = ["Italiano", "Inglese", "Francese", "Tedesco", "Spagnolo"]
    for i in range(1, NUM_FILM + 1):
        titolo = titoli[i - 1]
        anno = random.randint(1980, 2024)
        durata = random.randint(80, 180)
        lingua = random.choice(lingue)
        cur.execute("INSERT INTO film VALUES (%s, %s, %s, %s, %s)", (i, titolo, anno, durata, lingua))
    print("✔ Film inseriti.")

    # Popolazione Sale
    for i in range(1, NUM_SALE + 1):
        numFile = random.randint(5, 20)
        postiPerFila = random.randint(5, 20)
        tipo = random.choice(['3-D', 'tradizionale'])
        dim = round(random.uniform(150.0, 350.0), 2)
        numPosti = numFile * postiPerFila
        cur.execute("INSERT INTO sala VALUES (%s, %s, %s, %s, %s, %s)", (
            i, numPosti, dim, numFile, postiPerFila, tipo))
    print("✔ Sale inserite.")

    # Popolazione Proiezioni
    film_proiettati = random.sample(range(1, NUM_FILM + 1), int(NUM_FILM * 0.8))
    proiezione_id = 1
    proiezioni = []

    for film_id in film_proiettati:
        giorni = random.randint(1, 21)
        prima_data = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days - giorni))
        for g in range(giorni):
            data = prima_data + timedelta(days=g)
            orari_possibili = ["14:00", "17:00", "21:00", "22:30"]
            orari = random.sample(orari_possibili, random.randint(1, len(orari_possibili)))
            sale = random.sample(range(1, NUM_SALE + 1), len(orari))
            for ora, sala in zip(orari, sale):
                cur.execute("INSERT INTO proiezione VALUES (%s, %s, %s, %s, %s)",
                            (proiezione_id, sala, film_id, data.date(), ora))
                proiezioni.append((proiezione_id, sala))
                proiezione_id += 1
    print("✔ Proiezioni inserite.")

    # Popolazione Biglietti
    for idx, (p_id, sala_id) in enumerate(proiezioni):
        cur.execute("SELECT numFile, numPostiPerFila FROM sala WHERE numero = %s", (sala_id,))
        res = cur.fetchone()
        if not res:
            continue
        numFile, postiPerFila = res
        posti_tot = numFile * postiPerFila
        biglietti_da_emettere = min(posti_tot, max(1, int(random.gauss(posti_tot * 0.7, 5))))
        posti_occupati = set()
        while len(posti_occupati) < biglietti_da_emettere:
            posti_occupati.add((random.randint(1, numFile), random.randint(1, postiPerFila)))
        for fila, posto in posti_occupati:
            data_vendita = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
            prezzo = round(random.uniform(5.0, 12.0), 2)
            cur.execute("INSERT INTO biglietto VALUES (%s, %s, %s, %s, %s)",
                        (p_id, fila, posto, data_vendita.date(), prezzo))
        if idx % 100 == 0:
            print(f"➤ Inseriti biglietti per {idx} proiezioni...")
    print("✔ Biglietti inseriti.")

    # Finalizzazione
    conn.commit()
    print("✔ Database popolato con successo!")

except Exception as e:
    print("❌ Errore durante l'esecuzione:", e)
    conn.rollback()

finally:
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
