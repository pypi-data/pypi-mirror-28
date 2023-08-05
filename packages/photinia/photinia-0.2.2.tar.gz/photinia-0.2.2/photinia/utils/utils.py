#!/usr/bin/env python3

"""
@author: xi, anmx
@since: 2017-04-23
"""

import photinia as ph

import numpy as np
import pickle
import tensorflow as tf

pickle_loads = pickle.loads
pickle_dumps = pickle.dumps


def one_hot(index, dims, dtype=np.uint8):
    """Create one hot vector(s) with the given index(indices).

    :param index: int or list(tuple) of int. Indices.
    :param dims: int. Dimension of the one hot vector.
    :param dtype: Numpy data type.
    :return: Numpy array. If index is an int, then return a (1 * dims) vector,
        else return a (len(index), dims) matrix.
    """
    if isinstance(index, int):
        ret = np.zeros((dims,), dtype)
        ret[index] = 1
    elif isinstance(index, (list, tuple)):
        seq_len = len(index)
        ret = np.zeros((seq_len, dims), dtype)
        ret[range(seq_len), index] = 1.0
    else:
        raise ValueError('index should be int or list(tuple) of int.')
    return ret


def print_progress(current_loop,
                   num_loops,
                   msg='Processing',
                   interval=1000):
    """Print progress information in a line.

    :param current_loop: Current loop number.
    :param num_loops: Total loop count.
    :param msg: Message shown on the line.
    :param interval: Interval loops. Default is 1000.
    """
    if current_loop % interval == 0 or current_loop == num_loops:
        print('%s [%d/%d]... %.2f%%' % (msg, current_loop, num_loops, current_loop / num_loops * 100), end='\r')
    if current_loop == num_loops:
        print()


def read_variables(vars):
    """Get the value from a variable.

    :param vars: tf.Variable.
    :return: numpy.array value.
    """
    if not isinstance(vars, tf.Variable):
        raise ValueError('Invalid type for "var", expect %s but got %s' % (tf.Variable, type(vars)))
    session = ph.get_session()
    return session.run(vars)


def write_variable(vars, values):
    """Set the value to a variable.

    :param vars: tf.Variable.
    :param values: numpy.array value.
    """
    if not isinstance(vars, tf.Variable):
        raise ValueError('Invalid type for "var", expect %s but got %s' % (tf.Variable, type(vars)))
    session = ph.get_session()
    for var, value in zip(vars, values):
        var.load(value, session)
