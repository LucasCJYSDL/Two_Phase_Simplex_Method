from gurobipy import *

## Create a new model
m = Model()

## Create variables
x = []
site_num = 4
series_num = 4
for i in range(site_num):
    x.append([])
    for j in range(series_num):
        x[i].append(m.addVar(name='x_{}_{}'.format(i+1,j+1)))

## Set objective function
C = [[16, 12, 20, 18], [14, 13, 24, 20], [17, 10, 28, 20], [12, 11, 18, 17]]
obj = 0
for i in range(site_num):
    for j in range(series_num):
        obj += C[i][j] * x[i][j]
m.setObjective(obj , GRB.MAXIMIZE)

## Add constraints
# non-negativity
for i in range(site_num):
    for j in range(series_num):
        m.addConstr(x[i][j] >= 0, name='n_{}'.format(i*series_num+j+1))
# constraints on the available areas
A = [1500, 1700, 900, 600]
for i in range(site_num):
    con_i = 0
    for j in range(series_num):
        con_i += x[i][j]
    m.addConstr(con_i <= A[i], name='a_{}'.format(i+1))
# constraints on the minimum yield
Y = [22.5, 9, 4.8, 3.5]
UY = [[17, 14, 10, 9], [15, 16, 12, 11], [13, 12, 14, 8], [10, 11, 8, 6]]
for j in range(series_num):
    con_j = 0
    for i in range(site_num):
        con_j += UY[i][j] * x[i][j]
    m.addConstr(con_j >= Y[j], name='y_{}'.format(j+1))

# Optimize model
m.optimize()

#Print optimal values of the decision variables, defined in the paper
print("The objective solutions are listed as: ")
for v in m.getVars():
    print(v.varName, v.x)

#Print optimal objective value
print('Maximum of the expected annual revenue:',  m.objVal)