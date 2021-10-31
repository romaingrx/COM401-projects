from utilsT import get_value_from_parameters
# Q2
param = '284001-parameters.txt'
p = get_value_from_parameters(param, 'Q2_p')
q = get_value_from_parameters(param, 'Q2_q')
g = get_value_from_parameters(param, 'Q2_g')
g = Mod(g,p)
c1 = get_value_from_parameters(param, 'Q2_c1')
c2 = get_value_from_parameters(param, 'Q2_c2')
c3 = get_value_from_parameters(param, 'Q2_c3')
c4 = get_value_from_parameters(param, 'Q2_c4')
c5 = get_value_from_parameters(param, 'Q2_c5')
c6 = get_value_from_parameters(param, 'Q2_c6')
c7 = get_value_from_parameters(param, 'Q2_c7')
c8 = get_value_from_parameters(param, 'Q2_c8')
c9 = get_value_from_parameters(param, 'Q2_c9')
c10 = get_value_from_parameters(param, 'Q2_c10')
C = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
C = [ Mod(ci,p) for ci in C]
mp = 1
for c in C:
    mp *= c
print(mp)
# 2.

m = get_value_from_parameters(param,'Q2_mdash')
m = Mod(m,p)
mx = discrete_log(m,g)
mi = list(str(bin(mx))[2:])
mi = len(list(filter(lambda x : x == '1', mi)))
mi = mi if mi <2**32 else 2**32
print(mx)
print(mi)

# m%q