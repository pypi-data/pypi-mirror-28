import bstu, re, math
            

def are_dicts_equivalent(_dict1, _dict2):
    for _key in _dict1:
        if _key not in _dict2:
            return False
        if _dict1[_key] != _dict2[_key]:
            return False
    return True
    
    
def concat_dict_values(_source_dict, sep=' '):
    _output_values_str = ''
    for _key in _source_dict:
        _output_values_str = _output_values_str + '{0}{1}'.format(_source_dict[_key], sep)
    return _output_values_str

    
def create_sequenced_list(_start, _count):
    _sequenced_list = []
    for _i in range(_start, _start+_count):
        _sequenced_list.append(_i)
    return _sequenced_list


def create_zeros_list(_length):
    _output = []
    for _i in range(0, _length):
        _output.append(0)
    return _output


def daily_timestamp(_day_to_convert):
    _day_to_convert_year = _day_to_convert.year 
    _day_to_convert_month = str(_day_to_convert.month).zfill(2)
    _day_to_convert_day = str(_day_to_convert.day).zfill(2)
    return '{}{}{}'.format(_day_to_convert_year, _day_to_convert_month, _day_to_convert_day)    
       
    
def get_lidxs_of_substring(_fulltext, _subtext, _delimiter=' '):
    _substring_index = _fulltext.find(_subtext)
    if _substring_index < 0:
        return []        
    _preceding_delimiter_count = _fulltext[0:_substring_index].count(_delimiter)  
    return create_sequenced_list( _preceding_delimiter_count, _subtext.split(_delimiter).__len__())


def get_lidxs_of_substring_using_regex(_fulltext, _regex_str, _delimiter=' '):
    _match_object = re.search(_regex_str, _fulltext)
    if _match_object == None:
        return []
    _preceding_delimiter_count = _fulltext[0:_match_object.start()].count(_delimiter)
    _desired_word_count = _match_object.group().split(_delimiter).__len__()
    return create_sequenced_list( _preceding_delimiter_count, _desired_word_count)
    

def get_sub_dict(_source_dict, _sub_keys):
    _sub_dict = dict()
    for _sub_key in _sub_keys:
        if _sub_key in _source_dict:
            _sub_dict[_sub_key] = _source_dict[_sub_key]
    return _sub_dict
        
        
def glove_txt_file_to_dict_and_mat_pickles1(_glove_file):
    glove_txt_file_to_dict_and_mat_pickles(_glove_file, 
                                           '{0}.dict.p'.format(_glove_file),
                                           '{0}.reverse.dict.p'.format(_glove_file),
                                           '{0}.mat.p'.format(_glove_file))


def glove_txt_file_to_dict_and_mat_pickles(_glove_file, _dict_file, _reverse_dict_file, _mat_file):
    # txt file format : each line begins with the word string followed by its vector of floats, space delimited
    bstu.log('starting')
    print('reading file')
    _fo = open(_glove_file, 'r', encoding="utf8")
    _lines = _fo.readlines()
    _fo.close()
    print('finished reading file, line count was:{0}'.format(_lines.__len__()))
    _word_widx_dict = dict()
    _word_widx_reverse_dict = dict()
    _word_vector_mat = []
    print('creating dictionary and 2-d list objects')
    for _widx in range(0, _lines.__len__()):
        if _widx % 100000 == 0:
            print('{0} words completed'.format(_widx))
        _line_split = _lines[_widx].split()
        if _line_split.__len__() <= 2:
            continue
        _word_str = _line_split[0]
        _word_glove = [float(_x) for _x in _line_split[1:_line_split.__len__()]]
        # add to dict
        _word_widx_dict[_word_str] = _widx
        _word_widx_reverse_dict[_widx] = _word_str
        _word_vector_mat.append(_word_glove)
    # add a row of zeros to the word vector matrix
    _word_vector_mat.append(create_zeros_list(_word_vector_mat[0].__len__()))
    print('creating pickles')
    bstu.pickler(_word_widx_dict, _dict_file)
    bstu.pickler(_word_widx_reverse_dict, _reverse_dict_file)
    bstu.pickler(_word_vector_mat, _mat_file)
    print('finished')


def index_string_text_file_to_dict(_text_file, _should_include_empty_or_whitespace_values = False,
                                          _is_index_int = True):
    _fo = open(_text_file, 'r')
    _lines = _fo.readlines()
    _fo.close()
    _dict = dict()
    for i in range (0, _lines.__len__()):
        _lines_split = _lines[i].split()
        if _lines_split.__len__() <= 1:
            continue
        _index_key_str = _lines_split[0]
        _value_str = ''
        if _lines[i].__len__() > _index_key_str.__len__():
            _value_str = _lines[i][_index_key_str.__len__():]
        if is_string_empty_or_all_white_space(_value_str) and not _should_include_empty_or_whitespace_values:
            continue
        if _is_index_int:
            _dict[int(_index_key_str)] = _value_str.strip()
        else:
            _dict[_index_key_str] = _value_str.strip()
    return _dict


