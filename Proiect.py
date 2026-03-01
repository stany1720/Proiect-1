from typing import List, Dict, Any
import csv
import json
import cautare
import modul_salarii

"""
Aplicatie de management a angajatilor.

Aplicatia permite:
    - Adaugarea angajatilor
    - Cautarea angajatilor dupa CNP
    - Modificarea datelor angajatilor
    - Stergerea angajatilor
    - Exportarea listelor in CSV
    - Calcularea costurilor salariale
    - Generarea fluturasilor de salariu

Datele sunt persistate in fisier JSON (angajati.json),
iar exporturile se realizeaza in format CSV si TXT.

Structura aplicatiei este modulara:
    - cautare.py
    - modul_salarii.py
    - fisier principal (meniu si orchestrare)

Autor: [Mihai-Adrian Stanislav]
"""

cifre = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

Angajat = Dict[str, Any]
ListaAngajati = List[Angajat]


def salvare(angajati: ListaAngajati) -> None:
    """
    Salveaza lista angajatilor in fisierul JSON de persistenta.

    Functia suprascrie fisierul 'angajati.json' cu datele curente
    ale listei de angajati, folosind format JSON indentat
    pentru lizibilitate.

    Args:
        angajati (ListaAngajati): Lista actualizata a angajatilor.

    Returns:
        None
    """
    with open("angajati.json", "w", encoding='utf8') as file_angajati:
        json.dump(angajati, file_angajati, indent=4)

def adaugare_angajat(angajati: ListaAngajati) -> None:
    """
    Adauga un angajat nou in sistem.

    Functia:
        - Solicita datele angajatului prin input interactiv
        - Valideaza fiecare camp (nume, prenume, CNP, varsta, salariu)
        - Previne duplicarea CNP-ului
        - Permite selectarea sau crearea unui departament
        - Permite alegerea nivelului de senioritate

    Daca toate validarile sunt indeplinite, angajatul este
    adaugat in lista transmisa ca argument.

    Args:
        angajati (ListaAngajati): Lista existenta a angajatilor.

    Returns:
        None
    """
    while True:
        nume = input("Introdu numele de familie: ").strip().title()
        if nume.isalpha() and nume != '':
            nume = nume.title()
            break
        else:
            print("Numele trebuie sa contina doar litere. \nIncercati din nou.")
    while True:
        prenume = input("Introdu numele mic: ").strip().title()
        if prenume.isalpha() and prenume != '':
            prenume = prenume.title()
            break
        else:
            print("Prenumele trebuie sa contina doar litere. \nIncercati din nou.")
    while True:
        cnp = input("Introdu doar cifrele CNP-ului: ").strip()
        cnp_existente = {angajat['CNP'] for angajat in angajati}
        if (cnp.isdigit() and len(cnp) == 13 and cnp not in cnp_existente):
            break
        else:
            print(
                "CNP-ul trebuie sa aiba 13 cifre si sa contina doar cifre.\n"
                "Nu pot exista doi angajati cu acelasi CNP.\n"
                "Incercati din nou.")
    while True:
        varsta = input("Introdu varsta: ").strip()
        validare_varsta = True
        for caracter in varsta:
            if caracter not in cifre:
                validare_varsta = False
        if validare_varsta and varsta != '' and int(varsta) >= 18:
            varsta = int(varsta)
            break
        else:
            print(
                "Varsta trebuie sa contina numai cifre. \nVarsta minima pentru angajare este 18 ani.")
    while True:
        salar = input("Introdu salarul angajatului: ").strip()
        if salar.isdigit() and int(salar) >= 4050:
            salar = int(salar)
            break
        else:
            print("Salariul trebuie sa contina doar cifre. \nSalariul trebuie sa fie macar egal cu salariul minim pe economie, adica 4050 RON brut \nIncercati din nou.")
            continue
    lista_departamente = []
    for angajat in angajati:
        lista_departamente.append(angajat['Departament'])
        rezultat = set(lista_departamente)
    print(rezultat)
    while True:
        select_departament = input(
            "Selecteaza departamentul din optiunile de mai sus:").strip()
        if select_departament in rezultat:
            departament = select_departament
            break
        else:
            print("Doriti sa creati un departamentr nou? \n1. DA \nsau \n2. NU")
            raspuns = input("Alegeti un raspuns de mai sus. ")
            if raspuns == "1":
                departament = select_departament
                break
            elif raspuns == "2":
                continue
            else:
                print(
                    "Optiunea selectata nu corespunde cu optiunile prezente. \nVa rugam incercati din nou.")
    print("""Introdu senioritatea angajatului:
1. Junior
2. Mid
3. Senior
        """)
    select_senior = input("Selecteaza senioritatea din optiunile de mai sus:")
    while True:
        if select_senior == "1":
            senioritate = "Junior"
            break
        elif select_senior == "2":
            senioritate = "Mid"
            break
        elif select_senior == "3":
            senioritate = "Senior"
            break
        else:
            print(
                "Optiunea selectata nu corespunde cu optiunile prezente. \nVa rugam incercati din nou.")
    angajat = {
        "Nume": nume,
        "Prenume": prenume,
        "CNP": cnp,
        "Varsta": varsta,
        "Salar": salar,
        "Departament": departament,
        "Senioritate": senioritate
    }
    print(f"Angajatul adaugat este: {angajat}")
    angajati.append(angajat)
    return

