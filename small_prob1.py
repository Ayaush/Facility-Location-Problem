""" This problem contain 2 candidate warehouses and and 3 stores. This problem was discussed in the session. """

import pulp

def get_data():
    global str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc
    store_count = 3
    wh_count = 2
    str_dmd = [270,250,160]
    wh_cap = [1000,1000]
    wh_fc = [1200,800]
    tspc= [[4,5,6],
                [6,4,3]]

def create_model():
    """ define problem
    Create a variable using the LpProblem function.It has two parameters, the first being the arbitrary name of this
    problem (as a string),and the second parameter being either LpMinimize or LpMaximize.
    """
    model = pulp.LpProblem(" FLP", pulp.LpMinimize)

    """ Define decision variables
    The problem variables x1 and x2 are created using the LpVariable class. It has four parameters, the first is the 
    arbitrary name of what this variable represents, the second is the lower bound on this variable, the third is the 
    upper bound, and the fourth is essentially the type of data (discrete or continuous)
    """
    x1 = pulp.LpVariable("wh 1",0,1,pulp.LpInteger)
    x2 = pulp.LpVariable("wh 2",0,1,pulp.LpInteger)

    y11 = pulp.LpVariable("y11", 0, 1, pulp.LpInteger)
    y12 = pulp.LpVariable("y12", 0, 1, pulp.LpInteger)
    y13 = pulp.LpVariable("y13", 0, 1, pulp.LpInteger)
    y21 = pulp.LpVariable("y21", 0, 1, pulp.LpInteger)
    y22 = pulp.LpVariable("y22", 0, 1, pulp.LpInteger)
    y23 = pulp.LpVariable("y23", 0, 1, pulp.LpInteger)

    """ Define constraints"""
    """ demand constraints"""
    model += y11 + y21 == 1
    model += y12 + y22 == 1
    model += y13 + y23 == 1

    """ capacity constraints"""
    model += str_dmd[0]*y11 + str_dmd[1]*y12 + str_dmd[2]*y13 <= wh_cap[0]
    model += str_dmd[0]*y21 + str_dmd[1]*y22 + str_dmd[2]*y23 <= wh_cap[1]

    """ internal constraints for x"""
    model += y11 <= x1
    model += y12 <= x1
    model += y12 <= x1
    model += y21 <= x2
    model += y22 <= x2
    model += y23 <= x2


    """ 
    Define Objective function
    """
    fc = wh_fc[0]*x1 + wh_fc[1]*x2
    vc = tspc[0][0]*str_dmd[0]* y11 + tspc[0][1]*str_dmd[1]* y12 +tspc[0][2]*str_dmd[2]* y13 +\
         tspc[1][0] * str_dmd[0] * y21 + tspc[1][1] * str_dmd[1] * y22 + tspc[1][2] * str_dmd[2] * y23


    model += fc + vc
    model.writeLP("model.lp")

    """ set solver"""
    solver = pulp.getSolver('PULP_CBC_CMD', timeLimit=300,msg=True)

    """ solve LP model"""
    model.solve(solver)

    model_status = str(pulp.LpStatus[model.status])
    print("Model Status = ", model_status)
    print("Objective Value", pulp.value(model.objective))
    print(" Warehouse 1 status : ",x1.varValue)
    print(" Warehouse 1 status : ", x2.varValue)

if __name__ == '__main__':
    str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc = 0,0,0,0,0,0
    get_data()
    create_model()
