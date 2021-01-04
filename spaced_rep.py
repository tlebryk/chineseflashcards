import ebisu

t_init = 1
a_init = 3.0
b_init = 3.0

default_model = ebisu.defaultModel(t=t_init, alpha=a_init, beta=b_init)

(a_wrong, b_wrong, t_wrong) = ebisu.updateRecall(default_model, 0, 1, 0.1)
(a_right, b_right, t_right) = ebisu.updateRecall(default_model, 1, 1, 0.1)