def modificare_angajat(angajati: ListaAngajati) -> None:
    """
    Permite modificarea datelor unui angajat existent.

    Angajatul este identificat prin CNP utilizand
    functia cautare.cautare_angajat().

    Utilizatorul poate modifica:
        - CNP (cu validare si prevenire duplicare)
        - Nume
        - Prenume
        - Varsta
        - Salariu
        - Departament
        - Senioritate

    Fiecare modificare este salvata imediat in fisierul JSON.

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    angajat_gasit = cautare.cautare_angajat(angajati)
    if angajat_gasit is None:
        return
    while True:
        print("""Ce campuri doriti sa modificati?
        1) CNP
        2) Nume
        3) Prenume
        4) Varsta
        5) Salar
        6) Departament
        7) Senioritate (junior, mid, senior)
        8) Oprire modificari
        """)
        select_mod = input("Alegeti o optiune de mai sus: ")
        if select_mod == "1":
            while True:
                cnp_existente = {angajat['CNP'] for angajat in angajati if angajat != angajat_gasit}
                cnp_nou = input("Corectati CNP-ul angajatului: ").strip()
                if (cnp_nou.isdigit() and len(cnp_nou) == 13 and cnp_nou not in cnp_existente):
                    angajat_gasit['CNP'] = cnp_nou
                    print("Validare reusita.")
                    salvare(angajati)
                    break
                else:
                    print("CNP-ul trebuie sa aiba 13 cifre si sa contina doar cifre.")
                    print("Atentie, nu pot exista 2 angajati cu acelasi CNP.")
                    print("Incercati din nou.")
            print(
                f"{angajat_gasit['Nume']} are acum CNP-ul: {angajat_gasit['CNP']}.")
            print("Ce alte campuri mai doresti sa editezi? ")
            continue
        elif select_mod == "2":
            while True:
                nume_nou = input(
                    "Modificati numele angajatului: ")
                if nume_nou.isalpha() and nume_nou != '':
                    angajat_gasit['Nume'] = nume_nou.title()
                    salvare(angajati)
                    break
                else:
                    print("Numele trebuie sa contina doar litere. \nIncercati din nou.")
                print(
                    f"{angajat_gasit['CNP']} are acum numele: {angajat_gasit['Nume']}.")
                print("Ce alte campuri mai doresti sa editezi? ")
        elif select_mod == "3":
            while True:
                prenume_nou = input(
                    "Modificati prenumele angajatului: ")
                if prenume_nou.isalpha() and prenume_nou != '':
                    angajat_gasit['Prenume'] = prenume_nou.title()
                    salvare(angajati)
                    break
                else:
                    print(
                        "Prenumele trebuie sa contina doar litere. \nIncercati din nou.")
                print(
                    f"{angajat_gasit['Nume']} are acum prenumele: {angajat_gasit['Prenume']}.")
                print("Ce alte campuri mai doresti sa editezi? ")
                continue
        elif select_mod == "4":
            while True:
                angajat_gasit['Varsta'] = input(
                    "Modificati varsta angajatului: ")
                validare_varsta = True
                for caracter in angajat_gasit['Varsta']:
                    if caracter not in cifre:
                        validare_varsta = False
                if validare_varsta and angajat_gasit['Varsta'] != '' and int(angajat_gasit['Varsta']) >= 18:
                    angajat_gasit['Varsta'] = int(angajat_gasit['Varsta'])
                    salvare(angajati)
                    break
                else:
                    print(
                        "Varsta trebuie sa contina numai cifre. \nVarsta minima pentru angajare este 18 ani.")
            print(
                f"{angajat_gasit['Nume']} are acum varsta de {angajat_gasit['Varsta']} ani.")
            print("Ce alte campuri mai doresti sa editezi? ")
            continue
        elif select_mod == "5":
            while True:
                angajat_gasit['Salar'] = input(
                    "Modificati salariul angajatului: ")
                if angajat_gasit['Salar'].isdigit() and int(angajat_gasit['Salar']) >= 4050:
                    angajat_gasit['Salar'] = int(angajat_gasit['Salar'])
                    salvare(angajati)
                    break
                else:
                    print("Salariul trebuie sa contina doar cifre. \nSalariul trebuie sa fie macar egal cu salariul minim pe economie, adica 4050 RON brut \nIncercati din nou.")

            print(
                f"{angajat_gasit['Nume']} are acum salariul de {angajat_gasit['Salar']} RON.")
            print("Ce alte campuri mai doresti sa editezi? ")
            continue
        elif select_mod == "6":
            lista_departamente = []
            for angajat in angajati:
                lista_departamente.append(angajat['Departament'].upper())
                rezultat = set(lista_departamente)
            print(f'Departamentele disponibile sunt: {rezultat}')
            while True:
                departament = input(
                    "La ce departament doresti sa transferi angajatul? ").upper()
                if departament.upper() in rezultat:
                    angajat_gasit['Departament'] = departament
                    salvare(angajati)
                    break
                else:
                    print("Alegeti un departament din cele de mai sus.")
            print(
                f"{angajat_gasit['Nume']} a fost transferat la departamentul: {angajat_gasit['Departament']}.")
            print("Ce alte campuri mai doresti sa editezi? ")
            continue
        elif select_mod == "7":
            lista_senioritate = []
            for angajat in angajati:
                lista_senioritate.append(angajat['Senioritate'].upper())
                rezultat = set(lista_senioritate)
            print(f'Senioritatile disponibile sunt: {rezultat}')
            while True:
                senioritate = input(
                    "Ce senioritate doresti sa-i atribui angajatului? ").upper()
                if senioritate.upper() in rezultat:
                    angajat_gasit['Senioritate'] = senioritate
                    salvare(angajati)
                    break
                else:
                    print("Alegeti un nivel de senioritate din cele de mai sus.")
            print(
                f"{angajat_gasit['Nume']} are acum senioritatea: {angajat_gasit['Senioritate']}")
            print("Ce alte campuri mai doresti sa editezi? ")
            continue
        elif select_mod == "8":
            print("Am iesit din sectiunea de modificari! ")
            return
        else:
            print("Selectia nu corespunde nici unei optiuni. \nInceraca din nou.")
            continue

def stergere_angajat(angajati: ListaAngajati) -> None:
    """
    Sterge un angajat din sistem.

    Angajatul este identificat prin CNP.
    Inainte de stergere, utilizatorul trebuie sa confirme actiunea.

    Dupa confirmare:
        - Angajatul este eliminat din lista
        - Modificarea este salvata in fisierul JSON

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    angajat_gasit = cautare.cautare_angajat(angajati)
    if angajat_gasit is None:
        return
    while True:
        confirmare = input(
            "Sunteti sigur ca doriti sa stergeti acest angajat? \n1. DA \n2. NU \nAlegeti: ")
        if confirmare == "1":
            angajati.remove(angajat_gasit)
            print("Angajatul a fost sters din sistem")
            salvare(angajati)
            break
        elif confirmare == "2":
            return

