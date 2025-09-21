#! /usr/bin/env python3

import csv
from collections import defaultdict

import pulp


PREFERENCE_FILE = 'demo-data.csv'


def get_priority(priority):
    if priority == '':
        return 0
    priority = int(priority)
    if priority == -1:
        return -1
    elif priority == 1:
        return 1
    elif priority == 2:
        return 3
    elif priority == 3:
        return 5
    elif priority == 4:
        return 10
    elif priority == 5:
        return 15
    else:
        raise ValueError


def get_ranking(priority):
    if priority == -1:
        return "Not allowed"
    elif priority == 0:
        return "DC"
    elif priority == 1:
        return "1st"
    elif priority == 3:
        return "2nd"
    elif priority == 5:
        return "3rd"
    elif priority == 10:
        return "4th"
    elif priority == 15:
        return "5th"
    else:
        raise ValueError


class Person:
    def __init__(self, name, priorities):
        self.name_ = name

        self.priorities = {k: get_priority(v) for (k, v) in priorities.items()}

        self.assignment = None

    @property
    def name(self):
        return f"{self.name_}"

    def __repr__(self):
        priorities = ", ".join(
            "{}: {}".format(k, get_ranking(v)) for (k, v) in self.priorities.items()
        )

        return f"Person({self.name_}, {priorities})"

    def priority_of(self, badge):
        return self.priorities[badge]


def main():
    with open(PREFERENCE_FILE) as f:
        d = csv.DictReader(f.readlines())

    badges = ["Camper", "Chef", "Craft", "DIY", "Global Issues"]
    limits = {"Camper": 8, "Chef": 6, "Craft": 8, "DIY": 5, "Global Issues": 8}

    def person_from_dict(p):
        name = p["Name"]
        del p["Name"]
        return Person(name, p)

    people = [person_from_dict(p) for p in d]

    prob = pulp.LpProblem("Badge_Assignment", pulp.LpMinimize)
    assignments = {
        p: {b: pulp.LpVariable(f"{p.name}_{b}", 0, 1, cat="Integer") for b in badges}
        for p in people
    }

    thing_to_minimize = 0
    for person in people:
        for badge in badges:
            thing_to_minimize += assignments[person][badge] * person.priority_of(badge)

    prob += thing_to_minimize

    for person in people:
        condition = pulp.lpSum(assignments[person]) == 1
        prob += (condition, f"One badge for {person.name_}")

    for person in people:
        for badge in badges:
            if person.priority_of(badge) == -1:
                prob += (
                    assignments[person][badge] == 0,
                    f"No {badge} badge for {person.name_}",
                )

    for badge in badges:
        things_to_sum = []
        for person in people:
            things_to_sum.append(assignments[person][badge])
        limit = limits[badge]
        condition = pulp.lpSum(things_to_sum) <= limit
        prob += (condition, f"Max {limit} people in {badge}")

    result = prob.solve()

    variables = {v.name: v.varValue for v in prob.variables()}

    for person in people:
        for badge in badges:
            if variables[assignments[person][badge].name] == 1:
                person.assignment = badge

    for c in prob.constraints:
        print(c)

    print("\n================\n")

    assignment_counts = defaultdict(int)
    preference_counts = {"1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0, "DC": 0}
    for person in people:
        assignment_counts[person.assignment] += 1
        preference_counts[get_ranking(person.priority_of(person.assignment))] += 1
    for k, v in assignment_counts.items():
        print(f"{k}: {v}")
    print("\n================\n")
    for k, v in preference_counts.items():
        print(f"{k}: {v}")

    print("\n================\n")

    for person in people:
        print(
            f"{person.name_}: {person.assignment} ({get_ranking(person.priority_of(person.assignment))})"
        )

    print("\n================\n")

    print(pulp.LpStatus[result])


if __name__ == "__main__":
    main()
