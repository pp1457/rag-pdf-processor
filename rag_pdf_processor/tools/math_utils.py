import numpy as np

def cos_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim
