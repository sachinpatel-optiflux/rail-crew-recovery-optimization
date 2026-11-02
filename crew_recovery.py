import pulp

crews  = ["C1", "C2", "C3"]
trains = ["T1", "T2", "T3"]
ok = {("C1","T1"):1, ("C1","T2"):0, ("C1","T3"):1,
      ("C2","T1"):1, ("C2","T2"):1, ("C2","T3"):0,
      ("C3","T1"):0, ("C3","T2"):1, ("C3","T3"):1}
pen = {"T1": 10000, "T2": 8000, "T3": 2000}
available = {"C1": 1, "C2": 0, "C3": 1}      # C2 is out

m = pulp.LpProblem("crew_recovery", pulp.LpMinimize)
x = pulp.LpVariable.dicts("x", (crews, trains), cat="Binary")
D = pulp.LpVariable.dicts("D", trains, cat="Binary")

m += pulp.lpSum(pen[j] * D[j] for j in trains)           # objective
for j in trains:                                          # covered or delayed
    m += pulp.lpSum(x[i][j] for i in crews) + D[j] == 1
for i in crews:                                           # at most one train
    m += pulp.lpSum(x[i][j] for j in trains) <= 1
for i in crews:                                           # banned pairs
    for j in trains:
        if ok[(i, j)] == 0 or available[i] == 0:
            m += x[i][j] == 0

m.solve(pulp.PULP_CBC_CMD(msg=0))
print(pulp.LpStatus[m.status], pulp.value(m.objective))
for i in crews:
    for j in trains:
        if x[i][j].value() > 0.5:
            print(f"{i} -> {j}")
print("Delayed:", [j for j in trains if D[j].value() > 0.5])
