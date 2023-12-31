# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['kstep', 'kuut']

# %% ../nbs/00_core.ipynb 3
from typing import (NamedTuple, Optional, Union, List)
from dataclasses import dataclass
from tqdm.auto import tqdm

# %% ../nbs/00_core.ipynb 5
@dataclass
class kstep:
    """
    A dataclass to store step information.

    Parameters
    ----------
    num : int
        The main number of the step.
        
    sub : Optional[int], default=None
        The sub number of the step, if it exists.

    val : Optional[int], default=1
        The value of the step.
        
    desc : Optional[str], default=None
        A description for the step.

    Attributes
    ----------
    num : int
        The main number of the step.

    sub : Optional[int]
        The sub number of the step, if it exists.

    val : Optional[int]
        The value of the step.

    desc : Optional[str]
        A description for the step.

    Methods
    -------
    has_sub() -> bool:
        Check if the step has a substep.

    is_sub(other:Union[int, 'kstep']) -> bool:
        Check if the step is a substep of another step.

    __tuple__() -> Tuple[int, int, int, str]:
        Return a tuple representation of the step.

    __hash__() -> int:
        Return a hash of the step.

    __iter__():
        Return an iterator for the step.

    __len__() -> int:
        Return the length of the step.

    __getitem__(key: Union[int, str]) -> Union[int, str]:
        Get an item from the step.

    __eq__(other: Any) -> bool:
        Check if the step is equal to another step.

    __lt__(other: 'kstep') -> bool:
        Check if the step is less than another step.

    __gt__(other: 'kstep') -> bool:
        Check if the step is greater than another step.
    """
    num: int    
    sub: Optional[int] = None     
    val: Optional[int] = 1
    desc: Optional[str] = None

    @property
    def has_sub(self) -> bool:
        return self.sub is not None

    def is_sub(self, other: Union[int, 'kstep']) -> bool:
        return self.has_sub and self.num == other.num and (self.sub or -1) <= (other.sub or -1)

    def __tuple__(self):
        return (self.num, self.sub, self.val, self.desc)
    
    def __hash__(self):
        return hash(self.__tuple__())

    def __iter__(self):
        return iter(self.__tuple__())

    def __len__(self):
        return len(self.__dict__)

    def __getitem__(self, key: Union[int, str]):
        if isinstance(key, int):
            str_idx = list(kstep.__annotations__)[key]
            return self[str_idx]

        elif isinstance(key, slice):
            return list(self)[key]
            
        return self.__dict__[key]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.desc == other

        elif isinstance(other, tuple):
            return kstep(*self[:len(other)]) == kstep(*other)

        elif isinstance(other, kstep):
            return self.__tuple__() == other.__tuple__()

        elif isinstance(other, list):
            return self == tuple(other)

        elif isinstance(other, int):
            return self == tuple((other,))

        return super().__eq__(other)
    
    def __lt__(self, other):
        return self.__tuple__() < other.__tuple__()
    
    def __gt__(self, other):
        return self.__tuple__() < other.__tuple__()

