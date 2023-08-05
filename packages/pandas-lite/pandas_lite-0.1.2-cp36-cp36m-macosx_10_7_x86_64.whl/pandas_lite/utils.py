import decimal
from typing import List
import numpy as np
from pandas_lite._libs import validate_arrays as va


_DT = {'i': 'int', 'f': 'float', 'b': 'bool', 'O': 'str'}
_KIND = {'int': 'i', 'float': 'f', 'bool': 'b', 'str': 'O'}
_KIND_LIST = {'int': ['i'], 'float': ['f'], 'bool': ['b'],
              'str': ['O'], 'number': ['i', 'f']}
_DTYPES = {'int': 'int64', 'float': 'float64', 'bool': 'bool', 'str': 'str'}
_KIND_NP = {'i': 'int64', 'f': 'float64', 'b': 'bool', 'O': 'O'}

_AXIS = {'rows': 0, 'columns': 1}


def _get_decimal_len(num):
    if not np.isfinite(num):
        return 0
    return abs(decimal.Decimal(str(num)).as_tuple().exponent)


def _get_whole_len(num):
        return len(str(num).split('.')[0])


def check_duplicate_list(lst: List) -> None:
    s = set()
    for i, elem in enumerate(lst):
        if elem in s:
            raise ValueError(f'Column {elem} is selected more than once')
        s.add(elem)


def check_empty_slice(s: slice) -> bool:
    return (s.start is None and
            s.stop is None and
            (s.step is None or s.step == 1))


def try_to_squeeze_array(arr):
    if arr.ndim == 1:
        return arr
    if arr.ndim == 2 and arr.shape[1] == 1:
        return arr.squeeze()
    else:
        raise ValueError('Array must be one dimensional or two dimensional '
                         'with 1 column')


def convert_bytes_or_unicode(arr):
    if arr.dtype.kind == 'S':
        arr = arr.astype('U').astype('O')
    elif arr.dtype.kind == 'U':
        arr = arr.astype('O')
    return arr


def is_scalar(value):
    return isinstance(value, (int, str, float, np.number, bool, bytes))


def convert_list_to_single_arr(values, column):
    arr = np.array(values)
    kind = arr.dtype.kind
    if kind in 'ifbO':
        return arr
    elif kind in 'US':
        return np.array(values, dtype='O')


def maybe_convert_1d_array(arr, column=None):
    arr = try_to_squeeze_array(arr)
    kind = arr.dtype.kind
    if kind in 'ifb':
        return arr
    elif kind == 'U':
        return arr.astype('O')
    elif kind == 'S':
        return arr.astype('U').astype('O')
    elif kind == 'O':
        return va.validate_strings_in_object_array(arr, column)
    else:
        raise NotImplementedError(f'Data type {kind} unknown')


def convert_list_to_arrays(value):
    # check if one dimensional array
    if is_scalar(value[0]):
        arr = convert_list_to_single_arr(value)
        return [maybe_convert_1d_array(arr)]
    else:
        arr = np.array(value, dtype='O')
        if arr.ndim == 1:
            arr = arr[:, np.newaxis]
    if arr.ndim != 2:
        raise ValueError(f'List converted to {arr.ndim} dimensions. '
                         'Only 1 or 2 dimensions allowed')

    arrs = []
    for i in range(arr.shape[1]):
        a = convert_list_to_single_arr(arr[:, i].tolist())
        a = maybe_convert_1d_array(a)
        arrs.append(a)
    return arrs


def convert_array_to_arrays(arr):
    if arr.ndim == 1:
        arr = arr[:, np.newaxis]
    if arr.ndim != 2:
        raise ValueError('Setting array must be 1 or 2 dimensions')

    arrs = []
    for i in range(arr.shape[1]):
        a = np.array(arr[:, i].tolist())
        arrs.append(convert_bytes_or_unicode(a))
    return arrs


def is_entire_column_selection(rs, cs):
    return (isinstance(rs, slice) and isinstance(cs, str) and
            check_empty_slice(rs))


def validate_selection_size(key):
    if not isinstance(key, tuple):
        raise TypeError('You must provide both a row and column '
                        'selection separated by a comma')
    if len(key) != 2:
        raise TypeError('You must provide exactly one row selection '
                        'and one column selection')


def check_set_value_type(dtype, good_dtypes, name):
    if dtype not in good_dtypes:
            raise TypeError(f'Cannot assign {name} to column of '
                            f'type {_DT[dtype]}')


def check_valid_dtype_convet(dtype):
    if dtype not in _DTYPES:
        raise ValueError(f'{dtype} is not a valid type. Must be one '
                         f'of {list(_DTYPES.keys())}')
    return _DTYPES[dtype]


def convert_kind_to_dtype(kind):
    return _DT[kind]


def convert_kind_to_numpy(kind):
    return _KIND_NP[kind]


def convert_dtype_to_kind(dtype):
    return _KIND[dtype]


def get_kind_from_scalar(s):
    if isinstance(s, bool):
        return 'b'
    elif isinstance(s, (int, np.integer)):
        return 'i'
    elif isinstance(s, (float, np.floating)):
        return 'f'
    elif isinstance(s, (str, bytes)):
        return 'O'
    else:
        return False


def validate_array_size(arr, num_rows):
    if len(arr) != num_rows:
        raise ValueError(f'Mismatch number of rows {len(arr)} vs {num_rows}')


def validate_multiple_string_cols(arr):
    if arr.ndim == 1:
        return va.validate_strings_in_object_array(arr)
    arrays = []
    for i in range(arr.shape[1]):
        arrays.append(va.validate_strings_in_object_array(arr[:, i]))
    return np.column_stack(arrays)


def get_selection_object(rs, cs):
    is_row_list = isinstance(rs, (list, np.ndarray))
    is_col_list = isinstance(cs, (list, np.ndarray))
    if is_row_list and is_col_list:
        return np.ix_(rs, cs)
    return rs, cs


# def check_compatible_kinds(k1, k2):
#     if k1 == k2:
#         return True
#     if k1 in 'if' and k2 in 'if':
#         return True
#     if k1 == 'O' and k2 in 'SU':
#         return True
#     raise TypeError(f'Incompaitble dtypes {_DT[k1]} and {_DT[k2]}')


def check_compatible_kinds(kinds1, kinds2):
    for k1, k2 in zip(kinds1, kinds2):
        if k1 == k2:
            continue
        if k1 in 'if' and k2 in 'if':
            continue
        raise TypeError(f'Incompaitble dtypes {_DT[k1]} and {_DT[k2]}')
    return True


def convert_axis_string(axis):
    try:
        return _AXIS[axis]
    except KeyError:
        raise KeyError('axis must be either "rows" or "columns')


def convert_clude(clude, arg_name):
    if isinstance(clude, str):
        all_clude = try_to_convert_dtype(clude)
    elif isinstance(clude, list):
        all_clude = []
        for dt in clude:
            all_clude.extend(try_to_convert_dtype(dt))
    else:
        raise ValueError(f'Must pass a string or list of strings '
                         'to {arg_name}')
    return all_clude


def try_to_convert_dtype(dtype):
    try:
        return _KIND_LIST[dtype]
    except KeyError:
        raise KeyError(f"{dtype} must be one/list of "
                       "either ('float', 'integer', 'bool',"
                       "'str', 'number')")
