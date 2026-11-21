#!/usr/bin/env python3
"""Builds the full IT01 edit: joins the chapter narration and writes episode.json for engine/museo.py.

Usage (inside the assets folder of the episode, i.e. where narration_audio/, ai/ and the image folders live):
    python3 build_it01.py <assets_dir>
    python3 ../../engine/museo.py <assets_dir>/episode.json
Times in SHOTS are seconds inside each chapter's own audio (taken from words/*.words.json).
"""
import json, os, subprocess, sys

A = sys.argv[1]
GAP = 0.45  # breath between chapters
CH = ["ch00_hook", "ch01_mazze", "ch02_baionetta", "ch03_dumdum", "ch04_lanciafiamme", "ch05_cloro",
      "ch06_fosgene", "ch07_iprite", "ch08_caporetto", "ch09_ginevra", "ch10_finale"]

hook = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hook.json")))["shots"]


def img(*p):
    return {"images": list(p)}


def ai(i):
    return f"ai/{i}_1.jpg"


SHOTS = {
 "ch00_hook": hook,
 "ch01_mazze": [
  {"t": 0, "title": "LE MAZZE FERRATE", "sub": "Fronte italiano · 1915–1918", "src": "Collezione museale", **img("mazza_ferrata/3_commons.jpg"), "tag": "MUSEO", "move": "in"},
  {"t": 3.2, "title": "COME NEL MEDIOEVO", "sub": "Armi da trincea", "src": "Ricostruzione", **img(ai("ai_club_workshop")), "move": "left", "label": ["ARMI IMPROVVISATE", "piombo, chiodi, filo spinato"], "label_at": 1.2},
  {"t": 6.0, "title": "LA TRINCEA", "sub": "Larga un metro", "src": "Ricostruzione", **img(ai("ai_trench_narrow")), "move": "in", "impact": "1 METRO", "impact_at": 3.6},
  {"t": 11.4, "title": "TORNARE ALLE ARMI ANTICHE", "sub": "Carso", "src": "Trincee del Carso", **img("trincea_carso/1_commons.jpg", "trincea_carso/5_openverse.jpg"), "move": "right"},
  {"t": 18.6, "title": "PRODUZIONE IN SERIE", "sub": "Esercito austro-ungarico", "src": "Archivio", "doc": {"head": "ARMI DA TRINCEA · K.u.K.", "lines": ["Mazze con testa di piombo", "Chiodi da cavallo", "Filo spinato arrotolato", "Produzione: in serie"], "stamp": "1916"}},
  {"t": 21.4, "title": "INCURSIONI NOTTURNE", "sub": "Uccidere senza rumore", "src": "Ricostruzione", **img(ai("ai_night_raid")), "move": "in", "impact": "SILENZIO", "impact_at": 2.4},
  {"t": 25.7, "title": "SUL CARSO", "sub": "Testimonianze italiane", "src": "Archivio", **img("san_michele/2_openverse.jpg"), "move": "in", "tag": "BOLLETTINO"},
  {"t": 30.6, "title": "SENZA DIFESA", "sub": "Feriti a terra", "src": "Ricostruzione", **img(ai("ai_surrender")), "move": "out"},
  {"t": 34.5, "title": "CONVENZIONE DELL'AIA, 1907", "sub": "Articolo 23", "src": "L'Aia · 18 ottobre 1907", **img("aia_1907/1_commons.jpg"), "move": "in"},
  {"t": 40.8, "title": "ARTICOLO 23", "sub": "L'Aia · 1907", "src": "Regolamento sulle leggi e gli usi della guerra", "doc": {"head": "ARTICOLO 23 (c)", "lines": ["È vietato uccidere o ferire un nemico", "che, avendo deposto le armi o non avendo", "più mezzi di difesa, si è reso a discrezione."], "stamp": "VIETATO"}, "impact": "NESSUNA PIETÀ?", "impact_at": 4.0},
 ],
 "ch02_baionetta": [
  {"t": 0, "title": "LA BAIONETTA A SEGA", "sub": "Esercito tedesco", "src": "Collezione museale", **img("sawback/1_commons.jpg"), "move": "left", "tag": "MUSEO"},
  {"t": 4.0, "title": "UNA FILA DI DENTI", "sub": "Sul dorso della lama", "src": "Collezione museale", **img("sawback/2_openverse.jpg", "sawback/3_commons.jpg"), "move": "in", "label": ["SÄGEBAJONETT", "baionetta dei genieri"], "label_at": 1.2},
  {"t": 6.6, "title": "I GENIERI", "sub": "Per tagliare legno e rami", "src": "Ricostruzione", **img(ai("ai_pioneers_saw")), "move": "right"},
  {"t": 9.6, "title": "LA PROPAGANDA", "sub": "Giornali alleati · 1915", "src": "Archivio", **img(ai("ai_newspaper")), "move": "in"},
  {"t": 12.5, "title": "UN SIMBOLO", "sub": "Manifesti di guerra", "src": "Manifesto britannico", **img("propaganda_ww1/3_commons.jpg"), "move": "out", "impact": "PROPAGANDA", "impact_at": 2.0},
  {"t": 21.0, "title": "PRIGIONIERI", "sub": "Una voce terribile", "src": "Ricostruzione", **img(ai("ai_pow_column")), "move": "left"},
  {"t": 26.2, "title": "LE TESTIMONIANZE", "sub": "Soldati britannici", "src": "Archivio", "doc": {"head": "TESTIMONIANZA", "lines": ["\"Nessuno voleva essere preso", "da un uomo con quella lama.\"", "— soldato britannico, fronte occidentale"], "stamp": "1916"}},
  {"t": 33.3, "title": "I DENTI LIMATI", "sub": "Esercito tedesco · 1917", "src": "Ricostruzione", **img(ai("ai_file_teeth")), "move": "in"},
  {"t": 37.4, "title": "NESSUN TRATTATO", "sub": "Bastò la paura", "src": "", **img("amputati/1_commons.jpg"), "move": "in", "impact": "LA PAURA", "impact_at": 2.4},
 ],
 "ch03_dumdum": [
  {"t": 0, "title": "IL PROIETTILE ESPANSIVO", "sub": "Dum-dum", "src": "Collezione", **img("dumdum/4_commons.jpg"), "move": "in", "tag": "MUSEO"},
  {"t": 2.6, "title": "UN FORO PULITO", "sub": "Proiettile normale", "src": "Ricostruzione", **img(ai("ai_bullet_open")), "move": "left", "label": ["NORMALE vs ESPANSIVO", "a confronto"], "label_at": 1.5},
  {"t": 7.3, "title": "UN FIORE DI METALLO", "sub": "Punta cava", "src": "Collezione", **img("dumdum/2_openverse.jpg"), "move": "in"},
  {"t": 11.4, "title": "GRANDE COME UN PUGNO", "sub": "Il foro d'uscita", "src": "Ospedale militare", **img(ai("ai_surgery_tent")), "move": "out"},
  {"t": 14.2, "title": "AMPUTATI", "sub": "Braccia e gambe", "src": "Fotografia d'epoca", **img("amputati/2_commons.jpg", "amputati/3_commons.jpg"), "move": "in", "impact": "AMPUTAZIONE", "impact_at": 1.4},
  {"t": 17.6, "title": "DICHIARAZIONE DELL'AIA, 1899", "sub": "Dichiarazione IV, 3", "src": "L'Aia · 29 luglio 1899", "doc": {"head": "DICHIARAZIONE IV, 3", "lines": ["Le Potenze contraenti si impegnano ad astenersi", "dall'uso di proiettili che si espandono", "o si appiattiscono facilmente nel corpo umano."], "stamp": "VIETATO"}},
  {"t": 21.7, "title": "22 CONTRO 1", "sub": "Il voto", "src": "Conferenza dell'Aia", **img("aia_1899/3_commons.jpg"), "move": "in", "impact": "22 – 1", "impact_at": 0.6, "label": ["GRAN BRETAGNA", "contraria"], "label_at": 2.2},
  {"t": 25.4, "title": "1914", "sub": "Accuse reciproche", "src": "Ricostruzione", **img(ai("ai_italian_sentry")), "move": "left"},
  {"t": 32.3, "title": "ANCORA OGGI", "sub": "Vietato tra eserciti", "src": "", **img(ai("ai_police_ammo")), "move": "in", "label": ["POLIZIA", "proiettili espansivi"], "label_at": 3.0},
  {"t": 42.3, "title": "UN UOMO ALLA VOLTA", "sub": "Il limite del dum-dum", "src": "", **img(ai("ai_hague_text")), "move": "out"},
  {"t": 46.7, "title": "DECINE IN UN ISTANTE", "sub": "La prossima arma", "src": "", **img(ai("ai_burning_bunker")), "move": "in"},
 ],
 "ch04_lanciafiamme": [
  {"t": 0, "title": "IL LANCIAFIAMME", "sub": "Malancourt · 26 febbraio 1915", "src": "Fotografia d'epoca", **img("lanciafiamme/3_commons.jpg"), "move": "in", "tag": "1915"},
  {"t": 4.5, "title": "GETTI DI FUOCO", "sub": "Più di 20 metri", "src": "Ricostruzione", **img(ai("ai_flame_jet")), "move": "left", "impact": "20 METRI", "impact_at": 2.6},
  {"t": 9.3, "title": "NON SI SPEGNE", "sub": "Liquido infiammato", "src": "Fotografia d'epoca", **img("lanciafiamme/5_commons.jpg"), "move": "in"},
  {"t": 14.4, "title": "NEI RIFUGI", "sub": "Dove gli uomini si nascondevano", "src": "Ricostruzione", **img(ai("ai_gas_trench")), "move": "out"},
  {"t": 17.0, "title": "L'OPERATORE", "sub": "Il bersaglio più odiato", "src": "Ricostruzione", **img(ai("ai_flame_operator")), "move": "in", "label": ["SERBATOI SULLA SCHIENA", "nessuna via di fuga"], "label_at": 3.0},
  {"t": 25.7, "title": "NESSUN PRIGIONIERO", "sub": "Fronte occidentale", "src": "Fotografia d'epoca", **img("lanciafiamme/4_commons.jpg"), "move": "right"},
  {"t": 28.6, "title": "ANCHE L'ITALIA", "sub": "Reparti lanciafiamme", "src": "Fotografia d'epoca", **img("soldati_italiani/5_commons.jpg"), "move": "in"},
  {"t": 31.6, "title": "LA SORPRESA", "sub": "Mai vietato in battaglia", "src": "", "doc": {"head": "PROTOCOLLO III · CCW", "lines": ["Ginevra, 10 ottobre 1980", "Limita le armi incendiarie", "contro la popolazione civile.", "Contro i soldati: nessun divieto."], "stamp": "LEGALE"}, "impact": "ANCORA LEGALE", "impact_at": 9.5},
  {"t": 43.8, "title": "NESSUN NASCONDIGLIO", "sub": "La prossima arma", "src": "", **img(ai("ai_carso_dawn")), "move": "out"},
 ],
 "ch05_cloro": [
  {"t": 0, "title": "IL CLORO", "sub": "Ypres · 22 aprile 1915", "src": "Dipinto d'epoca", **img("ypres_1915/1_commons.jpg"), "move": "in", "tag": "1915"},
  {"t": 3.8, "title": "MIGLIAIA DI BOMBOLE", "sub": "Lungo il fronte", "src": "Ricostruzione", **img(ai("ai_cylinders")), "move": "left", "label": ["5.730 BOMBOLE", "circa 150 tonnellate di cloro"], "label_at": 1.5},
  {"t": 8.1, "title": "LA NUBE GIALLO-VERDE", "sub": "Verso le trincee francesi", "src": "Ricostruzione", **img(ai("ai_ypres_wind")), "move": "in"},
  {"t": 11.1, "title": "DALL'INTERNO", "sub": "Il cloro nei polmoni", "src": "Fotografia d'epoca", **img("maschera_gas/1_commons.jpg"), "move": "in", "impact": "SOFFOCATI", "impact_at": 3.0},
  {"t": 18.9, "title": "IL FRONTE SI APRE", "sub": "Per chilometri", "src": "Ypres in rovina", **img("ypres_1915/2_openverse.jpg"), "move": "out"},
  {"t": 20.6, "title": "MA ASPETTA", "sub": "Il gas non era già vietato?", "src": "Dichiarazione IV, 2", **{"doc": {"head": "DICHIARAZIONE IV, 2 · 1899", "lines": ["...proiettili che abbiano per UNICO SCOPO", "la diffusione di gas asfissianti..."], "stamp": "PROIETTILI"}}},
  {"t": 29.6, "title": "IL CAVILLO", "sub": "Le bombole non sono proiettili", "src": "", **img("bombole_gas/1_commons.jpg"), "move": "in", "impact": "IL CAVILLO", "impact_at": 1.2},
  {"t": 35.8, "title": "IMPARARE A RICONOSCERLO", "sub": "Colore e odore", "src": "Fotografia d'epoca", **img(ai("ai_mask_drill")), "move": "left"},
 ],
 "ch06_fosgene": [
  {"t": 0, "title": "IL FOSGENE", "sub": "Incolore", "src": "Fabbrica di fosgene · 1918", **img("fosgene/2_commons.jpg"), "move": "in", "tag": "ARCHIVIO"},
  {"t": 1.3, "title": "ODORE DI FIENO", "sub": "Appena tagliato", "src": "Ricostruzione", **img(ai("ai_hay_field")), "move": "left"},
  {"t": 5.6, "title": "SENZA ACCORGERSENE", "sub": "Sentirsi quasi bene", "src": "Ricostruzione", **img(ai("ai_empty_trench")), "move": "in"},
  {"t": 10.8, "title": "ORE DOPO", "sub": "I polmoni si riempiono", "src": "Fotografia d'epoca", **img("ospedale/1_commons.jpg"), "move": "out", "impact": "ANNEGATO", "impact_at": 3.0},
  {"t": 16.5, "title": "UNA REGOLA CRUDELE", "sub": "Medici di trincea", "src": "Ricostruzione", **img(ai("ai_rest_stretcher")), "move": "in", "label": ["IMMOBILE", "anche se sta bene"], "label_at": 4.0},
  {"t": 24.3, "title": "UNO SFORZO", "sub": "E il cuore cedeva", "src": "Fotografia d'epoca", **img("ospedale/3_commons.jpg"), "move": "left"},
  {"t": 28.9, "title": "IL GAS PIÙ LETALE", "sub": "Morti da gas · 1914–1918", "src": "", "doc": {"head": "MORTI DA GAS", "lines": ["Fosgene e difosgene: la grande maggioranza", "Cloro, iprite e altri: il resto"], "stamp": "≈ 85%"}},
  {"t": 32.9, "title": "MONTE SAN MICHELE", "sub": "29 giugno 1916", "src": "Monumento", **img("san_michele/3_commons.jpg"), "move": "in", "label": ["CLORO + FOSGENE", "quella mattina di giugno"], "label_at": 1.0},
  {"t": 37.5, "title": "LE MASCHERE ITALIANE", "sub": "Non bastavano", "src": "Fotografia d'epoca", **img("maschera_gas/4_commons.jpg"), "move": "out"},
  {"t": 42.3, "title": "1917", "sub": "Un gas diverso", "src": "", **img(ai("ai_mustard_mud")), "move": "in", "impact": "INUTILIZZABILE", "impact_at": 4.2},
 ],
 "ch07_iprite": [
  {"t": 0, "title": "L'IPRITE", "sub": "Il gas mostarda · Ypres, luglio 1917", "src": "Fotografia medica d'epoca", **img("iprite/1_commons.jpg"), "move": "in", "tag": "1917"},
  {"t": 5.9, "title": "BASTAVA TOCCARLA", "sub": "Attraverso vestiti e cuoio", "src": "Fotografia medica", **img("iprite/2_commons.jpg"), "move": "left"},
  {"t": 12.3, "title": "VESCICHE", "sub": "Dopo alcune ore", "src": "Tavola medica", **img("iprite/3_commons.jpg"), "move": "in", "impact": "USTIONI", "impact_at": 1.5},
  {"t": 15.3, "title": "CIECHI", "sub": "Per settimane", "src": "Archivio medico militare", **img("iprite/4_commons.jpg"), "move": "out"},
  {"t": 18.8, "title": "NON SPARIVA", "sub": "Nel terreno, nel fango", "src": "Ricostruzione", "doc": {"head": "PERSISTENZA DELL'IPRITE", "lines": ["Nel terreno e nel fango: giorni", "Nelle buche d'acqua: settimane", "Contatto con la pelle: ustioni"], "stamp": "PERICOLO"}},
  {"t": 27.2, "title": "I POSTI DI MEDICAZIONE", "sub": "Infermieri ustionati", "src": "Ricostruzione", **img(ai("ai_hospital_ward")), "move": "left"},
  {"t": 32.1, "title": "LEGATI AI LETTI", "sub": "Il dolore", "src": "Fotografia d'epoca", **img("gassati/2_openverse.jpg"), "move": "in"},
  {"t": 37.6, "title": "LO SCOPO", "sub": "Riempire gli ospedali", "src": "", "doc": {"head": "EFFETTI DELL'IPRITE", "lines": ["Morte sul colpo: rara", "Ricovero: settimane o mesi", "Obiettivo: togliere uomini dal fronte"], "stamp": "MESI"}},
  {"t": 44.1, "title": "IL COLPO PEGGIORE", "sub": "Per l'Italia", "src": "", **img(ai("ai_bovec_valley")), "move": "in"},
 ],
 "ch08_caporetto": [
  {"t": 0, "title": "CONCA DI PLEZZO", "sub": "24 ottobre 1917 · ore 2:00", "src": "Bovec, oggi", **img("plezzo/1_commons.jpg"), "move": "in", "tag": "CAPORETTO"},
  {"t": 5.4, "title": "NOTTE E PIOGGIA", "sub": "La valle", "src": "Ricostruzione", **img("plezzo/3_commons.jpg"), "move": "left"},
  {"t": 7.0, "title": "I LANCIAGAS", "sub": "Centinaia di tubi", "src": "Fotografia d'epoca", **img("gaswerfer/1_commons.jpg", "gaswerfer/2_commons.jpg"), "move": "in", "label": ["GASWERFER", "puntati sulla valle"], "label_at": 1.6},
  {"t": 12.5, "title": "AL SEGNALE", "sub": "Tutti insieme", "src": "Ricostruzione", **img(ai("ai_projectors")), "move": "out"},
  {"t": 14.3, "title": "LA NUBE DI FOSGENE", "sub": "Le maschere non filtrano", "src": "Fotografia d'epoca", **img("gaswerfer/3_commons.jpg"), "move": "in", "impact": "POCHI MINUTI", "impact_at": 5.0},
  {"t": 22.5, "title": "AL LORO POSTO", "sub": "Con il fucile in mano", "src": "Ricostruzione", **img(ai("ai_green_cloud")), "move": "in"},
  {"t": 25.4, "title": "IL FRONTE È VUOTO", "sub": "Le truppe nemiche avanzano", "src": "Illustrazione d'epoca", **img("caporetto/1_commons.jpg"), "move": "left"},
  {"t": 32.2, "title": "COME SE DORMISSERO", "sub": "I sopravvissuti raccontano", "src": "Ricostruzione", **img("soldati_italiani/1_commons.jpg"), "move": "in"},
  {"t": 38.6, "title": "MASCHERE PER IL CLORO", "sub": "Non per il fosgene", "src": "Fotografia d'epoca", **img("caporetto/2_commons.jpg"), "move": "out"},
  {"t": 44.1, "title": "CAPORETTO", "sub": "La più grande disfatta", "src": "Prigionieri italiani · 1917", **img("plezzo/2_openverse.jpg"), "move": "in", "impact": "CAPORETTO", "impact_at": 1.5},
  {"t": 47.8, "title": "DOPO LA GUERRA", "sub": "Fare qualcosa", "src": "Ricostruzione", **img(ai("ai_retreat")), "move": "left"},
 ],
 "ch09_ginevra": [
  {"t": 0, "title": "GINEVRA, 1925", "sub": "Protocollo di Ginevra", "src": "Ginevra · archivio", **img("ginevra_1925/1_commons.jpg"), "move": "in", "tag": "1925"},
  {"t": 2.0, "title": "IL PROTOCOLLO", "sub": "17 giugno 1925", "src": "Ricostruzione", **img(ai("ai_geneva_hall")), "move": "left"},
  {"t": 7.7, "title": "QUALSIASI MODO", "sub": "Non più solo i proiettili", "src": "Protocollo di Ginevra", "doc": {"head": "PROTOCOLLO DI GINEVRA · 1925", "lines": ["Vietato in guerra l'uso di gas asfissianti,", "tossici o simili, e dei mezzi batteriologici."], "stamp": "VIETATO"}, "impact": "CHIUSO", "impact_at": 4.0},
  {"t": 13.1, "title": "IL BILANCIO", "sub": "Guerra chimica · 1914–1918", "src": "", "doc": {"head": "VITTIME DEL GAS", "lines": ["Morti: circa 90.000", "Intossicati: più di 1.000.000"], "stamp": "1918"}, "impact": "90.000", "impact_at": 3.6},
  {"t": 20.9, "title": "PER IL RESTO DELLA VITA", "sub": "Polmoni rovinati", "src": "Ricostruzione", **img(ai("ai_veterans_cough")), "move": "in"},
  {"t": 26.1, "title": "L'EUROPA VEDE", "sub": "Che cos'è una guerra chimica", "src": "Fotografia d'epoca", **img(ai("ai_memorial")), "move": "out"},
  {"t": 30.8, "title": "I REDUCI CIECHI", "sub": "In fila", "src": "Ricostruzione", **img(ai("ai_blind_line")), "move": "in"},
  {"t": 36.2, "title": "IL PUNTO DEBOLE", "sub": "Uso vietato, produzione no", "src": "Ricostruzione", **img(ai("ai_warehouse")), "move": "left", "label": ["MAGAZZINI PIENI", "\"solo per sicurezza\""], "label_at": 6.5},
  {"t": 48.4, "title": "ANCHE L'ITALIA", "sub": "Ratifica · 1928", "src": "", "doc": {"head": "REGNO D'ITALIA", "lines": ["Protocollo di Ginevra", "Firma: 17 giugno 1925", "Ratifica: 3 aprile 1928"], "stamp": "RATIFICATO"}},
  {"t": 54.0, "title": "IL CARSO E CAPORETTO", "sub": "Chi aveva sofferto di più", "src": "", **img("san_michele/4_commons.jpg"), "move": "in"},
  {"t": 58.0, "title": "LA VERITÀ", "sub": "Il dossier finale", "src": "", "doc": {"head": "FASCICOLO RISERVATO", "lines": ["Oggetto: uso del gas dopo la guerra", "Paese: ...", "Anno: ..."], "stamp": "APERTO"}},
 ],
 "ch10_finale": [
  {"t": 0, "title": "ETIOPIA, 1935", "sub": "Guerra d'Etiopia", "src": "Fotografia d'epoca", **img("etiopia_1935/3_commons.jpg"), "move": "in", "tag": "1935", "impact": "ITALIA", "impact_at": 1.2},
  {"t": 3.6, "title": "LA RESISTENZA ETIOPE", "sub": "1935–1936", "src": "Fotografia d'epoca", **img("etiopia_1935/1_openverse.jpg", "etiopia_1935/2_openverse.jpg"), "move": "left"},
  {"t": 5.4, "title": "BOMBE ALL'IPRITE", "sub": "Regia Aeronautica", "src": "Ricostruzione", **img(ai("ai_bombers_1935")), "move": "in", "label": ["IPRITE", "su soldati, villaggi e civili"], "label_at": 1.8},
  {"t": 9.3, "title": "VILLAGGI E CIVILI", "sub": "Altopiano etiope", "src": "Ricostruzione", **img(ai("ai_ethiopia_village")), "move": "out"},
  {"t": 11.0, "title": "LO STESSO GAS", "sub": "18 anni prima", "src": "Fotografia medica · 1917", **img("etiopia_1935/4_commons.jpg"), "move": "in"},
  {"t": 13.5, "title": "NEGATO PER DECENNI", "sub": "1936 – 1996", "src": "Ricostruzione", **img(ai("ai_archive_boxes")), "move": "left"},
  {"t": 16.0, "title": "L'AMMISSIONE", "sub": "Governo italiano · 1996", "src": "", "doc": {"head": "MINISTERO DELLA DIFESA · 1996", "lines": ["Riconosciuto ufficialmente l'impiego", "di aggressivi chimici in Etiopia", "durante la guerra del 1935–1936."], "stamp": "AMMESSO"}, "impact": "1996", "impact_at": 3.0},
  {"t": 21.4, "title": "LA LEZIONE", "sub": "1899 · 1907 · 1925", "src": "", **img("aerei_1935/1_openverse.jpg"), "move": "in"},
  {"t": 23.7, "title": "DUM-DUM, GAS, VELENO", "sub": "Tutti vietati", "src": "", "doc": {"head": "DIVIETI", "lines": ["1899 · proiettili espansivi", "1899 · gas asfissianti", "1907 · veleno e armi avvelenate", "1925 · guerra chimica e batteriologica"], "stamp": "VIETATO"}},
  {"t": 27.2, "title": "FINCHÉ QUALCUNO RISPETTA", "sub": "", "src": "", **{"doc": {"head": "", "lines": ["Un divieto vale solo", "finché qualcuno decide", "di rispettarlo."], "stamp": ""}}, "impact": "CRUDELE", "impact_at": 5.0},
  {"t": 33.6, "title": "ISCRIVITI", "sub": "e attiva la campanella", "src": "", "doc": {"head": "E TU?", "lines": ["Qual era l'arma più crudele di tutte?", "Scrivilo nei commenti."], "stamp": "ISCRIVITI"}},
 ],
}


