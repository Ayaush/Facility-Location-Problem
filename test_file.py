import pulp
import numpy as np
import pandas as pd



""" test pulp"""
try:
    model = pulp.LpProblem(" test model", pulp.LpMinimize)
    x = pulp.LpVariable("x",5,10,pulp.LpInteger)
    model += x
    solver = pulp.getSolver('PULP_CBC_CMD', timeLimit=300, gapRel=0.001, msg=False)
    model.solve(solver)
    print(" Pulp Library is working ")

except:
    print("Issue with pulp Library installation")


""" test pandas"""
try:
    lst1 ={"No":[1,2,3],"Score":[10,20,30]}
    df =pd.DataFrame.from_dict(lst1)
    print(" Pandas Library is working ")
except:
    print("issue with numpy library installation")


"""test numpy"""
try:
    arr = np.array([1, 2, 3, 4, 5])
    print(" numpy Library is working ")
except:
    print("issue with numpy library installation")