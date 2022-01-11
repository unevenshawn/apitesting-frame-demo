from api import yamlUtil


class Inst:
    def tt(self):
        return "this is data from Inst::tt"

    def read_extract_data(self, param):
        return yamlUtil.read_extract_yaml_by_keys(param)
