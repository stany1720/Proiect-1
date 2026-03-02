from typing import List, Dict, Any, Optional
import display

Angajat = Dict[str, Any]
ListaAngajati = List[Angajat]

def cautare_angajat(angajati: ListaAngajati) -> Optional[Angajat]:
    """
    Cauta un angajat in lista pe baza CNP-ului introdus de utilizator.

    Functia solicita introducerea CNP-ului si parcurge lista
    angajatilor pentru a identifica o potrivire exacta.

    Daca angajatul este gasit:
        - este afisat in consola
        - este returnat sub forma de dictionar

    Daca angajatul nu este gasit:
        - utilizatorul poate reintroduce CNP-ul
        - sau poate iesi din procesul de cautare

    Args:
        angajati (ListaAngajati): Lista tuturor angajatilor existenti.

    Returns:
        Optional[Angajat]:
            - Angajat (dict) daca este gasit
            - None daca utilizatorul alege sa iasa
    """
    while True:
        cnp_cautat = input("Introdu CNP-ul angajatului cautat: ")
        for angajat in angajati:
            if cnp_cautat == angajat['CNP']:
                display.succes(f"Angajatul cautat este: {angajat['Nume']} {angajat['Prenume']} | {angajat['CNP']} | {angajat['Varsta']} | {angajat['Salar']} | {angajat['Departament']} | {angajat['Senioritate']} \n")
                return angajat

        display.eroare("Angajatul cautat nu a fost gasit! \n1. Incercati din nou \nsau \n2. Iesiti din program.")
        select_caut = input("Selectati o optiune de mai sus: ")
        if select_caut == "1":
            continue
        elif select_caut == "2":
            display.info("Am inchis programul! ")
            break
