# file_utility.py

import os,bstu, pandas


def append(_source_string, _target_file):
    if os.path.exists(_target_file):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not    
    _file_object = open(_target_file, append_write)
    _file_object.write(_source_string)
    _file_object.close() 
    bstu.log('file_appended: {0}'.format(_target_file)) 


def append_line(_source_string, _target_file):
    if os.path.exists(_target_file):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not  
    _file_object = open(_target_file, append_write)
    _file_object.write('\n{}'.format(_source_string))
    _file_object.close() 
    #bstu.log('file_appended: {0}'.format(_target_file)) 
    
    
def csvfile_to_dataframe(_file, _sep=','):
    _df = pandas.read_csv(_file, _sep, encoding = "ISO-8859-1")
    return _df


def csvfile_to_dataframe_pickle(_input_csv_file, _output_pickle_file, _sep=','):
    _df = csvfile_to_dataframe(_input_csv_file, _sep)
    bstu.pickler(_df, _output_pickle_file)
            
def csvfile_to_dataframe2(_input_csv_file):
    _df = pandas.read_csv(_input_csv_file, _delimiter="\t", quoting=csv.QUOTE_NONE, encoding='utf-8')
    return _df 

        
def dict_values_to_concatenated_text_file(_input_dict, _output_text_file, _sep='\n'):
    _output_str = ''
    for _key in _input_dict:
        _value = _input_dict[_key]
        _output_str = _output_str + '{}{}'.format(_value, _sep)
    write(_output_str, _output_text_file)    
    bstu.logg('this file was created from dict values: {}'.format(_output_text_file))
    
        
def file_to_dict(_source_file, _key_value_sep=' '):
    _output_dict = dict()
    _key_value_pairs = read_lines(_source_file)
    for _key_value_pair in _key_value_pairs:
        _key_value_pair_split = _key_value_pair.split(_key_value_sep)
        if _key_value_pair_split.__len__() != 2:
            continue
              
        _output_dict[_key_value_pair_split[0].strip()] = _key_value_pair_split[1].strip()
    return _output_dict
        
        
def file_to_matrix(_file):
    _matrix = []
    _file_object = open(_file, 'r')
    _lines = _file_object.ReadLines()
    for _i in range(0, _lines.__len__()):
        _line_split = _lines[i].split()
        _row = []
        for _j in range(0, _line_split.__len__()):
            _row.append(float(_line_split[_j]))
        
        _matrix.append(_row)
    _file_object.close()
    return _matrix
    

def int_string_dict_to_text_file(_source_dict_fpf, _target_text_full_filename, _sep=' '):
    _dict = bstu.unpickler(_source_dict_fpf)
    _fo = open(_target_text_full_filename, 'w')
    _lines_to_write = []
    for _ocrid in _dict:
        _lines_to_write.append('{0}{2}{1}\n'.format(_ocrid, _dict[_ocrid]))
    _fo.writelines(_lines_to_write)
    _fo.close()
    bstu.log('created file {0}'.format(_target_text_full_filename))    
    
    
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
    
    
def matrix_to_file( _matrix, _file, _should_use_first_line_for_matrix_shape = False):
    _m = _matrix.__len__()
    if _m == 0:
        return
    _n = _matrix[0].__len__()
    _file_object = open(_file, 'w')
    if _should_use_first_line_for_matrix_shape:
        _file_object.write('{0} {1}\n'.format(_m, _n))
    for _i in range(0, _m):      
        _row_str = ''
        for _j in range(0, _n):
            _row_str = _row_str + '{0} '.format(_matrix[_i][_j])
        _row_str = _row_str.strip()
        _file_object.write('{0}\n'.format(_row_str))        
    _file_object.close()
    bstu.logg('matrix of shape {0}x{1} written to file named {2}'.format(_m, _n, _file))
    
    
def vector_to_file(_vector, _file, _delimiter = ' '):
    _vector_str = ''
    for _i in range(0, _vector.__len__()):
        _vector_str = _vector_str + '{0}{1}'.format(_vector[_i], _delimiter)    
    _file_object = open(_file, 'w')
    _file_object.write(_vector_str.strip(_delimiter))
    _file_object.close()
    bstu.logg('vector of length {0} written to file named {1}'.format(_vector.__len__(), _file))
    

def read_lines(_filename):
    _file_object = open(_filename, 'r')
    _lines = open(_filename, 'r').readlines()
    _file_object.close()
    return _lines
    
    
def write(_source_string, _target_file, _should_append=True):
    if _should_append:
        _file_object = open(_target_file, 'a')
        _file_object.write(_source_string)
        _file_object.close() 
        bstu.log('file_appended: {0}'.format(_target_file)) 
    else:
        _file_object = open(_target_file, 'w')
        _file_object.write(_source_string)
        _file_object.close() 
        bstu.log('file_created: {0}'.format(_target_file))    