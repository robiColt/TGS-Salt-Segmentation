#!/usr/bin/env python
# coding: utf-8

# In[2]:

import numpy as np

def iou_np(mask, predict):
    intersection = np.logical_and(mask, predict).astype(int)
    union = np.logical_or(mask, predict).astype(int)
    intersec_sum = np.sum(intersection)
    union_sum = np.sum(union)
    return 0 if union_sum == 0 else intersec_sum/union_sum


import numpy as np     # linear algebra library
import pandas as pd    
import tensorflow as tf
from random import randint
from keras import backend as K


# In[3]:

def iou(y_true, y_pred):
    import numpy as np     # linear algebra library
    import pandas as pd    
    import tensorflow as tf
    from random import randint
    from keras import backend as K
    prec = []
    for t in np.arange(0.5, 1.0, 0.05):
        y_pred = tf.to_int32(y_pred > t)
        score, up_opt = tf.metrics.mean_iou(y_true, y_pred, 2)
        K.get_session().run(tf.local_variables_initializer())
        with tf.control_dependencies([up_opt]):
            score = tf.identity(score)
        prec.append(score)
    return K.mean(K.stack(prec), axis=0)


# In[4]:

# def jaccard_distance_loss(y_true, y_pred, smooth=100):
#     """
#     Jaccard = (|X & Y|)/ (|X|+ |Y| - |X & Y|)
#             = sum(|A*B|)/(sum(|A|)+sum(|B|)-sum(|A*B|))
    
#     The jaccard distance loss is usefull for unbalanced datasets. This has been
#     shifted so it converges on 0 and is smoothed to avoid exploding or disapearing
#     gradient.
    
#     Ref: https://en.wikipedia.org/wiki/Jaccard_index
    
#     @url: https://gist.github.com/wassname/f1452b748efcbeb4cb9b1d059dce6f96
#     @author: wassname
#     """
    
#     import numpy as np     # linear algebra library
#     import pandas as pd    
#     import tensorflow as tf
#     from random import randint
#     from keras import backend as K
    
#     intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
#     sum_ = K.sum(K.abs(y_true) + K.abs(y_pred), axis=-1)
#     jac = (intersection + smooth) / (sum_ - intersection + smooth)
#     return (1 - jac) * smooth







# In[5]:


"""
Here is a dice loss for keras which is smoothed to approximate a linear (L1) loss.
It ranges from 1 to 0 (no error), and returns results similar to binary crossentropy
"""

# define custom loss and metric functions 


def dice_coef(y_true, y_pred, smooth=1):
    """
    Dice = (2*|X & Y|)/ (|X|+ |Y|)
         =  2*sum(|A*B|)/(sum(A^2)+sum(B^2))
    ref: https://arxiv.org/pdf/1606.04797v1.pdf
    """
    
    import numpy as np     # linear algebra library
    import pandas as pd    
    import tensorflow as tf
    from random import randint
    from keras import backend as K
    
    
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    return (2. * intersection + smooth) / (K.sum(K.square(y_true),-1) + K.sum(K.square(y_pred),-1) + smooth)

def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)

