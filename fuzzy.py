import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


age = ctrl.Antecedent(np.arange(18, 66, 1), 'age')
bad_words = ctrl.Antecedent(np.arange(1, 11, 1), 'word')
output = ctrl.Consequent(np.arange(0, 4, 1), 'output')

# Custom membership functions can be built interactively with a familiar,
# Pythonic API


age.automf(3, names=("low", "medium", "high"))
bad_words.automf(3, names=("low", "medium", "high"))
output.automf(3, names=("low", "medium", "high"))

rule1 = ctrl.Rule(age['low'] & bad_words['low'], output['low'])
rule2 = ctrl.Rule(age['low'] & bad_words['medium'], output['medium'])
rule3 = ctrl.Rule(age['low'] & bad_words['high'], output['high'])
rule4 = ctrl.Rule(age['medium'] & bad_words['low'], output['medium'])
rule5 = ctrl.Rule(age['medium'] & bad_words['medium'], output['medium'])
rule6 = ctrl.Rule(age['medium'] & bad_words['high'], output['high'])
rule7 = ctrl.Rule(age['high'] & bad_words['low'], output['medium'])
rule8 = ctrl.Rule(age['high'] & bad_words['medium'], output['high'])
rule9 = ctrl.Rule(age['high'] & bad_words['high'], output['high'])

outputping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
outputping = ctrl.ControlSystemSimulation(outputping_ctrl)

outputping.input['age'] = 22
outputping.input['word'] = 1

# Crunch the numbers
outputping.compute()
value=outputping.output['output']
label=""
if 0<=value and value<=1:
    label="low"
elif 1<=value and value<=2:
    label="medium"
elif 2<=value and value<=3:
    label="high"
print(value,label)

# age.view()
# bad_words.view()
# output.view(sim=outputping)

# plt.show()
