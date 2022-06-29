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