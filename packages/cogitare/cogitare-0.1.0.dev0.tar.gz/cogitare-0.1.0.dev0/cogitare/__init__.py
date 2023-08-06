import torch
import random
import numpy as np
from cogitare.core import PluginInterface
from cogitare.core import Model
from cogitare.core import SequentialModel


__all__ = ['Model', 'SequentialModel', 'PluginInterface']
__version__ = '0.1.0dev'


def seed(value):
    torch.manual_seed(value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(value)
    random.seed(value)
    np.random.seed(value)
