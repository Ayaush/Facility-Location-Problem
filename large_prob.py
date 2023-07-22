""" This version takes csv data as input and then uses it to solve FLP problem.
It uses different formulation than small problem cases. Try to run it for 10wh-100 regions,
10wh-500 regions (infeasible problem), 50wh-500 rgions and 150wh-2000strs (may take large time to solve)  """

import pulp
import pandas as pd
import sys
import time


def get_data(df):
    st = time.time()
    print("start data definition module")


    global str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc
    str_ct = df['Region ID'].nunique()
    wh_ct = df['WH ID'].nunique()

    print("total candidate warehouses :",wh_ct)
    print("total stores : ",str_ct)

    str_dmd ={}
    tmpdf =df [['Region ID','Demand']].drop_duplicates()
    for index, row in tmpdf.iterrows():
        str_dmd[row['Region ID']] = row['Demand']

    wh_cap = {}
    tmpdf = df[['WH ID', 'WH Cap']].drop_duplicates()
    for index, row in tmpdf.iterrows():
        wh_cap[row['WH ID']] = row['WH Cap']

    wh_fc = {}
    tmpdf = df[['WH ID', 'WH Setup Cost']].drop_duplicates()
    for index, row in tmpdf.iterrows():
        wh_fc[row['WH ID']] = row['WH Setup Cost']

    tspc ={}
    for index,row in df.iterrows():
        tspc[(row['WH ID'],row['Region ID'])]= row['Cost']

    """ check if problem is feasible or not. if total demand is more than total wh cap, then problem is infeasible"""
    if (sum(wh_cap.values())< sum(str_dmd.values())):
        print(" Total demand is more than total Warehouses capacities")
        print("Total WH cap: ",sum(wh_cap.values()))
        print("Total Demand: ",sum(str_dmd.values()))
        sys.exit()

    print("data definition complete, time taken: ", time.time() - st)


def create_model():

    print("Start model definition")
    st =time.time()
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
    for i in wh_cap:
        x[i] = pulp.LpVariable('X_'+i,0,1,pulp.LpInteger)

    y={}
    for i in wh_cap:
        for j in str_dmd:
            if (i,j) in tspc.keys():
                y[(i,j)] = pulp.LpVariable('Y_'+i+'_'+j,0,1,pulp.LpInteger)




    """ Define constraints"""
    """ demand constraints"""
    for i in str_dmd:
        tmplst = []
        for j in wh_cap:
            if (j,i) in tspc.keys():
                tmplst.append(y[(j,i)])
        model+= pulp.lpSum(tmplst) >= 1
    """ cap contraints.  It links the x with y variable in the same constraint. """
    for i in wh_cap:
        tmplst =[]
        for j in str_dmd:
            if (i,j) in tspc.keys():
                tmplst.append(str_dmd[j]* y[(i,j)])
        model+=pulp.lpSum(tmplst)<= x[i]*wh_cap[i]

    """
        Define Objective function
    """
    opn_cst_list =[]
    for i in wh_cap:
        opn_cst_list.append(x[i]* wh_fc[i])

    tspc_cst_list = []
    for i in wh_cap:
        for j in str_dmd:
            if (i,j) in tspc.keys():
                tspc_cst_list.append(tspc[(i,j)]*str_dmd[j]*y[(i,j)] )
    model += pulp.lpSum(opn_cst_list) + pulp.lpSum(tspc_cst_list)
    model.writeLP("a.lp")
    print("model definition complete, time taken: ",time.time()-st)

    """ set solver"""
    solver = pulp.getSolver('PULP_CBC_CMD', timeLimit=300,gapRel=0.01,msg=True)

    """ solve LP model"""
    model.solve(solver)

    model_status = str(pulp.LpStatus[model.status])
    print("Model Status = ", model_status)
    print("Objective Value", pulp.value(model.objective))
    if model_status !="Optimal":
        return "Not abl to solve"
    open_WH=[]
    closed_WH = []
    WH_Rgn_map ={}
    for i in wh_cap:
        if x[i].varValue == 1:
            open_WH.append(i)
        else:
            closed_WH.append(i)
    for i in wh_cap:
        if x[i].varValue==1:
            WH_Rgn_map.setdefault(i,[])
            for j in str_dmd:
                if (i,j) in tspc.keys():
                    if y[(i,j)].varValue ==1:
                        WH_Rgn_map[i].append(j)
    print("No of WH selected: ",len(open_WH))
    print("Selected WH list:",open_WH)
    print("WH to Region Map: ",WH_Rgn_map)


if __name__ == '__main__':
    str_ct, wh_ct, str_dmd, wh_cap, wh_fc, tspc = 0,0,0,0,0,0
    df = pd.read_csv("data/WH10_Region100_data.csv")

    df = df.astype({'WH ID': str, 'Region ID': str, 'Cost': int, 'Demand': int, 'WH Cap': int, 'WH Setup Cost': int})
    get_data(df)
    create_model()



