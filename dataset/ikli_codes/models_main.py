"""-------------------------------------------------------------------------***

This python code contains the implementation of three

MIP models for sequencing aircraft landing

***----------------------------------------------------------------------*** """



#--------------------            import modules        ------------------------#
from docplex.mp.model import Model   
import datetime
import operator
import pandas as pd
import time
#------------------------------------------------------------------------------#


# ------------------        Some utility functions        ---------------------#

separation_dict = {('Heavy' , 'Heavy') : 96,
                   ('Heavy' , 'Medium'): 157,
                   ('Heavy' , 'Light') : 196,
                   ('Medium', 'Heavy') : 60,
                   ('Medium', 'Medium'): 69,
                   ('Medium', 'Light') : 131,
                   ('Light' , 'Heavy') : 60,
                   ('Light' , 'Medium'): 69,
                   ('Light' , 'Light') : 82 }

def s_to_time_stamp(s):
    return str(datetime.timedelta(seconds=int(s)))


def parameters(instance):
    
    """ Returns parameters of the MIP model: E, T, L, and costs """
    
    T       = {i: instance.sta_s[i]  for i in instance.index}
    E       = {i: T[i] - 60          for i in instance.index}
    L       = {i: T[i] + 1800        for i in instance.index}
    c_moins = {i: instance.cost_5[i] for i in instance.index}
    c_plus  = {i: instance.cost_5[i] for i in instance.index}
    
    S = {}
    for i in instance.index:
        for j in instance.index:
            S[i,j] = separation_dict[instance.category[i], 
              instance.category[j] ]
            
    M = {(i, j): (L[i] + S[i,j] - E[j]) for i in instance.index  for j in instance.index}
    
    return E, T, L, c_moins, c_plus, S, M



def fcfs(instance, T, S):
    
    """ Returns the FCFS solution sequence and its cost """
    x        = {}
    sorted_T = sorted(T.items(), key=operator.itemgetter(1))
    i0       = sorted_T[0][0]
    x[i0]    = T[i0]
    cost     = instance.cost_5[i0]*(x[i0] - T[i0])
    for i in range(1, len(sorted_T)):
        idx  = sorted_T[i][0]
        x[idx]       = max(T[idx], x[sorted_T[i-1][0]] + S[sorted_T[i-1][0],idx])
        cost         = cost +  instance.cost_5[idx] * (x[idx] - T[idx])
    return x, cost

#------------------------------------------------------------------------------#
    

    
#---------------           Beasley multiple runway        ---------------------#
    
def beasley_mlp_rwy(m, E, T, L, g, h, S):
    
    """ Returns the MIP model of Beasley et al.  """
                
    mdl = Model(name = "Beasley_ALP")  # Create problem instance   
    P   =[i for i in T.keys() ]        # list of aircraft indexes
    R   = [k for k in range(1,m+1)]                              
    PP  = [(i,j) for i in P for j in P if i!=j]
    PK  = [(i,r) for i in P for r in R]
    M   = 99999
    
    delta = mdl.binary_var_dict(PP, name = "delta")
    y     = mdl.binary_var_dict(PK, name = "y")  
    z     = mdl.binary_var_dict(PP, name = "z")
    x     = mdl.continuous_var_dict(P, name = "x") 
    alpha = mdl.continuous_var_dict(P, name = "alpha")
    beta  = mdl.continuous_var_dict(P, name = "beta")  
    
    # Objective function
    mdl.minimize(mdl.sum( ( g[i]*alpha[i]  + h[i]*beta[i])                          for i in P))
       
    # Constraints         
    mdl.add_constraints( x[i]                     >=  E[i]                          for i in P )
    mdl.add_constraints( x[i]                     <=  L[i]                          for i in P )
    mdl.add_constraints( delta[i,j] + delta[j,i]  ==   1                            for (i,j) in PP if i<j)
    mdl.add_constraints( x[i]                     == T[i] - alpha[i] + beta[i]      for i in P )
    
    mdl.add_constraints( alpha[i]                 >=  T[i] - x[i]                   for i in P )
    mdl.add_constraints( alpha[i]                 <=  T[i] - E[i]                   for i in P )
    mdl.add_constraints( alpha[i]                 >=  0                             for i in P )
    
    mdl.add_constraints( beta[i]                  >=  x[i] - T[i]                   for i in P )
    mdl.add_constraints( beta[i]                  <=  L[i] - T[i]                   for i in P )
    mdl.add_constraints( beta[i]                  >=  0                             for i in P )
    
    mdl.add_constraints( x[j]      >=     x[i] + S[i,j]*z[i,j] - M*delta[j,i]       for (i,j) in PP)
       
    mdl.add_constraints(mdl.sum(y[i,r] for r in R)    ==    1       for i in P)
    mdl.add_constraints( z[i,j]       == z[j,i]                     for i in P for j in P if i<j)
    mdl.add_constraints( z[i,j]       >= y[i,r] + y[j,r] - 1        for r in R for i in P for j in P if i<j)
    

    return mdl, x, delta, alpha, beta


