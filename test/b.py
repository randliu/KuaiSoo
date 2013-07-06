import pickle

a={'df':1232}
d={"ab":1,"fd":2,"e":a}
f=open("x","w")
pickle.dump(d, f)
f.close()