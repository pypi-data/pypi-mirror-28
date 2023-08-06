def in_notebook():
    '''Simple function to check if module is loaded in a notebook'''
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

#Global variable to keep track of whether the output_notebook command was run    
bokeh_ouput_notebook_called = False
mpl_ouput_notebook_called = False   

def mpl_output_notebook():
    from IPython import get_ipython
    ipython = get_ipython()
    #ipython.magic('matplotlib inline')
    mpl_ouput_notebook_called = True

def get_data_from_file(path, delim=','):
    '''Reads data from a file, splitting rows at the delimiter.
    Returns data in a 2-dimensional numpy array.
    '''
    import csv
    with open(path, newline='') as openfile:
        reader = csv.reader(openfile, delimiter=delim)
        data=[]
        for row in reader:
            for col in range(len(row)):
                append = True
                try:
                    row[col] = float(row[col])
                except ValueError:
                    append=False
                    break
            if append:
                data.append(row)
        ret = np.transpose(np.array(data, dtype=float))
    return ret

#These are used for checking whether something is an instance of
#an array or a number.
import numpy as np
number_types = (int, float, np.int8, np.int16, np.int32, np.int64,\
                np.uint8, np.uint16, np.uint32, np.uint64,\
                np.float16, np.float32, np.float64\
                )
int_types = (int, np.int8, np.int16, np.int32, np.int64,\
                np.uint8, np.uint16, np.uint32, np.uint64\
                )
array_types = (tuple, list, np.ndarray)