def afisare_angajati(angajati: ListaAngajati) -> None:
    """
    Afiseaza si exporta lista completa a angajatilor.

    Functia:
        - Scrie lista angajatilor in fisierul CSV 'lista_angajati.csv'
        - Afiseaza fiecare angajat in consola

    Fisierul generat contine urmatoarele campuri:
        Nume, Prenume, CNP, Varsta, Salar, Departament, Senioritate

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    print('Lista angajatilor firmei a fost exportata in fisierul: lista_angajati.csv')
    print('Lista angajatilor firmei, este dupa cum urmeaza:...')
    with open('lista_angajati.csv', "w", newline='', encoding='utf-8') as lista_angajati:
        antet = (["Nume", "Prenume", "CNP", "Varsta",
                 "Salar", "Departament", "Senioritate"])
        dict_writer = csv.DictWriter(lista_angajati, fieldnames=antet)
        dict_writer.writeheader()
        for salariat in angajati:
            dict_writer.writerow(salariat)
            print(salariat)

def afisare_angajati_dupa_senioritate(angajati: ListaAngajati) -> None:
    """
    Afiseaza si exporta angajatii filtrati dupa senioritate.

    Functia:
        - Identifica nivelurile de senioritate existente
        - Permite selectarea unuia
        - Exporta rezultatul in fisierul CSV
          'lista_angajati_senioritate.csv'

    Doar angajatii corespunzatori senioritatii selectate
    sunt afisati si salvati.

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    lista_senioritate = []
    for angajat in angajati:
        lista_senioritate.append(angajat['Senioritate'].upper())
        rezultat = set(lista_senioritate)
    print(f'Senioritatile disponibile sunt: {rezultat}')
    while True:
        senioritate = input("Ce senioritate cauti? ").upper()
        gasit = False
        with open('lista_angajati_senioritate.csv', "w", newline='', encoding='utf-8') as angajati_sen:
            antet = (["Nume", "Prenume", "CNP", "Varsta",
                     "Salar", "Departament", "Senioritate"])
            dict_writer = csv.DictWriter(angajati_sen, fieldnames=antet)
            dict_writer.writeheader()
            for angajat in angajati:
                if angajat['Senioritate'].upper() == senioritate and senioritate in lista_senioritate:
                    print(angajat)
                    dict_writer.writerow(angajat)
                    gasit = True
        if gasit:
            return
        else:
            print("Alegeti un nivel de senioritate din cele se mai sus.")

