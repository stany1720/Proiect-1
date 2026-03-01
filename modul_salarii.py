import os
from typing import List, Dict, Any
import cautare

Angajat = Dict[str, Any]
ListaAngajati = List[Angajat]

def calcul_total_salarii_comp(angajati: ListaAngajati) -> None:
    """
    Calculeaza si afiseaza totalul salariilor brute din companie.

    Functia parcurge lista angajatilor si insumeaza
    valorile campului 'Salar'.

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    total_salarii_comp = []
    for angajat in angajati:
        total_salarii_comp.append(angajat['Salar'])
        total = sum(total_salarii_comp)
    return print(f"Total salariilor din companie este de {total} RON. ")

def calcul_total_salarii_dep(angajati: ListaAngajati) -> None:
    """
    Calculeaza si afiseaza totalul salariilor brute per departament.

    Creeaza un dictionar in care:
        - cheia reprezinta departamentul
        - valoarea reprezinta suma salariilor din acel departament

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    dictionar_angajati = {}

    for angajat in angajati:
        departament = angajat['Departament']
        salar = float(angajat['Salar'])
        if departament in dictionar_angajati:
            dictionar_angajati[departament] += salar
        else:
            dictionar_angajati[departament] = salar

    if not dictionar_angajati:
        pass
    else:
        for departament, total in dictionar_angajati.items():
            print(f"Departamentul {departament}: {total} RON.")

def calcul_fluturas_salar(angajati: ListaAngajati) -> None:
    """
    Calculeaza si afiseaza fluturasul de salariu pentru un angajat.

    Pe baza salariului brut se calculeaza:
        - CAS (10%)
        - CASS (25%)
        - Venitul impozabil
        - Impozitul (10%)
        - Salariul net

    Angajatul este identificat prin CNP, utilizand functia
    cautare.cautare_angajat().

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    angajat_gasit = cautare.cautare_angajat(angajati)
    if angajat_gasit is None:
        return

    brut = angajat_gasit['Salar']
    cas = brut * 0.10
    cass = brut * 0.25
    impozabil = brut - cas - cass
    impozit = impozabil * 0.10
    net = impozabil - impozit

    return print(f'''Pentru angajatul {angajat_gasit['Nume']} {angajat_gasit['Prenume']},
--------------------------------
Salariul brut este de {brut} RON
--------------------------------
CAS-ul este de {cas} RON, 
--------------------------------
CASS-ul este de {cass} RON, 
--------------------------------
Impozitul este de {impozit} RON 
--------------------------------
Salariul net este de {net} RON''')

def export_fluturasi(angajati: ListaAngajati) -> None:
    """
    Genereaza un fisier TXT continand fluturasul de salariu
    pentru angajatul selectat.

    Fisierul este salvat in directorul:
        Proiect 1/salarii/

    Daca directorul nu exista, acesta este creat automat.

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor.

    Returns:
        None
    """
    path_director = r"Proiect 1\salarii"
    if not os.path.exists(path_director):
        os.makedirs(path_director)
    angajat_gasit = cautare.cautare_angajat(angajati)
    if angajat_gasit is None:
        return
    brut = angajat_gasit['Salar']
    cas = brut * 0.10
    cass = brut * 0.25
    impozabil = brut - cas - cass
    impozit = impozabil * 0.10
    net = impozabil - impozit
    nume_fisier = f"salarii/fluturas_{angajat_gasit['CNP']}.txt"
    date_salariu = {
        "Nume": angajat_gasit['Nume'],
        "Prenume": angajat_gasit['Prenume'],
        "CNP": angajat_gasit['CNP'],
        "Salariul Brut": brut,
        "CAS": cas,
        "CASS": cass,
        "Impozabil": impozabil,
        "Impozit": impozit,
        "Salariu Net": net
    }
    with open(nume_fisier, 'w', encoding='utf-8') as fluturas_salariu:
        fluturas_salariu.write(f'''Pentru angajatul {date_salariu['Nume']} {date_salariu['Prenume']},
--------------------------------
Salariul brut este de {brut} RON
--------------------------------
CAS-ul este de {cas} RON
--------------------------------
CASS-ul este de {cass} RON
--------------------------------
Impozitul este de {impozit} RON
--------------------------------
Salariul net este de {net} RON'''
        )
 