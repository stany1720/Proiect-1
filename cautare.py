from typing import List, Dict, Any, Optional

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
                print(f"Angajatul cautat este: {angajat}")
                return angajat

        print("Angajatul cautat nu a fost gasit! \n1. Incercati din nou \nsau \n2. Iesiti din program.")
        select_caut = input("Selectati o optiune de mai sus: ")
        if select_caut == "1":
            continue
        elif select_caut == "2":
            print("Am inchis programul! ")
            break
