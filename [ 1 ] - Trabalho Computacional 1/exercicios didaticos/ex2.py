import math

epsilons = [10**-2, 10**-4, 10**-6, 10**-8, 10**-10]

for epsilon in epsilons:
    k = (math.log(1) - math.log(epsilon)) / math.log(2)
    print(epsilon,"-", k)