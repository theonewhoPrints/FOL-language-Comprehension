import sys
import random


def reader(language):

    predicates = []
    variables = []
    constants = []
    functions = []
    clauses = []

    section = None

    with open(language, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("Predicates:"):
                section = "predicates"
                items = line.split()
                predicates.extend(items[1:])

            elif line.startswith("Variables:"):
                section = "variables"
                items = line.split()
                variables.extend(items[1:])

            elif line.startswith("Constants:"):
                section = "constants"
                items = line.split()
                constants.extend(items[1:])

            elif line.startswith("Functions:"):
                section = "functions"
                items = line.split()
                functions.extend(items[1:])

            elif line.startswith("Clauses:"):
                section = "clauses"
            elif line and section:
                # Split line by whitespace and store accordingly
                items = line.split()
                if section == "clauses":
                    clauses.append(tuple(items))
    return predicates, variables, constants, functions, clauses


def PL_Resolution(values):

    variables = values[1]
    constants = values[2]
    functions = values[3]
    pairclauses = set(values[4])
    newclause = set()
    while True:
        if not variables:

            resolvents = PL_resolve(list(pairclauses))
        if variables:
            resolvents = unify(variables, list(pairclauses), constants, functions)
        if () in resolvents:
            return "no"
        newclause.update(resolvents)
        if newclause.issubset(pairclauses):
            return "yes"
        pairclauses.update(newclause)


def unify(variables, pairclauses, constants, functions):
    resolver = set()


    for i, clause in enumerate(pairclauses):
        for term in clause:
            # Extract predicate
            try:
                predicate, args = term[:-1].split("(", 1)
            except ValueError:
                continue  # Skip if the term format is not as expected


            term_args = args.strip().split(',')


            for j in range(i + 1, len(pairclauses)):
                next_clause = pairclauses[j]

                for term_2 in next_clause:
                    try:
                        predicate_2, args_2 = term_2[:-1].split("(", 1)
                    except ValueError:
                        continue  # Skip if the term format is not as expected


                    term_2_args = args_2.strip().split(',')


                    if predicate == ("!" + predicate_2) or ("!" + predicate) == predicate_2:
                        # Check for matching arg counts
                        if len(term_args) == len(term_2_args) and term_args != term_2_args:
                            k = 0
                            while k < len(term_args) and k < len(term_2_args):
                                cont = None
                                repl1 = None
                                func1 = None
                                func2 = None
                                curr = term_args[k]
                                curr2 = term_2_args[k]
                                if curr in variables and curr2 in variables:
                                    cont = True
                                elif curr in constants and curr2 in variables:
                                    cont = True
                                    repl1 = True
                                elif curr in variables and curr2 in constants:
                                    cont = True
                                    repl1 = False
                                elif curr.split('(')[0] in functions and curr2.split('(')[0] in functions:
                                    cont = True
                                    func1 = True
                                    func2 = True
                                elif curr2.split('(')[0] in functions:
                                    cont = True
                                    func1 = False
                                    func2 = True
                                elif curr.split('(')[0] in functions:
                                    cont = True
                                    func1 = True
                                    func2 = False
                                k += 1

                            if cont == True:
                                x1 = clause.index(term)
                                y1 = next_clause.index(term_2)
                                x2 = x1 + 1
                                y2 = y1 + 1
                                new_var_arg = "CSCI" + str(random.randint(200, 888))

                                # Remove terms from og clauses
                                lang1 = clause[:x1] + clause[x2:]
                                lang2 = next_clause[:y1] + next_clause[y2:]
                                if func1 and not func2:
                                    if curr2 not in curr:
                                        new_var_arg = curr
                                    else:
                                        return resolver
                                if not func1 and func2:
                                    if curr not in curr2:
                                        new_var_arg = curr2
                                    else:
                                        return resolver
                                if cont == True and repl1 == True:
                                    new_var_arg = args
                                if cont == True and repl1 == False:
                                    new_var_arg = args_2
                                # Substitute new variable in place of existing args
                                updated_ci = tuple(
                                    item.replace(args, new_var_arg) for item in lang1
                                )
                                updated_cj = tuple(
                                    item.replace(args_2, new_var_arg) for item in lang2
                                )
                                resolve = updated_ci + updated_cj
                                if new_var_arg not in constants and '(' not in new_var_arg:
                                    variables.append(new_var_arg)
                                resolver.add(resolve)
                        elif term_args == term_2_args:
                            pair = [clause, next_clause]
                            resolve = tuple(PL_resolve(pair))
                            for r in resolve:
                                resolver.add(r)

    return resolver


def PL_resolve(pairclauses):
    resolver = set()
    for clause in pairclauses:
        for term in clause:
            nextx = 0
            while nextx < len(pairclauses):
                next = pairclauses[nextx]
                if clause == next:
                    nextx += 1
                    continue
                for term_2 in next:
                    if term == ("!" + term_2) or ("!" + term) == term_2:
                        x1 = clause.index(term)
                        y1 = next.index(term_2)
                        x2 = clause.index(term) + 1
                        y2 = next.index(term_2) + 1
                        lang1 = clause[0:x1] + clause[x2:]
                        lang2 = next[0:y1] + next[y2:]
                        resolve = tuple(lang1 + lang2)
                        resolver.add(resolve)
                nextx += 1  # Move to the next clause
    return resolver


def main():

    language = sys.argv[1]
    values = reader(language)
    print(PL_Resolution(values))

main()