import numpy as np
import sys

def calerror(a, b, c, d):
    asig = np.sqrt(a)
    bsig = np.sqrt(b)
    csig = np.sqrt(c)
    dsig = np.sqrt(d)

    aerror = (1/(c+d))*asig
    berror = (1/(c+d))*bsig
    cerror = ((a+b)/((c+d)*(c+d)))*csig
    derror = ((a+b)/((c+d)*(c+d)))*dsig

    error = np.sqrt(aerror*aerror + berror*berror + cerror*cerror + derror*derror)

    print("value : {}".format((a+b)/(c+d)))
    print("error : {}".format(error))
    
    

def main():
    args = sys.argv
    a = args[1]
    b = args[2]
    c = args[3]
    d = args[4]
    calerror(float(a), float(b), float(c), float(d))

if __name__=='__main__':
    main()


    