def int_string_text_file_to_dict(_filename, _separator=' '):
    _file_object = open(_filename, 'r')
    _lines = open(_filename, 'r').readlines()
    _file_object.close()
    _dict = dict()
    _exception_count = 0
    for _i in range(0, _lines.__len__()):
        try: 
            _line_split = _lines[_i].split(_separator)
            if _line_split.__len__() < 2:
                continue
            _key = int(_line_split[0])
            _value = ''
            for _j in range(1, _line_split.__len__()):
                _value = _value + _line_split[_j] + ' '
            _dict[_key] = _value.strip()
        except:
            print('exception on {0}th line: {1}'.format(_i, _lines[_i]))
            _exception_count = _exception_count + 1
    print('dictionary_length:{0}, exception_count:{1}'.format(_dict.__len__(), _exception_count))
    return _dict


def intersection_of_sets(_sets):
    if _sets.__len__() <= 0:
        return set()
    _intersection = _sets[0]
    for _i in range(1, _sets.__len__()):
        _intersection = _intersection.intersection(_sets[_i])
    return _intersection


def is_empty_or_all_white_space(s):
    return '' == s.strip()


def is_null_or_empty_or_all_white_space(s):
    return s == None or '' == s.strip()


def is_sublist(_list, _sublist_candidate):
    if _sublist_candidate.__len__() > _list.__len__():
        return False
    for _i in range(0, _list.__len__()):
        if _sublist_candidate.__len__() > _list.__len__() - _i:
            return False
        for _j in range(0, _sublist_candidate.__len__()):
            if _sublist_candidate[_j] != _list[_i+_j]:
                break
            if _j == _sublist_candidate.__len__() - 1:
                return True
    return False


def key_value_dataframe_columns_to_dict_pickle(_df, _output_file, _key_column, _value_column):
    _dict = dict()
    _count = 0
    for _i in range(0, _df.__len__()):
        if (_count % 10000) == 0:
            bstu.logg(_count)
        _count = _count + 1
        _key = int(_df.iloc[_i][_key_column])
        _value = _df.iloc[_i][_value_column]
        _dict[_key] = _value
    bstu.pickler(_dict, _output_file)


def list_to_lol_partitions(_list, _number_of_partitions):
    _partitions = []
    _partition_index = 0
    _elements_per_partition = int(math.ceil(_list.__len__()/_number_of_partitions))
    for _partition_index in range(0, _number_of_partitions):
        _partition = []
        for _local_index in range(0, _elements_per_partition):
            _global_index = _partition_index*_elements_per_partition + _local_index
            if _global_index >= _list.__len__():
                break
            _partition.append(_list[_global_index])
        _partitions.append(_partition)
    return _partitions
    

def location_indexes_of_sublist(_list, _sublist_candidate):
    if _sublist_candidate.__len__() > _list.__len__():
        return []
    for _i in range(0, _list.__len__()):
        if _sublist_candidate.__len__() > _list.__len__() - _i:
            return []
        for _j in range(0, _sublist_candidate.__len__()):
            if _sublist_candidate[_j] != _list[_i+_j]:
                break
            if _j == _sublist_candidate.__len__() - 1:
                return create_sequenced_list(_i, _sublist_candidate.__len__())
    return []    


def max_of_mat(_mat):
    _max_element = 0.0
    for _i in range(0, _mat.__len__()):
        if _mat[_i].__len__() <= 0:
            continue
        for _j in range(0, _mat[_i].__len__()):
            if _mat[_i][_j] > _max_element:
                _max_element = _mat[_i][_j]
    return _max_element
        

def min_of_mat(_mat):
    _min_element = 0.0
    for _i in range(0, _mat.__len__()):
        if _mat[_i].__len__() <= 0:
            continue
        for _j in range(0, _mat[_i].__len__()):
            if _mat[_i][_j] < _min_element:
                _min_element = _mat[_i][_j]
    return _min_element    


def print_head(_container, _max_entries_to_print = 10):
    if _max_entries_to_print > _container.__len__():
        _max_entries_to_print = _container.__len__()
    for _i in range(0, _max_entries_to_print):
        print(_container[_i])

        
def print_list2d(_l):
    for _i in range(0, _l.__len__()):
        print(_l[_i])

        
def print_lol(_lol):
    print_list2d(_lol)
        

