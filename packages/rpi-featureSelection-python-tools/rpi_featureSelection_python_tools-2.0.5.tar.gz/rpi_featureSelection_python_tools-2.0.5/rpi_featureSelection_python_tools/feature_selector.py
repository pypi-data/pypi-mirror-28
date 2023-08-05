import os, sys
# from typing import NamedTuple, Union, List, Sequence, Any, Dict
import typing
import scipy.io
import numpy as np

# from d3m_metadata.container.numpy import ndarray
# from d3m_metadata import hyperparams, params
from d3m_metadata import container, hyperparams, metadata as metadata_module, params, utils
from primitive_interfaces.supervised_learning import SupervisedLearnerPrimitiveBase
# from . import __version__


import rpi_feature_selection_toolbox


Inputs = container.ndarray
Outputs = container.ndarray

__all__ = ('IPCMBplus_Selector',)

# class Params(params.Params):
#     n_features: int
#     feature_index: ndarray


class Hyperparams(hyperparams.Hyperparams):
    n_bins = hyperparams.UniformInt(
                            lower=5,
                            upper=15,
                            default=10,
                            semantic_types=['n_bins'],
                            description='The maximum number of bins used for continuous variables.'
                            )


class IPCMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    # __author__ = "RPI TA1 Performers"
    # __metadata__ = {
    #     "team": "RPI DARPA D3M TA1 team",
    #     "common_name": "Structured Feature Selection",
    #     "algorithm_type": ["Dimensionality Reduction"],
    #     "task_type": ["Feature Selection"],
    #     "compute_resources": {
    #         "sample_size": [],
    #         "sample_unit": [],
    #         "disk_per_node": [],
    #         "expected_running_time": [],
    #         "gpus_per_node": [],
    #         "cores_per_node": [],
    #         "mem_per_gpu": [],
    #         "mem_per_node": [],
    #         "num_nodes": [],
    #     },
    #     "learning_type": ["Supervised Learning"],
    #     "handles_regression": False,
    #     "handles_classification": False,
    #     "handles_multiclass": False,
    #     "handles_multilabel": False,
    # }

    metadata = metadata_module.PrimitiveMetadata({
        'id': '69845479-0b61-3578-b382-972cd0e61d69',
        'version': '2.0.5',
        'name': 'IPCMB feature selector',
        'keywords': 'rpi primitives',
        'source': {
            'name': 'RPI',
            'uris': [
                'rpi_featureSelection_python_tools',
                'rpi_feature_selection_toolbox'
            ],
        },
        'installation':[{
            'type': 'PIP',
            'package_uri': 'rpi_featureSelection_python_tools'
        }],
        'python_path': 'd3m.primitives.rpi_featureSelection_python_tools.IPCMBplus_Selector',
        'algorithm_types': 'MINIMUM_REDUNDANCY_FEATURE_SELECTION',
        'primitive_family': 'FEATURE_SELECTION',
        'preconditions': [
            "NO_CATEGORICAL_VALUES",
            "NO_MISSING_VALUES"
        ]
    })




    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)
        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False

    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.IPCMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass


'''
class JMIplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.JMIplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class STMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.STMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class aSTMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.aSTMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class sSTMBplus_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.sSTMBplus()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class pSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.pSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class F_STMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_STMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class F_aSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_aSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class F_sSTMB_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.F_sSTMB()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass




class JMIp_Selector(SupervisedLearnerPrimitiveBase[Inputs, Outputs, Params, Hyperparams]):
    __author__ = "RPI TA1 Performers"
    __metadata__ = {
        "team": "RPI DARPA D3M TA1 team",
        "common_name": "Structured Feature Selection",
        "algorithm_type": ["Dimensionality Reduction"],
        "task_type": ["Feature Selection"],
        "compute_resources": {
            "sample_size": [],
            "sample_unit": [],
            "disk_per_node": [],
            "expected_running_time": [],
            "gpus_per_node": [],
            "cores_per_node": [],
            "mem_per_gpu": [],
            "mem_per_node": [],
            "num_nodes": [],
        },
        "learning_type": ["Supervised Learning"],
        "handles_regression": False,
        "handles_classification": False,
        "handles_multiclass": False,
        "handles_multilabel": False,
    }


    def __init__(self, *, hyperparams: Hyperparams, random_seed: int = 0, docker_containers: Dict[str, str] = None) -> None:
        super().__init__(hyperparams=hyperparams, random_seed=random_seed)

        self.is_feature_selection = True
        self.index = None
        self.training_inputs = None
        self.training_outputs = None
        self.fitted = False


    def set_training_data(self, inputs: Inputs, outputs: Outputs) -> None:
        self.training_inputs = inputs
        self.training_outputs = outputs
        self.fitted = False


    def fit(self) -> None:
        if self.fitted:
            return True

        if self.training_inputs.any() == None or self.training_outputs.any() == None:
            raise ValueError('Missing training data, or missing values exist.')

        scipy.io.savemat('rpi_data.mat', mdict={'traindata': self.training_inputs, 'trainlabel': self.training_outputs})

        a = rpi_feature_selection_toolbox.initialize()
        index = np.reshape(np.array(a.JMIp()), [-1, ])

        self.index = (index - 1).astype(int)
        self.fitted = True

        os.remove('rpi_data.mat')

        return True


    def produce(self, inputs: Inputs) -> Outputs:  # inputs: m x n numpy array
        if self.fitted:
            return inputs[:, self.index]
        else:
            raise ValueError('Model should be fitted first.')


    def get_params(self) -> None:
        pass


    def set_params(self):
        pass



'''














