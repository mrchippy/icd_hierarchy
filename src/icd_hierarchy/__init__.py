import pandas as pd

def _title(diag: dict[str,any]) -> str: 
    return f'{diag["code"]} : {diag["desc"]}'

def _icd9_iter(iterable_map):
    it = iter(iterable_map)
    while True:
        try:
            yield next(it)
        except (StopIteration, KeyError):
            break

DIAGS = 'diags'
PARENTS = 'parents'

icd9_packaged_json_filename = 'icd9_cm.json'

class ICD9Visitor:
    def visit(self, icd9_node) -> tuple[bool, str, any]:
        raise NotImplemented()
    
class ValueVisitor(ICD9Visitor):
    def __init__(self, code_value_map: dict[str,int|float]) -> None:
        super().__init__()
        self._values = code_value_map
    
    def visit(self, icd9_node) -> tuple[bool, str, any]:
        code = icd9_node['code']
        code = code.replace('.','')
        value = self._values.get(code, 0)
        return value != 0, 'values', value

class ICD9Hierarchy:
    def __init__(self, visitor: ICD9Visitor=None, filename: str=None):
        self._filename = filename
        self._df = None
        self._visitor = visitor

    def _load_df(self) -> pd.DataFrame:
        df = None
        if self._filename:
            df = pd.read_json(self._filename)
        else:
            from importlib.resources import files
            df = pd.read_json(files('icd_hierarchy').joinpath(icd9_packaged_json_filename))
        return df
    
    def get_df(self):
        if self._df is None:
            self._df = self._load_df()
        return self._df
 
    def _add_diag(self,
                  parent_title: str,
                  children: list[dict[str,any]],
                  out_series: dict[str,list[any]],
                  visitor: ICD9Visitor = None):
        keep_level = False
        for child in _icd9_iter(children):
            value = 0
            title = 'title'
            keep_node = True
            if visitor:
                keep_node, title, value = visitor.visit(child)   
            child_title = _title(child)
            grandchildren = child['children']
            keep_branch = False
            if grandchildren:
                keep_branch = self._add_diag(child_title, grandchildren, out_series, visitor)   
            if keep_node or keep_branch:
                out_series[DIAGS].append(child_title)
                out_series[PARENTS].append(parent_title)
                series = out_series.setdefault(title,[])
                series.append(value)
                keep_level = True
        return keep_level
                

    def get_flattened_df(self) -> pd.DataFrame:
        top_level = self.get_df()
        out_series = {DIAGS:[],PARENTS:[]}
        self._add_diag("", top_level.loc, out_series, self._visitor)
        out_df = pd.DataFrame(out_series)
        return out_df 