import sys
from constraint import Problem


def add_adjacency_constraints(problem, adjacency_list):
    """Fügt für jedes benachbarte Länderpaar eine Constraint hinzu:
    die Farben der beiden Länder müssen verschieden sein."""
    already_added = set()
    for state, neighbors in adjacency_list.items():
        for neighbor in neighbors: # Für jedes benachbarte Land
            # Jedes Paar nur einmal hinzufügen (Reihenfolge egal)
            pair = tuple(sorted([state, neighbor])) 
            if pair not in already_added:
                problem.addConstraint(lambda x, y: x != y, pair) # Farben müssen verschieden sein
                already_added.add(pair) # Paar als hinzugefügt markieren


def solve(num_colors):
    """Versucht, eine Färbung mit `num_colors` Farben zu finden.
    Gibt die Liste aller Lösungen zurück (leer = keine Lösung)."""
    problem = Problem()

    # Wertebereich: Farben
    if num_colors == 3:
        domain = ["Grün", "Rot", "Blau"]
    else:
        domain = ["Grün", "Rot", "Blau", "Gelb"]

    # Variablen: die 16 deutschen Bundesländer
    states = [
        "Baden-Württemberg", "Bayern", "Saarland", "Hessen", "Thüringen",
        "Sachsen", "Nordrhein-Westfalen", "Niedersachsen", "Sachsen-Anhalt",
        "Brandenburg", "Mecklenburg-Vorpommern", "Schleswig-Holstein",
        "Bremen", "Hamburg", "Berlin", "Rheinland-Pfalz"
    ]

    # Nachbarschaftsliste: welche Länder teilen eine Grenze?
    adjacency_list = {
        "Baden-Württemberg":       ["Bayern", "Hessen", "Rheinland-Pfalz"],
        "Bayern":                  ["Baden-Württemberg", "Hessen", "Thüringen", "Sachsen"],
        "Saarland":                ["Rheinland-Pfalz"],
        "Hessen":                  ["Baden-Württemberg", "Bayern", "Rheinland-Pfalz",
                                    "Nordrhein-Westfalen", "Thüringen", "Niedersachsen"],
        "Thüringen":               ["Bayern", "Sachsen", "Sachsen-Anhalt",
                                    "Niedersachsen", "Hessen"],
        "Sachsen":                 ["Bayern", "Thüringen", "Sachsen-Anhalt", "Brandenburg"],
        "Nordrhein-Westfalen":     ["Hessen", "Rheinland-Pfalz", "Niedersachsen"],
        "Niedersachsen":           ["Bremen", "Hamburg", "Schleswig-Holstein",
                                    "Mecklenburg-Vorpommern", "Brandenburg",
                                    "Sachsen-Anhalt", "Thüringen", "Hessen",
                                    "Nordrhein-Westfalen"],
        "Sachsen-Anhalt":          ["Niedersachsen", "Thüringen", "Sachsen",
                                    "Brandenburg"],
        "Brandenburg":             ["Sachsen", "Sachsen-Anhalt",
                                    "Mecklenburg-Vorpommern", "Berlin",
                                    "Niedersachsen"],
        "Mecklenburg-Vorpommern":  ["Schleswig-Holstein", "Niedersachsen", "Brandenburg"],
        "Schleswig-Holstein":      ["Niedersachsen", "Mecklenburg-Vorpommern", "Hamburg"],
        "Bremen":                  ["Niedersachsen"],
        "Hamburg":                 ["Niedersachsen", "Schleswig-Holstein"],
        "Berlin":                  ["Brandenburg"],
        "Rheinland-Pfalz":         ["Saarland", "Baden-Württemberg", "Hessen",
                                    "Nordrhein-Westfalen"],
    }

    problem.addVariables(states, domain)
    add_adjacency_constraints(problem, adjacency_list)

    return problem.getSolutions()


def main():
    # Zuerst mit 3 Farben versuchen
    print("=" * 55) 
    print("Teste mit 3 Farben (Grün, Rot, Blau)...")
    solutions_3 = solve(3)

    if solutions_3:
        print(f"✓ 3 Farben GENÜGEN! ({len(solutions_3)} Lösungen gefunden)")
        print("\nBeispiel-Lösung:")
        example = solutions_3[0] # Einfach die erste gefundene Lösung nehmen
        for state in sorted(example):
            print(f"  {state:<30} → {example[state]}") # Sortieren für bessere Lesbarkeit
    else:
        print("✗ 3 Farben genügen NICHT.")
        print("\nTeste mit 4 Farben (Grün, Rot, Blau, Gelb)...")
        solutions_4 = solve(4)
        if solutions_4:
            print(f"✓ 4 Farben GENÜGEN! ({len(solutions_4)} Lösungen gefunden)")
            print("\nBeispiel-Lösung:")
            example = solutions_4[0]
            for state in sorted(example):
                print(f"  {state:<30} → {example[state]}")
        else:
            print("✗ Auch 4 Farben genügen nicht – das sollte nicht passieren!")

    print("=" * 55)


if __name__ == "__main__":
    main()