# %% ../nbs/00_core.ipynb 10
class kuut(tqdm):
    """
    A progress bar class that extends tqdm and operates with kstep instances.

    Parameters
    ----------
    steps : List[kstep]
        The list of steps for the progress bar.
        
    *args : 
        Variable length argument list.

    **kwargs : 
        Arbitrary keyword arguments.

    Attributes
    ----------
    steps : List[kstep]
        The list of steps for the progress bar.

    Methods
    -------
    __enter__():
        Enter the context for the progress bar.

    __exit__(exc_type, exc_val, exc_tb):
        Exit the context for the progress bar.

    __iter__():
        Return an iterator for the progress bar.

    step(num: int, sub: Optional[int]=None):  
        Advance the progress bar by a step.

    does_num_match(step:Union[tuple, kstep], num:int) -> bool:
        Check if a step number matches a given number.

    does_sub_match(step:Union[tuple, kstep], sub:int) -> bool:
        Check if a step sub number matches a given sub number.

    does_step_match(step:Union[tuple, kstep], num:int, sub:int) -> bool:
        Check if a step matches a given main and sub number.

    get_step(num:int, sub:Optional[int]=None) -> Optional[kstep]:
        Get a step from the progress bar.

    does_step_exist(num: int, sub: Optional[int]=None) -> bool:
        Check if a step exists in the progress bar.

    is_step(num:int, sub:Optional[int]=None) -> bool:
        Alias for does_step_exist.

    get_step_subs(num:int) -> List[int]:
        Get the sub steps for a main step.
        
    pbar_total() -> int:
        Get the total progress bar value.

    step_nums() -> List[int]:
        Get the main step numbers.

    num_main_steps():
        Get the number of main steps.

    step_subs():
        Get all sub steps for all main steps.

    num_all_steps():
        Get the total number of steps (main and sub).

    calc_pbar_val(num:int, sub:Optional[int]=None) -> int:
        Calculate the progress bar value.
    """
    def __new__(cls, *args, **kwargs):
        try:
            cls._instances = tqdm._instances
        except AttributeError:
            pass

        instance = super().__new__(cls, *args, **kwargs)

        tqdm._instances = cls._instances
        return instance
     
    def __init__(self, steps: List[kstep], *args, **kwargs):
        self.steps = steps        
        kwargs['total'] = self.pbar_total        
        super().__init__(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __iter__(self):
        last_num = self.steps[0].num
        last_desc = self.steps[0].desc

        for step in self.steps:
            if last_num < step.num:
                last_num = step.num
                last_desc = step.desc

            desc = step.desc
            if desc is None:
                desc = last_desc if last_num == step.num else f"({step.num}, {step.sub})"

            # self.step(step.num, step.sub)            
            yield kstep(step.num, step.sub, step.val, desc)

    def step(self, num: int, sub: Optional[int] = None):  
        # self.display()      
        self.n = self.calc_pbar_val(num, sub)
        self.refresh()
        # self.container
        return 
    
    def does_num_match(self, step: Union[tuple, kstep], num: int) -> bool:
        return kstep(*step).num == num
    
    def does_sub_match(self, step: Union[tuple, kstep], sub: int) -> bool:
        return kstep(*step).sub == sub
    
    def does_step_match(self, step: Union[tuple, kstep], num: int, sub: int) -> bool:
        return kstep(*step) == (num, sub)

    def get_step(self, num: int, sub: Optional[int] = None) -> Optional[kstep]:
        return next((step for step in self.steps if kstep(*step) == (num, sub)), None)

    def does_step_exist(self, num: int, sub: Optional[int] = None) -> bool:
        return self.get_step(num, sub) is not None
    
    # NOTE: alias for does_step_exist
    def is_step(self, num: int, sub: Optional[int] = None) -> bool:
        return self.does_step_exist(num, sub)

    def get_step_subs(self, num: int) -> List[int]:
        return sorted(list(set(filter(lambda s: s.is_sub(num), self.steps))))

    @property
    def pbar_total(self) -> int:
        return sum([step.val for step in self.steps])

    @property
    def step_nums(self) -> List[int]:
        return sorted(list(set([step.num for step in self.steps])))

    @property
    def num_main_steps(self):
        # total number of steps
        return len(self.step_nums)

    @property
    def step_subs(self):
        return {num: self.get_step_subs(num) for num in self.step_nums}
    
    @property
    def num_all_steps(self):
        total = 0
        for _, subs in self.step_subs.items():
            total += 1 + len(subs)
        return total

    
    def _check_sub(self, num: int, sub: Optional[int] = None) -> Optional[int]:
        # NOTE: no substep, so use main step instead
        exists_q = self.is_step(num, sub)
        if not exists_q and sub is not None:
            sub = None
        return sub

    def _check_num(self, num: int) -> Optional[int]:
        if num in self.step_nums:
            return num            
        # NOTE: not a main step, so figure out if user means 100%
        is_above_any = num > self.num_all_steps
        is_above_main = num > self.num_main_steps
        is_above_step = num > max(self.step_nums)

        if is_above_any or is_above_main or is_above_step:        
            return float('inf')
        return None

    def calc_pbar_val(self, num: int, sub: Optional[int] = None) -> int:        
        total = 0

        num = self._check_num(num)
        sub = self._check_sub(num, sub)

        if num is None:
            return total

        if num is float('inf'):
            return self.pbar_total
        
        for step in self.steps:  
            if step.num < num:
                total += step.val
                continue

            elif step.num > num:
                break

            # NOTE: step.num == num
            # kstep(*step).is_sub((num, sub))
            if sub is None:
                total += step.val
                continue

            elif step.sub > sub:                
                break

            else:
                total += step.val

        return total