def card(t, title, sub, head, lines, stamp="", **kw):
    return {"t": t, "title": title, "sub": sub, "src": "", "doc": {"head": head, "lines": lines, "stamp": stamp}, **kw}


# fills used when the AI scenes are not available (keeps every screen under ~10 s)
EXTRA = {
 "ch01_mazze": [card(5.0, "LA TRINCEA", "Spazio per combattere", "TRINCEA · FRONTE ITALIANO", ["Larghezza: circa 1 metro", "Fucile con baionetta: oltre 1,7 metri"], "1 METRO", impact="1 METRO", impact_at=3.0)],
 "ch02_baionetta": [card(17.0, "LA VOCE", "Tra i soldati nemici", "VOCE DAL FRONTE", ["Chi aveva la baionetta a sega", "rischiava di non arrivare vivo", "al campo di prigionia."], "VOCE"),
                    card(33.3, "IL RISULTATO", "Esercito tedesco", "ORDINE · 1917", ["Ritirare la baionetta a sega", "oppure limare i denti"], "RITIRATA")],
 "ch03_dumdum": [card(25.4, "1914", "Accuse reciproche", "AGOSTO 1914", ["Germania: \"gli inglesi usano il dum-dum\"", "Gran Bretagna: \"i tedeschi lo usano\""], "ACCUSE"),
                 card(32.3, "ANCORA OGGI", "Lo stesso principio", "PROIETTILI ESPANSIVI · OGGI", ["Guerra tra eserciti: vietati", "Polizia: permessi in molti paesi", "Motivo: non colpire chi sta dietro"], "OGGI", impact="PERMESSO", impact_at=9.0),
                 card(46.7, "LA PROSSIMA ARMA", "Peggio del dum-dum", "IL PROBLEMA", ["Il dum-dum colpiva un uomo alla volta.", "Serviva qualcosa che ne bruciasse decine."], "?")],
 "ch04_lanciafiamme": [card(4.5, "MALANCOURT", "26 febbraio 1915", "PRIMO ATTACCO", ["Getti di fuoco: oltre 20 metri", "Bersaglio: trincee francesi"], "1915", impact="20 METRI", impact_at=3.0),
                       card(14.4, "IL LIQUIDO", "Non si spegne", "LIQUIDO INFIAMMATO", ["Cola nelle trincee", "Si attacca ai vestiti", "Entra nei rifugi"], "FUOCO"),
                       card(19.3, "L'OPERATORE", "Il bersaglio più odiato", "L'OPERATORE", ["Serbatoi sulla schiena", "Riconoscibile da lontano", "Spesso non veniva fatto prigioniero"], "BERSAGLIO")],
 "ch05_cloro": [{"t": 3.8, "title": "YPRES", "sub": "Il fronte · aprile 1915", "src": "Mappa d'epoca", "images": ["gas_cloud/1_commons.jpg"], "move": "in", "label": ["MIGLIAIA DI BOMBOLE", "lungo il fronte"], "label_at": 1.0},
                {"t": 8.1, "title": "LA NUBE AVANZA", "sub": "Verso le trincee francesi", "src": "Mappa d'epoca", "images": ["gas_cloud/3_commons.jpg"], "move": "left"},
                card(35.8, "RICONOSCERLO", "I soldati imparano", "IL CLORO", ["Colore: giallo-verde", "Odore: pungente"], "CLORO")],
 "ch06_fosgene": [card(1.3, "INVISIBILE", "Il fosgene", "IL FOSGENE", ["Colore: nessuno", "Odore: fieno appena tagliato", "Effetto: ore dopo"], "INVISIBILE"),
                  card(16.5, "UNA REGOLA CRUDELE", "Medici di trincea", "ISTRUZIONI MEDICHE", ["Esposto al gas?", "Restare immobile.", "Anche se ti senti bene."], "IMMOBILE"),
                  card(42.3, "1917", "Un gas diverso", "UN NUOVO OBIETTIVO", ["Non uccidere il nemico,", "ma renderlo inutilizzabile."], "1917", impact="INUTILIZZABILE", impact_at=4.2)],
 "ch07_iprite": [card(27.2, "POSTI DI MEDICAZIONE", "Infermieri ustionati", "POSTO DI MEDICAZIONE", ["Bastava togliere le divise ai feriti", "per ustionarsi le mani."], "CONTAMINATO"),
                 card(44.1, "IL COLPO PEGGIORE", "Per l'Italia", "FRONTE ITALIANO · 1917", ["Il colpo più devastante", "doveva ancora arrivare."], "1917")],
 "ch08_caporetto": [card(22.5, "AL LORO POSTO", "In pochi minuti", "CONCA DI PLEZZO", ["Centinaia di morti in pochi minuti,", "ancora al loro posto,", "con il fucile in mano."], "PLEZZO"),
                    card(47.8, "DOPO LA GUERRA", "Fare qualcosa", "1918", ["Davanti a tutto questo,", "il mondo decide di intervenire."], "1918")],
 "ch09_ginevra": [card(20.9, "I SOPRAVVISSUTI", "Per il resto della vita", "DOPO IL GAS", ["Tosse per tutta la vita", "Polmoni rovinati per sempre"], "1918"),
                  card(26.1, "L'EUROPA VEDE", "La guerra chimica", "OPINIONE PUBBLICA", ["Per la prima volta l'Europa vede", "che cosa significa una guerra chimica."], "1919"),
                  card(30.8, "I REDUCI CIECHI", "In fila", "NELLE CITTÀ", ["I reduci ciechi arrivano in fila,", "una mano sulla spalla di chi è davanti."], "CIECHI"),
                  card(36.2, "IL PUNTO DEBOLE", "Uso vietato, produzione no", "PROTOCOLLO · IL LIMITE", ["Uso del gas: vietato", "Produzione: permessa", "Scorte nei magazzini: permesse"], "PERMESSO", impact="MAGAZZINI PIENI", impact_at=6.5)],
}
for k, v in EXTRA.items():
    SHOTS[k] = sorted(SHOTS[k] + v, key=lambda x: x["t"])

