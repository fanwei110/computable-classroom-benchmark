# Correct solution with eccentric formatting and dict(zip(...)) assembly
# (must be judged correct).
FACE  =  100.0 ;  CR = 0.046 ;   N=7 ;Y =0.053

cfs=[ (t, FACE*CR + (FACE if t==N else 0)) for t in range(1,N+1) ]
P  = sum( cf/(1+Y)**t for t,cf in cfs )
MAC= sum( t*cf/(1+Y)**t for t,cf in cfs )/P
MOD= MAC/(1+Y)
CX = sum( t*(t+1)*cf/(1+Y)**(t+2) for t,cf in cfs )/P

result = dict(zip(
    ["price","macaulay_duration_years","modified_duration_years","convexity"],
    [P, MAC, MOD, CX]))
