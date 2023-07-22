""" This problem contain 3 warehouses and 5 stores. We have used dictionary data structure and for loop  to write the LP Model."""

import pulp


def get_data():
    global str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc
    str_ct = 5
    wh_ct = 3
    str_dmd = [80,270,250,160,180]
    wh_cap = [1000,10000,1000]
    wh_fc = [1200,800,900]
    tspc= [[4,5,6,8,10],
                [6,4,3,5,8],
                [9,7,4,3,4]]

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
    x = {}
    for i in range(wh_ct):
        x[i] = pulp.LpVariable("wh"+str(i),0,1,pulp.LpInteger)

    y={}
    for i in range(wh_ct):
        for j in range(str_ct):
            y[(i,j)] = pulp.LpVariable("y"+str(i)+str(j),0,1,pulp.LpInteger)



    """ Define constraints"""
    """ demand constraints"""
    for i in range(str_ct):
        lst =[]
        for j in range(wh_ct):
            lst +=y[(j,i)]
        model+= pulp.lpSum(lst) >= 1
    """ capacity constraints"""
    for i in range(wh_ct):
        lst ={}
        for j in range(str_ct):
            lst += str_dmd[j]*y[(i,j)]
        model+=pulp.lpSum(lst)<=wh_cap[i]

    """ internal constraints for x"""
    for i in range(wh_ct):
        for j in range(str_ct):
            model+=y[(i,j)]<=x[i]

    """ 
        Define Objective function
    """
    opn_cst_list = [x[i]*wh_fc[i] for i in range(wh_ct)]
    tsp_cst_list = [tspc[i][j]*str_dmd[j]*y[(i,j)] for i in range(wh_ct) for j in range(str_ct)]
    model += pulp.lpSum(opn_cst_list) + pulp.lpSum(tsp_cst_list)
    model.writeLP("prob2.lp")


    """ set solver"""
    solver = pulp.getSolver('PULP_CBC_CMD', timeLimit=300,msg=True)

    """ solve LP model"""
    model.solve(solver)

    model_status = str(pulp.LpStatus[model.status])
    print("Model Status = ", model_status)
    print("Objective Value", pulp.value(model.objective))
    for i in range(wh_ct):
        print("wh"+str(i+1)+" status : ",x[i].varValue)


if __name__ == '__main__':
    str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc=0,0,0,0,0,0
    get_data()
    create_model()


