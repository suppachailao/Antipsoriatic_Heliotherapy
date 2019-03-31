from pathlib import Path
import numpy as np
import pandas as pd
import h5py
from matplotlib import pyplot as plt
from convertUnit import MdToDay, effTilT
from block import genTimeBlock

pd.set_option('display.max_columns', 15)

does = pd.read_hdf(Path(__file__).parent / 'result'/ 'does'/'smooth'/'does.h5') #read from br

month = ['Feb', 'March', 'Apirl', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #index name
stats = ['Mean', 'Std'] 
multiCol = pd.MultiIndex.from_product([does.columns, stats]) #multi-columns with 
statDoes = pd.DataFrame(index=month, columns=multiCol) #Empty data frame
statDoes.iloc[0 , 1::2] = does.loc['0206' :'0228', :].std(axis=0).round(3).values

print [i for i in range(9, 18)]

















