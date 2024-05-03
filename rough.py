from numba import jit, cuda 
@jit(target_backend='cuda')
def prin():
    for i in range(1000):
        print("hi")
def prinn():
    for i in range(1000):
        print("hello")
if __name__=="__main__":
    prin()
    