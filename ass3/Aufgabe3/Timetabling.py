from constraint import Problem, AllDifferentConstraint

def solve():
    problem = Problem()

    domain = [1,2,3,4]

    problem.addVariable("Maier", domain)
    problem.addVariable("Müller", domain)
    problem.addVariable("Schmid", domain)
    problem.addVariable("Huber", domain)

    problem.addVariable("Deutsch", domain)
    problem.addVariable("Englisch", domain)
    problem.addVariable("Mathe", domain)
    problem.addVariable("Physik", domain)

    problem.addConstraint(AllDifferentConstraint(), ["Maier", "Müller", "Schmid", "Huber"])

    problem.addConstraint(AllDifferentConstraint(), ["Deutsch", "Englisch", "Mathe", "Physik"])

    # 1
    problem.addConstraint(lambda maier: maier != 4, ["Maier"])

    # 2
    problem.addConstraint(lambda muller, deutsch: muller == deutsch, ["Müller", "Deutsch"])

    # 3
    problem.addConstraint(lambda schmid , mueller: abs(schmid - mueller) > 1, ["Schmid", "Müller"])

    # 4
    problem.addConstraint(lambda huber, mathe: huber == mathe, ["Huber", "Mathe"])

    # 5
    problem.addConstraint(lambda physik: physik == 4, ["Physik"])

    # 6
    problem.addConstraint(lambda deutsch, englisch: deutsch != 1 and englisch != 1, ["Deutsch", "Englisch"])


    solutions = problem.getSolutions()
    return solutions

def main():
    solutions = solve()
    for solution in solutions:
        print(solution)

if __name__ == "__main__":
    main()