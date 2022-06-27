import numpy as np
import copy
class AnvnUtils:
    
    def get_fuse_op():
        return {'min': np.min, 'max': np.max, 'mean': np.mean, 'median': np.median, 'sum': np.sum}

    @staticmethod
    def list2str(sep: str, data: list):
        return sep.join([str(d) for d in data])
    
    @staticmethod
    def middle_text_omission(data, num):
        if len(data) > num:
            return data[:num // 2] + '...' + data[(-num // 2) :] 
        return data
    
    @staticmethod
    def l2s_mto(sep, data, num):
        return AnvnUtils.middle_text_omission(AnvnUtils.list2str(sep, data), num)

    @staticmethod
    def deepcopy(*data):
        ds = []
        for d in data:
            if type(d) == np.ndarray:
                ds.append(d.copy())
            elif type(d) == dict:
                di = {}
                for k, v in d.items():
                    di[k] = AnvnUtils.deepcopy(v)
                ds.append(di)   
            elif type(d) == list and len(d) > 0 and type(d[0]) == np.ndarray:
                rd = []
                for dd in d:
                    rd.append(dd.copy())
                ds.append(rd)
            else:
                ds.append(copy.deepcopy(d))
        
        if len(ds) == 1:
            return ds[0]

        return tuple(ds)
    
    @staticmethod
    def range_str(*d):
        return np.array([str(i) for i in range(*d)], dtype=object)

    @staticmethod
    def n_range_str(n, *d):
        ns = []
        for _ in range(n):
            ns.append(AnvnUtils.range_str(*d))
        return ns 
    
    @staticmethod
    def flatten_list(ls):
        rs = []
        for l in ls:
            if type(l) == list:
                rs.extend(l)
            else:
                rs.append(l)
        return rs
    
    def delete_first(ls: list):
        ls = ls.copy()
        first = ls.pop(0)
        return ls, first 

if __name__ == '__main__':
    print(AnvnUtils.deepcopy([1], [2], [3]))
    print(AnvnUtils.deepcopy([1]))
    print(AnvnUtils.deepcopy({
        'a': 1,
        'b': [1, 2, np.array([1, 2])],
    }))
    print(AnvnUtils.range_str(10))
    print(AnvnUtils.range_str(1, 10))
    print(AnvnUtils.range_str(10, 1, -1))
    x = AnvnUtils.n_range_str(3, 3)
    x[0][0] = 1
    print(x)
    array = np.array([1, 2, 3, 4], dtype=object)
    array[0] = [1, 2, 3]
    print(AnvnUtils.flatten_list(array))
    x = [1, 2, 3]
    print(AnvnUtils.delete_first(x))
    print(x)