def print_dict(_d, _max_entries_to_print = -1):
    # _d is the dictionary to display
    if _max_entries_to_print <= 0:
        _max_entries_to_print = _d.__len__()
    _count = 0    
    for _key in _d:
        print('{0}: {1}\r\n'.format(_key, _d[_key]))
        _count = _count + 1
        if _count >= _max_entries_to_print:
            break
        

def read_file_into_2d_list_float(_filename, _separator=' '):
    _file_object = open(_filename, 'r')
    _lines = _file_object.readlines()
    _file_object.close()
    _output_list = []
    for _i in range(0, _lines.__len__()):
        _row_string_split = _lines[_i].split(_separator)
        _row = []
        for _j in range(0, _row_string_split.__len__()):
            _row.append(float(_row_string_split[_j]))
        _output_list.append(_row)
    return _output_list


def read_string_int_dictionary_from_file(_filename, _separator=' '):
    _file_object = open(_filename, 'r')
    _lines = open(_filename, 'r').readlines()
    _file_object.close()
    _dictionary = dict()
    for _i in range(0, _lines.__len__()):
        _line_split = _lines[_i].split(_separator)
        if _line_split.__len__() != 2:
            continue
        _dictionary[_line_split[0]] = int(_line_split[1])
    return _dictionary


def select_from_df_where_col_eq_val(_df, _column, _value):
    return _df[(_df[_column] == _value)]


def shape_list2d(_l):
    _m = _l.__len__()
    if _m == 0:
        return '0 x 0'
    _n = _l[0].__len__()
    return '{0} x {1}'.format(_m, _n)
    

def special_split(_original_list, _split_distance_threshold):
    _output_list2d = []
    if _original_list.__len__() <= 0:
        return _output_list2d
    _new_sub_list = []       
    _j = 0
    _zeroith_index_value = _original_list[0]
    while _j < _original_list.__len__():
        if _original_list[_j] - _zeroith_index_value > _split_distance_threshold:
            # in this case, there is a gap and we need to add the sub list and start a new one
            _output_list2d.append(_new_sub_list)
            _new_sub_list = []
            _zeroith_index_value = _original_list[_j]
        _new_sub_list.append(_original_list[_j])         
        _j = _j + 1   
    _output_list2d.append(_new_sub_list)
    return _output_list2d


def string_string_text_file_to_dict(_filename, _entry_separator = '\n', _key_value_separator = ' '):
    _file_object = open(_filename, 'r')
    _text = open(_filename, 'r').read()
    _file_object.close()    
    _entries = _text.split(_entry_separator)
    _dict = dict()
    for _i in range(0, _entries.__len__()):
        try: 
            _entry_split = _entries[_i].split(_key_value_separator)
            if _entry_split.__len__() < 2:
                continue
            _key = _entry_split[0] 
            _value = ''
            for _j in range(1, _entry_split.__len__()):
                _value = _value + _entry_split[_j] + ' '
            _dict[_key] = _value.strip()
        except:
            print('exception on {0}th line: {1}'.format(_i, _entries[_i]))
    return _dict


# transform matrix elements into grey-scale, where min weight is 0 (black) and max weight is 255 (white)
def transform_matrix_values_to_greyscale(_matrix):
    # find min and max values of matrix
    _matrix_min = min_of_mat(_matrix)
    _matrix_max = max_of_mat(_matrix)
    # transform every weight w by:
    # (target_max - target_min)/(max_w - min_w) * w + (target_max - target_min)/(max_w - min_w) * (target_min - min_w)
    _target_min = 0
    _target_max = 255
    _stretcher_value = (_target_max - _target_min)/(_matrix_max - _matrix_min)
    _gs_matrix = []
    for _i in range(0, _matrix.__len__()):
        _gs_row = []
        for _j in range(0, _matrix[0].__len__()):
            _matrix_element = _matrix[_i][_j]
            _gs_matrix_element = int(math.floor(_stretcher_value * _matrix_element + _stretcher_value * (_target_min - _matrix_min)))
            _gs_row.append(_gs_matrix_element)
        _gs_matrix.append(_gs_row)
    return _gs_matrix


def vocab_dict_to_reverse_dict(_source_dict_fpf, _target_dict_fpf): # fpf := full-pickle-file
    _source_dict = bstu.unpickler(_source_dict_fpf)
    _reverse_dict = dict()
    for _k in _source_dict:
        _v = _source_dict[_k]
        _reverse_dict[int(_v)] = _k
    bstu.pickler(_reverse_dict, _target_dict_fpf)
    

def union_of_sets(_sets):
    if _sets.__len__() <= 0:
        return set()
    _union = _sets[0]
    for _i in range(1, _sets.__len__()):
        _union = _union.union(_sets[_i])
    return _union    
    