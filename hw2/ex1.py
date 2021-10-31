import string
import base64
from utils import get_value_from_parameters
import ast
import hashlib as _

A = string.printable

def inverse(a,b):
    old_r, r = a,b
    old_s, s = 1,0
    old_t, t = 0,1
    while r != 0:
        q = old_r//r
        old_r, r = r,old_r-q*r
        old_s, s = s,old_s-q*s
        old_t, t = t,old_t-q*t
    return old_s

def encrypt(K,plaintext):
    a,b= K
    x = [f(x)for x in list(plaintext)]
    y = [(a*c + b )%n for c in x]
    ciphertext = ''.join([g(c) for c in y])
    return ciphertext

def decrypt(K,ciphertext):
    a,b = K
    new_a = inverse(a,n)
    return encrypt((new_a,-b*new_a),ciphertext) 

def checksum(*args):
    data = ';'.join(map(str, args)).encode()
    return _.new('sha256', data=data).hexdigest()

f = lambda x: A.index(x)
g = lambda x: A[x]
n = len(A)
param = '284001-parameters.txt'
# 1.
K = ast.literal_eval(get_value_from_parameters(param, 'Q1a_K'))
s = ast.literal_eval(get_value_from_parameters(param,'Q1a_M'))
new_s = base64.b64decode(s).decode('utf-8')
encr_s = encrypt(K,new_s)
def_s = base64.b64encode(encr_s.encode(encoding = 'utf-8'))
print(def_s)
# 2.
K = ast.literal_eval(get_value_from_parameters(param,'Q1b_K'))
s = ast.literal_eval(get_value_from_parameters(param, 'Q1b_C'))
new_s = base64.b64decode(s).decode("utf-8") 
decr_s = decrypt(K,str(new_s))
print(decr_s)

# 3.
T = ast.literal_eval(get_value_from_parameters(param, 'Q1c_T'))
s = ast.literal_eval(get_value_from_parameters(param, 'Q1c_C'))
new_s = base64.b64decode(s).decode()
dico = {}
for i in range(len(new_s)):
    char = new_s[i]
    if char in dico:
        dico[char] += 1
    else:
        dico[char] = 1

dico = {k: v/len(new_s) for k,v in dico.items()}
# From this we get that ' ' -> J, 'e' -> 'p', 't' -> 'Y'
# By resolving the linear system , K = (9,99)
# A FAIRE A LA MAIN pour trouver K 
K = (9,99)
decr_s = decrypt(K,new_s)
print(decr_s)
H = ast.literal_eval(get_value_from_parameters(param, 'Q1c_H'))
assert checksum(base64.b64encode(decr_s.encode()).decode(),K[0],K[1]) == H