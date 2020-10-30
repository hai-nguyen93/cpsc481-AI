from unify import *
from copy import deepcopy


class Rule:
    def __init__(self, if_expr=None, then_expr=None):
        self.if_clause = []
        if if_expr:
            self.add_to_if(if_expr)

        self.then_clause = []
        if then_expr:
            self.add_to_then(then_expr)

    def add_to_if(self, expression):
        self.if_clause.append(expression)

    def add_to_then(self, expression):
        self.then_clause.append(expression)

    def __str__(self):
        return str(self.if_clause) + ' -> ' + str(self.then_clause)


# A Rule has an if clause, and a then clause.
# if clause and then clause are a list of expresions.
# each expression has a format: f(a, b) -> ['f', 'a', 'b']
# in if clause, the expressions are connected to each other with logical and.
# logical or can be re-written as separate rules.
# Rules
r1 = Rule(['spaniel', 'X'], ['gooddog', 'X'])

r2 = Rule()
r2.add_to_if(['collie', 'X'])
r2.add_to_if(['trained', 'X'])
r2.add_to_then(['gooddog', 'X'])

r3 = Rule(then_expr=['location', 'X', 'Z'])
r3.add_to_if(['gooddog', 'X'])
r3.add_to_if(['master', 'X', 'Y'])
r3.add_to_if(['location', 'Y', 'Z'])

r4 = Rule(then_expr=['location', 'sam', 'park'])
r4.add_to_if(['day', 'saturday'])
r4.add_to_if(['warm', 'saturday'])

r5 = Rule(then_expr=['location', 'sam', 'museum'])
r5.add_to_if(['day', 'saturday'])
r5.add_to_if(['warm', 'saturday', 'not'])

rules = [r1, r2, r3, r4, r5]


def valid_goal(goal):
    for s in goal:
        if is_variable(s):
            return False
    return True


def solve():
    # location(fred, P) -> ['location', 'fred', 'P']
    goal = ['location', 'fred', 'P']
    subs = []  # substitution sets, obtained from unify
    expr_list = [goal]  # contain the expressions that need verifying
    need_verifying = []  # contain the rule correspond to the expr in expr_list need_verifying[i] <-> expr_list[i+1]
    used_rule = []  # contain the used rules
    subs_history = []  # contain previous substitution set; this is used to roll back if one path fails
    print("\nWhere is Fred?\n")

    while expr_list:
        current_expr = expr_list[-1]  # pick the last element of expr_list to process
        if len(subs) > 0:
            apply(subs, current_expr)

        # find a rule (use unify to find, found a rule if unify doesn't fail)
        rule_index = -1
        for i in range(len(rules)):
            if i not in used_rule:
                s = unify(rules[i].then_clause[0], current_expr)
                if s != -1:
                    subs_history.append(deepcopy(subs))
                    subs = composition(subs, s)
                    rule_index = i
                    break

        # if found a rule to use, add all expr in if_clause to expr_list to verify
        if rule_index > -1:
            for e in rules[rule_index].if_clause:
                expr_list.append(e)
                need_verifying.append(rule_index)
            used_rule.append(rule_index)

        # if it's not a rule then it's a fact that needs verifying
        else:
            found = False
            # find a fact in known facts to unify with expr; if success, the expr is true
            for f in facts:
                s1 = unify(f, current_expr)
                if s1 != -1:
                    found = True
                    if len(s1) > 0:
                        subs_history.append(deepcopy(subs))
                        subs = composition(subs, s1)
                        apply(subs, current_expr)
                        facts.append(current_expr)

                    # all rules are verified, return answer
                    if len(need_verifying) == 0:
                        apply(subs, goal)
                        print(goal)
                        print(goal[1] + ' is at ' + goal[2])
                        return

                    # if expr is true, remove from expr_list
                    current_rule = need_verifying.pop()
                    expr_list.pop()

                    # if all expr in if_clause of a rule is true, then_clause is true and add then clause to facts
                    if len(need_verifying) == 0 or current_rule != need_verifying[-1]:
                        e = rules[current_rule].then_clause[0]
                        apply(subs, e)
                        facts.append(e)
                    break

            # if can't find a fact, expr is false and the rule it is associated with is false;
            # remove expr from expr_list, roll back substitution set subs,
            # remove all expr associated with the incorrect rule
            if not found:
                # if there is no rule to verify and the expr is false, cannot find the answer
                if len(need_verifying) == 0:
                    print("Cannot find the answer!\n")
                    return
                subs = subs_history.pop()
                incorrect_rule = need_verifying.pop()
                expr_list.pop()
                while len(need_verifying) > 0 and incorrect_rule == need_verifying[-1]:
                    need_verifying.pop()
                    expr_list.pop()

    apply(subs, goal)
    print(goal)
    print(goal[1] + ' is at ' + goal[2])
    return


# A fact is an single expression, stored as a list of string.
# For example: Fred's master is Sam -> master(fred, sam) -> ['master', 'fred', 'sam']
# Facts
facts = [['master', 'fred', 'sam']]

# get user input
day = input("What day of the week is it?: ").lower()
facts.append(['day', day])
if day == 'saturday':
    w = input("Is it cold today? (y/n): ")
    if w[0] in ['y', 'Y']:
        facts.append(['warm', 'saturday', 'not'])
    else:
        facts.append(['warm', 'saturday'])

dog = input("What kind of dog is fred?: ").lower()
facts.append([dog, 'fred'])
if dog == 'collie':
    t = input("Is it trained? (y/n): ")
    if t[0] in ['y', 'Y']:
        facts.append(['trained', 'fred'])
    else:
        facts.append(['trained', 'fred', 'not'])
print(facts)
solve()