#---------------          Salehipour multiple runway                 ----------#
def salehipour_mlp_rwy(m, E, T, L, c_moins, c_plus, S):
    
    """ Returns the MIP model of Salehipouret al.  """
            
    mdl = Model(name = "Salehipour_ALP") 
    A   = [i for i in T.keys() ]                     
    R   = [k for k in range(1,m+1)]                           
    AA  = [(i,j) for i in A for j in A if i!=j]
    AR  = [(i,k) for i in A for k in R]
    M   = 99999
    
    y       = mdl.binary_var_dict(AA, name = "y")
    gamma   = mdl.binary_var_dict(AR, name = "gamma")  
    delta   = mdl.binary_var_dict(AA, name = "delta")
    x       = mdl.continuous_var_dict(A, name = "x") 
    a       = mdl.continuous_var_dict(A, name = "a")
    b       = mdl.continuous_var_dict(A, name = "b")
      

    mdl.minimize(mdl.sum( ( c_moins[i]*b[i]  + c_plus[i]*a[i])         for i in A))   
    mdl.add_constraints( x[i]                     >=  E[i]             for i in A )
    mdl.add_constraints( x[i]                     <=  L[i]             for i in A )
    mdl.add_constraints( x[i]  - T[i]             ==  a[i] - b[i]      for i in A )
    mdl.add_constraints( x[j] - x[i]              >=    S[i,j]*delta[i,j]  - M*y[j,i]    for (i,j) in AA)
       
    mdl.add_constraints( y[i,j] + y[j,i]  ==   1                         for (i,j) in AA)
    mdl.add_constraints( delta[i,j]       >= gamma[i,r] + gamma[j,r] - 1 for r in R for (i,j) in AA)
    mdl.add_constraints(mdl.sum(gamma[i,r] for r in R)    ==    1        for i in A)
    
    mdl.add_constraints( x[i]     >=  0             for i in A )
    mdl.add_constraints( a[i]     >=  0             for i in A )
    mdl.add_constraints( b[i]     >=  0             for i in A )

    return mdl, x, delta, a, b


#--------------------------             Furini             --------------------#

