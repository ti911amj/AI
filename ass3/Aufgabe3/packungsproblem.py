from constraint import Problem


def get_positions(groesse_grosses_rechteck, width, height):
    """Berechnet alle gültigen Platzierungen für ein Rechteck der Größe width x height
    im großen Rechteck. Jede Platzierung ist ein Tupel:
      (x, y, ausrichtung, breite, hoehe)
    wobei x/y die obere linke Ecke ist.

    Ausrichtung 'h' = horizontal (width entlang x-Achse)
    Ausrichtung 'v' = vertikal   (height entlang x-Achse, also gedreht)
    """
    W, H = groesse_grosses_rechteck
    positions = []

    # Horizontale Platzierung: Rechteck liegt so wie angegeben
    # Es muss gelten: x + width <= W  und  y + height <= H
    for x in range(0, W - width + 1):       # +1 wegen range (exklusives Ende)
        for y in range(0, H - height + 1):
            positions.append((x, y, "h", width, height)) # x und y sind die Koordinaten der oberen linken Ecke, "h" für horizontal, und die Originalbreite und -höhe

    # Vertikale Platzierung (gedreht): Breite und Höhe tauschen
    # Nur hinzufügen, wenn das Rechteck nicht quadratisch ist (sonst doppelt)
    if width != height:
        for x in range(0, W - height + 1):  # jetzt height entlang x
            for y in range(0, H - width + 1):
                positions.append((x, y, "v", width, height))

    return positions


def overlaps(p1, p2):
    """Prüft, ob zwei Platzierungen sich überschneiden.
    Jede Platzierung: (x, y, ausrichtung, orig_width, orig_height)
    """
    x1, y1, a1, w1, h1 = p1 # x/y = obere linke Ecke, a = Ausrichtung, w/h = Originalbreite und -höhe
    x2, y2, a2, w2, h2 = p2 

    # Tatsächliche Ausdehnung je nach Ausrichtung
    # 'h': Rechteck liegt so wie angegeben → dx=w, dy=h
    # 'v': Rechteck ist gedreht            → dx=h, dy=w
    dx1 = w1 if a1 == "h" else h1  #dx1 = Breite entlang x-Achse 
    dy1 = h1 if a1 == "h" else w1  #dy1 = Höhe entlang y-Achse
    dx2 = w2 if a2 == "h" else h2
    dy2 = h2 if a2 == "h" else w2

    # Zwei Rechtecke überschneiden sich, wenn sie sich in BEIDEN Achsen überlappen.
    # Sie überschneiden sich NICHT, wenn eines vollständig links/rechts/oben/unten
    # vom anderen liegt.
    no_overlap_x = (x1 + dx1 <= x2) or (x2 + dx2 <= x1) # wenn p1 komplett links von p2 oder p2 komplett links von p1 dann überlappen sie sich nicht in x-Richtung
    no_overlap_y = (y1 + dy1 <= y2) or (y2 + dy2 <= y1) # wenn p1 komplett über p2 oder p2 komplett über p1 dann überlappen sie sich nicht in y-Richtung

    return not (no_overlap_x or no_overlap_y)


def packungsproblem(groesse_grosses_rechteck, kleine_rechtecke):
    """Löst das Packungsproblem als CSP.

    Variablen: Indizes 0..N-1, eine pro kleinem Rechteck
    Werte:     Alle gültigen Platzierungen des jeweiligen Rechtecks im großen Rechteck
    Constraints: Je zwei Rechtecke dürfen sich nicht überschneiden
    """
    problem = Problem()

    # Für jedes kleine Rechteck: berechne alle möglichen Positionen
    for i, (width, height) in enumerate(kleine_rechtecke): # i = Index des Rechtecks, width/height = Größe des Rechtecks, enumerate macht aus der Liste der kleinen Rechtecke eine Liste von (Index, (width, height)) Tupeln
        positions = get_positions(groesse_grosses_rechteck, width, height)
        print(f"Rechteck {i} ({width}x{height}): {len(positions)} mögliche Positionen")
        problem.addVariable(i, positions)

    # Constraint: kein Rechteckpaar darf sich überschneiden
    n = len(kleine_rechtecke)
    for i in range(n):
        for j in range(i + 1, n):          # j > i → jedes Paar nur einmal
            problem.addConstraint(
                lambda p1, p2: not overlaps(p1, p2),
                (i, j)
            )

    return problem.getSolution()   # erste gefundene Lösung (oder None)


def print_solution(solution, groesse_grosses_rechteck, kleine_rechtecke):
    """Gibt die Lösung als ASCII-Gitter aus."""
    if solution is None:
        print("Keine Lösung gefunden!")
        return

    W, H = groesse_grosses_rechteck
    # Gitter mit Leerzeichen füllen
    grid = [["." for _ in range(W)] for _ in range(H)]

    labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, pos in solution.items(): # i = Index des Rechtecks, pos = Platzierung (x, y, a, w, h)
        x, y, a, w, h = pos 
        dx = w if a == "h" else h # dx = Breite entlang x-Achse, abhängig von der Ausrichtung 
        dy = h if a == "h" else w # dy = Höhe entlang y-Achse, abhängig von der Ausrichtung
        for row in range(y, y + dy): 
            for col in range(x, x + dx): 
                grid[row][col] = labels[i] # Beschrifte die Zellen des Gitters mit dem entsprechenden Buchstaben für das Rechteck

    print(f"\nLösung ({W}x{H} Gitter):")
    print("  " + " ".join(str(c) for c in range(W)))
    for row_idx, row in enumerate(grid):
        print(f"{row_idx} " + " ".join(row))

    print("\nLegende:")
    for i, (w, h) in enumerate(kleine_rechtecke):
        pos = solution[i]
        x, y, a, _, _ = pos
        print(f"  {labels[i]}: {w}x{h} @ ({x},{y}) {'horizontal' if a == 'h' else 'vertikal'}")


# ── Hauptprogramm ────────────────────────────────────────────────────────────
groesse_grosses_rechteck = (7, 8)
kleine_rechtecke = [(6, 4), (8, 1), (4, 1), (5, 2), (2, 2), (3, 2)]

print("Starte Packungsproblem...")
print(f"Großes Rechteck: {groesse_grosses_rechteck[0]}x{groesse_grosses_rechteck[1]}")
print(f"Kleine Rechtecke: {kleine_rechtecke}\n")

solution = packungsproblem(groesse_grosses_rechteck, kleine_rechtecke)
print_solution(solution, groesse_grosses_rechteck, kleine_rechtecke)