# join narration with short breaths between chapters
parts, off, shots = [], 0.0, []
for c in CH:
    path = os.path.join(A, "narration_audio", c + ".flac")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                               capture_output=True, text=True).stdout)
    for s in SHOTS[c]:
        s = dict(s)
        if any(not os.path.exists(os.path.join(A, q)) for q in s.get("images", [])):
            if s["t"] == 0:
                sys.exit(f"Falta a imagem de abertura do capítulo {c}")
            print("sem imagem, plano retirado:", s["title"])
            continue
        s["t"] = round(off + s["t"] + (0 if s["t"] == 0 or c == "ch00_hook" else -0.1), 3)
        shots.append(s)
    parts.append((path, dur))
    off += dur + GAP

cmd, fl = ["ffmpeg", "-v", "error", "-y"], ""
for i, (p, _) in enumerate(parts):
    cmd += ["-i", p]
    fl += f"[{i}:a]aformat=sample_rates=44100:channel_layouts=mono,apad=pad_dur={GAP}[a{i}];"
fl += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[out]"
subprocess.run(cmd + ["-filter_complex", fl, "-map", "[out]", os.path.join(A, "full.flac")], check=True)

# no image may appear twice
seen = {}
for s in shots:
    for p in s.get("images", []):
        if p in seen:
            sys.exit(f"Imagem repetida: {p} ({seen[p]} e {s['title']})")
        seen[p] = s["title"]
        if not os.path.exists(os.path.join(A, p)):
            print("FALTA:", p)
json.dump({"fps": 30, "audio": "full.flac", "start": 0, "end": round(off - GAP + 0.6, 2), "shots": shots},
          open(os.path.join(A, "episode.json"), "w"), indent=1, ensure_ascii=False)
print(f"{len(shots)} planos · {off - GAP:.1f}s · {len(seen)} imagens diferentes")
