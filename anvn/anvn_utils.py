import copy

class AnvnUtils:
    
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
            ds.append(copy.deepcopy(d))
        return tuple(ds)
    
    @staticmethod
    def range_str(*d):
        return [str(i) for i in range(*d)]

    @staticmethod
    def n_range_str(n, *d):
        ns = []
        for _ in range(n):
            ns.append(AnvnUtils.range_str(*d))
        return ns 


if __name__ == '__main__':
    print(AnvnUtils.deepcopy([1], [2], [3]))
    print(AnvnUtils.range_str(10))
    print(AnvnUtils.range_str(1, 10))
    print(AnvnUtils.range_str(10, 1, -1))
    x = AnvnUtils.n_range_str(3, 3)
    x[0][0] = 1
    print(x)