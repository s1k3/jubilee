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

# age.view()
# bad_words.view()
# output.view(sim=outputping)

# plt.show()

import csv

bad_words = ["bitch", "slut", "brown", "black", "suck", "fuck", "boobs", "ass"]


def count_bad_words(sentence):
    count = 0
    words = sentence.lower().split(" ")
    for word in words:
        if word in bad_words:
            count += 1
    return count


outputs = []
outputs += ["sentence,output,age,type"]
with open('output.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        outputping.input['age'] = int(row['age'])
        outputping.input['word'] = count_bad_words(row['Sentence'])

        # Crunch the numbers
        outputping.compute()
        value = outputping.output['output']
        label = ""
        if 0 <= value <= 1:
            label = "low"
        elif 1 <= value <= 2:
            label = "medium"
        elif 2 <= value <= 3:
            label = "high"
        outputs += [row['Sentence'] + "," + row['output'] + "," + row["age"] + "," + label]
file = open("output_final.csv", "w+")
for line in outputs:
    file.write(line + "\n")
file.close()