def furini(T, w, tS, d):
    
    """ Returns the MIP model of Furini et al.  """
           
    mdl   = Model(name = "Furinir_ALP")  
    I     = [i for i in T.keys() ]     
    K     = [k for k in range(1,len(T)+1)]      # list of aircraft indexes
    bar_K = [k for k in K if k!=1]
    IK    = [(i,k) for i in I for k in K]

    x   = mdl.binary_var_dict(IK   , name = "x")
    y   = mdl.continuous_var_dict(K, name = "y")  
    z   = mdl.continuous_var_dict(I, name = "z")
    
    mdl.minimize(mdl.sum( w[i]*(z[i] - T[i])      for i in I)) 
    
    mdl.add_constraints(mdl.sum(x[i,k] for k in K) ==    1          for i in I)
    mdl.add_constraints(mdl.sum(x[i,k] for i in I) ==    1          for k in K)
    mdl.add_constraints( z[i]    <=           T[i]   + d[i]         for i in I) 
    
    mdl.add_indicator_constraints(mdl.indicator_constraint(x[i,k] , z[i]>= y[k]) for k in K for i in I )
    
    mdl.add_constraints( y[k] >= 0                                               for k in K)
    mdl.add_constraints( y[k] >= mdl.sum(T[i]*x[i,k] for i in I)                 for k in K)
    mdl.add_constraints( y[k] >= y[k-1]  + tS[i1,i2]*(x[i1,k-1] + x[i2,k] - 1)   for k in bar_K for i1 in I for i2 in I)
    mdl.add_constraints( y[k] >= y[k-1]                                          for k in bar_K)
    return mdl, x


#-----------------------------   solve functions       ------------------------#

def solve_beasley_ml_rwy(m, E, T, L, g, h, S, timelimit):

    """ Returns the solution of the MIP model of Beasley et al.  """
    
    mdl, x, delta, x_moins, x_plus = beasley_mlp_rwy(m, E, T, L, g, h, S)
    mdl.set_time_limit(timelimit)
    
    start = time.time()
    s     = mdl.solve()
    end   = time.time()
    cpu   = end-start
    return  mdl, s, x, cpu

def solve_salehipour_ml_rwy(m, E, T, L, c_moins, c_plus, S, timelimit):
    
    """ Returns the solution of the MIP model of Salehipour et al.  """
    
    mdl, x, delta, x_moins, x_plus= salehipour_mlp_rwy(m, E, T, L, c_moins, c_plus, S)
    mdl.parameters.timelimit = timelimit
    
    start = time.time()
    s     = mdl.solve()
    end   = time.time()
    cpu   = end-start
    
    return  mdl, s, x, cpu


def solve_furini(T, w, tS, d, timelimit):
    
    """ Returns the solution of the MIP model of Furini et al.  """
    
    mdl, x                   = furini(T, w, tS, d)
    mdl.parameters.timelimit = timelimit
    
    start = time.time()
    s     = mdl.solve()
    end   = time.time()
    cpu   = end-start

    return  mdl, s, x, cpu

#****************************         Main            ***********************************


if __name__ == '__main__':
    
    """ This main function solves the three ikli_instances
    form the dataset "instance_7_11.csv". For the remaining instances from 
    "ikli_instances", from the OR-Library, the OR group Bologna, replace
    "name" by the name of the instance you want to solve """
    
    """ CPU results for each MIP model are contained in the objects named
    cpu_beasley, cpu_salehipour, and cpu_scpu_furini """

    m          = 3
    timelimit  = 300
    cpu_beasley, cpu_salehipour, cpu_furini = {}, {}, {}
    
    for N in range(30,60, 10):
        name     = "alp_7_"+str(N)+".csv"
        instance = pd.read_csv(name)
        instance = instance[:N]
        E, T, L, c_moins, c_plus, S, M = parameters(instance)

        for k in range(1, m+1):
            print("solving  ",N, "  for ", k, " runway")
            print("\n" )
            mdl_b, s_b, x_b, cpu_b  =  solve_beasley_ml_rwy(k, E, T, L, c_moins, c_plus, S, timelimit)
            mdl_s, s_s, x_s, cpu_s  =  solve_salehipour_ml_rwy(k, E, T, L, c_moins, c_plus, S, timelimit)
            
            cpu_beasley[N,k]    = cpu_b
            cpu_salehipour[N,k] = cpu_s
            if k == 1:
                mdl_f, s_f, x_f, cpu_f = solve_furini(T, c_plus, S, L, timelimit)
                cpu_furini[N,k] = cpu_f
                

