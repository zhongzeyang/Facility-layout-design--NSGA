import autograd.numpy as anp
from pymoo.core.problem import Problem
import numpy as np


class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=10, n_obj=2, n_constr=1, xl=anp.array([0,0,0,0,0,6,7,9,14,19]), xu=anp.array([1,1,1,1,1,8,9,12,18,22]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = -x[:,0]*x[:,5]-x[:,1]*x[:,6]-x[:,2]*x[:,7]-x[:,3]*x[:,8]-x[:,4]*x[:,9]
        f2 = (np.ceil(x[:,5]/3)*(3*3.333+3*4+4*5.992+4*6.466+4*3.233+5*15.733+8*30.256)*3+x[:,5]*6*15.662)*0.3*x[:,0]+(np.ceil(x[:,6]/3)*(3*3.111+3*3.333+4*5.867*2+4*3.233+5*15.244+8*30.256)*3+x[:,6]*6*15.311)*0.3*x[:,1]+(np.ceil(x[:,7]/3)*(3*3.111+3*3.333+4*5.945*2+4*3.233+5*15.244+8*30.256)*3+x[:,7]*6*15.444)*0.3*x[:,2]+(np.ceil(x[:,8]/3)*(3*3.111+3*3.333+4*5.945*2)*3+x[:,8]*(6*15.444+4*3+5*15+8*30))*0.3*x[:,3]+(np.ceil(x[:,9]/3)*(3*3.111+3*3.333)*6+(6*15.04+4*5.48+4*5.78+4*3.233+5*15.22+8*30.23)*x[:,9])*0.3*x[:,4]+2*x[:,1]+2*x[:,2]+341*x[:,3]+355*x[:,4]

        g1 = -1+ (x[:,0]+x[:,1]+x[:,2]+x[:,3]+x[:,4])
        
        out["F"] = anp.column_stack([f1,f2])
        out["G"] = anp.column_stack([g1])


from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_crossover, get_mutation, get_sampling
from pymoo.optimize import minimize

mask = ["int", "int", "int", "int", "int", "real", "real", "real", "real", "real"]

from pymoo.operators.mixed_variable_operator import MixedVariableSampling, MixedVariableMutation, MixedVariableCrossover

sampling = MixedVariableSampling(mask, {
    "real": get_sampling("real_random"),
    "int": get_sampling("int_random")
})

crossover = MixedVariableCrossover(mask, {
    "real": get_crossover("real_sbx", prob=0.9, eta=15),
    "int": get_crossover("int_sbx", prob=0.9, eta=15)
})

mutation = MixedVariableMutation(mask, {
    "real": get_mutation("real_pm", eta=20),
    "int": get_mutation("int_pm", eta=1)
})

algorithm = NSGA2(pop_size=40,n_offsprings=10,sampling=sampling, crossover=crossover,mutation=mutation,eliminate_duplicates=True,)

res = minimize(MyProblem(),
               algorithm,
               termination=('n_gen', 50),
               seed=1,
               save_history=True,
               verbose=True,
               eliminate_duplicates=True
               )

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
print("Constraint violation: %s" % res.CV)

F=res.F
F_1=[]
F_2=[]
for i in range(40):
    if -18<F[i][0]<-13:
        f = F[i]
        F_1.append(f.tolist())
    elif F[i][0]<-18:
        f = F[i]
        F_2.append(f.tolist())

from pymoo.visualization.scatter import Scatter

plot = Scatter()
plot.add(MyProblem().pareto_front(), marker="x", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolors='gold')
plot.add(np.array(F_1), facecolor="none", edgecolors='darkorange')
plot.add(np.array(F_2), facecolor="none", edgecolors='red')
plot.show()