def afisare_angajati_dupa_departament(angajati: ListaAngajati) -> None:
    """
    Afiseaza si exporta angajatii filtrati dupa departament.

    Functia:
        - Identifica departamentele existente
        - Permite selectarea unuia
        - Exporta rezultatul in fisierul CSV
          'lista_angajati_departament.csv'

    Doar angajatii din departamentul selectat
    sunt afisati si salvati.

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    lista_departamente = []
    for angajat in angajati:
        lista_departamente.append(angajat['Departament'].upper())
        rezultat = set(lista_departamente)
    print(f'Departamentele disponibile sunt: {rezultat}')
    while True:
        departament = input("Ce departament cauti? ").upper()
        gasit = False
        with open('lista_angajati_departament.csv', "w", newline='', encoding='utf-8') as angajati_dep:
            antet = (["Nume", "Prenume", "CNP", "Varsta",
                     "Salar", "Departament", "Senioritate"])
            dict_writer = csv.DictWriter(angajati_dep, fieldnames=antet)
            dict_writer.writeheader()
            for angajat in angajati:
                if angajat['Departament'].upper() == departament and departament in lista_departamente:
                    print(angajat)
                    dict_writer.writerow(angajat)
                    gasit = True
        if gasit:
            return
        else:
            print("Alegeti un departament din cele se mai sus.")

while True:
    """
Bucla principala a aplicatiei.

Responsabila pentru:
    - Incarcarea datelor din fisierul JSON
    - Afisarea meniului principal
    - Directionarea catre functionalitatile aplicatiei
    - Oprirea programului la selectarea optiunii de iesire
"""
    try:
        with open("angajati.json", "r", encoding='utf8') as fisier_angajati:
            angajati = json.load(fisier_angajati)
    except FileNotFoundError:
        print('Fisierul cu angajatii, nu a fost gasit... \nInitializez programul in modul "0"... \nCreez o lista noua de angajati pentru tine... ')
        angajati = []
        print('Noua lista de angajati a fost creata cu succes si poate fi populata! \nAcum puteti sa va bucurati de program.')
    print("""
    1) Adaugare angajat
    2) Cautare angajat (dupa CNP)
    3) Modificare date angajat (dupa CNP)
    4) Stergere angajat (dupa CNP)
    5) Afisare angajati
    6) Calcul cost total salarii companie
    7) Calcul cost total salarii departament
    8) Calcul fluturas salar angajat (dupa CNP)
    9) Export fluturas salariu
    10) Afisarea angajatilor pe baza senioritatii
    11) Afisarea angajatilor pe baza departamentului
    12) Iesire
    """)

    selectie = input("Selectati o actiune de mai sus: ")

    if selectie == "1":
        adaugare_angajat(angajati)
        salvare(angajati)
    elif selectie == "2":
        cautare.cautare_angajat(angajati)
    elif selectie == "3":
        modificare_angajat(angajati)
    elif selectie == "4":
        stergere_angajat(angajati)
    elif selectie == "5":
        afisare_angajati(angajati)
    elif selectie == "6":
        modul_salarii.calcul_total_salarii_comp(angajati)
    elif selectie == "7":
        modul_salarii.calcul_total_salarii_dep(angajati)
    elif selectie == "8":
        modul_salarii.calcul_fluturas_salar(angajati)
    elif selectie == "9":
        modul_salarii.export_fluturasi(angajati)
    elif selectie == "10":
        afisare_angajati_dupa_senioritate(angajati)
    elif selectie == "11":
        afisare_angajati_dupa_departament(angajati)
    elif selectie == "12":
        print("Ati iesit din program!")
        break
