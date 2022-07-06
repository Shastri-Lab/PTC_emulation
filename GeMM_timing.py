import numpy as np


class PhotonicTensor:
    inputs = None
    weights = None
    constants = None

    iterations = 0
    matSize = (1,4)
    trail = None
    padA = None
    padB = None
    outputSize = np.array([0,0])

    def __init__(self, A, B, C=None, matSize=(1,4)):

        if matSize[0] > 0 and matSize[1] > 0 and isinstance(matSize[0], int) and isinstance(matSize[1], int):
            self.matSize = matSize
        else:
            raise RuntimeError("Please specify a positive integer for matrix size.")
            
        if A.shape[1] != B.shape[0]:
            raise RuntimeError("Incorrect input matrix dimension for dot product.")

        self.iterations = int(np.ceil(len(B) / self.matSize[1]))
        if len(B) % self.matSize[1] != 0:
            self.trail = self.matSize[1] - int(len(B) % self.matSize[1])
        else:
            self.trail = 0
            
        if A.shape[0] % self.matSize[0] != 0:
            self.padA = self.matSize[0] - int(A.shape[0] % self.matSize[0])
        else:
            self.padA = 0
            
        if B.shape[1] % self.matSize[0] != 0:
            self.padB = self.matSize[0] - int(B.shape[1] % self.matSize[0])
        else:
            self.padB = 0

        self.inputs = self.foldArray(np.asarray(A), flag="input")
        self.weights = self.foldArray(np.asarray(B), flag="weight")
        
        self.outputSize[0] = A.shape[0] + self.padA
        self.outputSize[1] = B.shape[1] + self.padB

        if C is not None:
            if np.array_equal(C.shape, self.outputSize-[self.padA, self.padB]):
                self.constants = C
            else:
                raise RuntimeError("Matrix C must be the same size as the output matrix.")
        
        self.inputs = np.reshape(self.inputs, (self.iterations, self.outputSize[0], self.matSize[1]))
        self.weights = np.reshape(self.weights.T, (self.iterations, self.outputSize[1], self.matSize[1]))

    def foldArray(self, mat, flag):
        if flag == "input":
            temp = np.zeros([mat.shape[0], self.trail])
            mat = np.append(mat, temp, axis=1)
            temp = np.zeros([self.padA, mat.shape[1]])
            mat = np.append(mat, temp, axis=0)
            return np.vstack(np.hsplit(mat, self.iterations))
        elif flag == "weight" or flag == "const":
            temp = np.zeros([self.trail, mat.shape[1]])
            mat = np.append(mat, temp, axis=0)
            temp = np.zeros([mat.shape[0], self.padB])
            mat = np.append(mat, temp, axis=1)
            return np.hstack(np.vsplit(mat, self.iterations))

    def dotproduct(self, a, b):
        '''
            Dot product between sub arrays. Please replace this with experimental function
        '''
        return np.dot(a, b)
    
    def DotProduct_break_time(self):  #Just measure the time of empty loop
        for i in range(0, self.iterations, 1):
            for j in range(0, self.outputSize[0]-self.matSize[0]+1, self.matSize[0]):
                for k in range(0, self.outputSize[1]-self.matSize[0]+1, self.matSize[0]):
                    continue
                    #output[j:(j+self.matSize[0]), k:(k+self.matSize[0])] += self.dotproduct(self.inputs[i, j:(j+self.matSize[0]), :], self.weights[i, k:(k+self.matSize[0]), :].T)
        #return output[0:(self.outputSize[0]-self.padA), 0:(self.outputSize[1]-self.padB)]
        return
        
    def DotProduct_combine_time(self):  #Just store +=0 instead of the actual small dot product, to measure combine time
        output = np.zeros(self.outputSize)
        for i in range(0, self.iterations, 1):
            for j in range(0, self.outputSize[0]-self.matSize[0]+1, self.matSize[0]):
                for k in range(0, self.outputSize[1]-self.matSize[0]+1, self.matSize[0]):
                    output[j:(j+self.matSize[0]), k:(k+self.matSize[0])] += 0
        return output[0:(self.outputSize[0]-self.padA), 0:(self.outputSize[1]-self.padB)]
        
    def count(self):  #Just to count the time of dot products
        count = 0
        for i in range(0, self.iterations, 1):
            for j in range(0, self.outputSize[0]-self.matSize[0]+1, self.matSize[0]):
                for k in range(0, self.outputSize[1]-self.matSize[0]+1, self.matSize[0]):
                    #output[j:(j+self.matSize[0]), k:(k+self.matSize[0])] += self.dotproduct(self.inputs[i, j:(j+self.matSize[0]), :], self.weights[i, k:(k+self.matSize[0]), :].T)
        #return output[0:(self.outputSize[0]-self.padA), 0:(self.outputSize[1]-self.padB)]
                    count = count + 1
        return count

    
if __name__ == "main":
    a = np.array([[1, 2, 3], [5, 6, 7], [9, 10, 11], [13, 14, 15]])
    b = np.array([[11, 12, 13, 14], [15, 16, 17, 18], [19, 20, 21, 22]])
    PT = PhotonicTensor(a, b, C=None, matSize=(1,2))
    PT.testDotProduct()
    print(np.dot(a, b))
