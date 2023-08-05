import tensorflow as tf
import numpy as np
from ..utils.general import device_name
from .base import Model
from ..graph import Graph, NodeKeys


class MultiGPUSplitor(Model):
    """
    A Helper class to create
    """

    def __init__(self, name='gpu_splitor', nb_gpu=2):
        super().__init__(name, nb_gpu=nb_gpu)

    @classmethod
    def _default_config(cls):
        result = dict()
        result.update(super()._default_config())
        result.update({
            'lazy_create': True,
            'register_inputs': False,
            'register_outputs': False,
            'format': 'split'
        })
        return result

    def _kernel(self, feeds):
        from dxpy.collections.dicts import swap_dict_hierarchy
        result = {k: self._slice_tensor_for_gpu(feeds[k]) for k in feeds}
        if self.param('format') == 'name':
            return result
        else:
            return swap_dict_hierarchy(result)

    def _get_shape_split(self, shape):
        if isinstance(shape, tf.TensorShape):
            shape_gpu = shape.as_list()
        else:
            shape_gpu = list(shape)
        if shape_gpu[0] is None:
            raise TypeError("Batch size can not be None for MultiGPUSplitor.")
        shape_gpu[0] = shape_gpu[0] // self.param('nb_gpu')
        return shape_gpu

    def _slice_tensor_for_gpu(self, tensor_input):
        result = dict()
        shape_gpu = self._get_shape_split(tensor_input.shape)
        with tf.name_scope(self._get_tensor_name(tensor_input.name)):
            for id_slice in range(self.param('nb_gpu')):
                with tf.device(device_name('gpu', id_slice)):
                    slice_start = [id_slice * shape_gpu[0]] + \
                        [0] * (len(shape_gpu) - 1)
                    name = 'part_{}'.format(id_slice)
                    result[name] = tf.slice(tensor_input, slice_start,
                                            shape_gpu, name=name)
        if len(result) == 0:
            return tensor_input
        return result

    def part_names(self):
        return ['part_{}'.format(id_slice) for id_slice in range(self.param('nb_gpu'))]

    def _get_tensor_name(self, name):
        prefix, idt = name.split(':')
        idt = int(idt)
        if idt == 0:
            return prefix
        else:
            return '{}_{}'.format(prefix, idt)


class PlaceHolder(Graph):
    """
    Placeholder for graph. Note this placeholder can be used to construct logic
    graph, thus may not create in tensorflow.
    """

    def __init__(self, shape_or_tensor, dtype=None, name='placeholder', restrict=False):
        dtype = self._unified_dtype(dtype)
        if not restrict and isinstance(shape_or_tensor, tf.Tensor):
            shape_or_tensor = shape_or_tensor.shape
        if isinstance(shape_or_tensor, tf.TensorShape):
            shape_or_tensor = shape_or_tensor.as_list()
        super().__init__(name, shape=shape_or_tensor, dtype=dtype)

    @classmethod
    def _default_config(cls):
        from dxpy.collections.dicts import combine_dicts
        return combine_dicts({'dtype': tf.float32}, super()._default_config())

    @staticmethod
    def _unified_dtype(dtype):
        if isinstance(dtype, type(tf.float32)):
            return dtype
        type_desc = {
            tf.float32: ['FLOAT', 'FLOAT32', 'TF.FLOAT32'],
            tf.int64: ['INT', 'INT64', 'TF.INT64']
        }
        if isinstance(dtype, str):
            for k in type_desc:
                if dtype.upper() in type_desc[k]:
                    return k
            raise ValueError("Unknown dtype {}.".format(dtype))

    @property
    def shape(self):
        return self.param('shape')

    @property
    def dtype(self):
        return self.param('dtype')

    def as_tensor(self):
        if not NodeKeys.MAIN in self.nodes:
            self.register_main_node(tf.placeholder(self.dtype,
                                                   self.shape,
                                                   self.basename))
        return self.nodes[NodeKeys.MAIN]


class ShapeEnsurer(Model):
    """
    Used for assert on shapes or provide information for None dimensions.
    """

    def __init__(self, input_tensor, shape=None, *, batch_size=None, name='shape_ensurer'):
        super().__init__(name, inputs={NodeKeys.INPUT: input_tensor},
                         shape=shape, batch_size=batch_size, simple_output=True)

    def _kernel(self, feeds):
        with tf.name_scope('shape_ensurer'):
            if self.param('shape', raise_key_error=False) is None:
                shape = self.tensor(NodeKeys.INPUT).shape.as_list()
            else:
                shape = self.param('shape')
            return tf.reshape(feeds[NodeKeys.INPUT], self.param('shape'))


from typing import TypeVar, Tuple, List


def to_tensor(input_: TypeVar('TensorConvertable', tf.Tensor, np.ndarray, Graph), name: str="to_tensor") -> tf.Tensor:
    if isinstance(input_, Graph):
        return input_.as_tensor()
    if isinstance(input_, np.ndarray):
        with tf.name_scope(name):
            return tf.constant(input_, input_.dtype)
    if isinstance(input_, tf.Tensor):
        return input_


def to_tensor_with_shape(input_, shape: Tuple[int], *, batch_size: int=None, name: str='to_tensor_with_shape') -> tf.Tensor:
    with tf.name_scope(name):
        input_ = to_tensor(input_)
        if shape is None and batch_size is not None:
            shape = shape_as_list(input_)
            shape[0] = batch_size
        return tf.reshape(input_, shape)


def shape_as_list(input_) -> List[int]:
    if isinstance(input_, (tf.Tensor, tf.Variable)):
        return list(input_.shape.as_list())
    if isinstance(input_, np.ndarray):
        return list(input_.shape)
    if isinstance(input_, (tuple, list)):
        return list(input_)


def ensure_tensor(input_):
    import warnings
    warnings.warn(DeprecationWarning())
    if isinstance(input_, Graph):
        return input_.as_tensor()
    if isinstance(input_, np.ndarray):
        return tf.constant(input_, input_.dtype)
    if isinstance(input_, tf.Tensor):
        return input_


def ensure_tensor_with_shape(input_, shape=None, *, batch_size=None, name='shape_ensurer'):
    import warnings
    warnings.warn(DeprecationWarning())
    with tf.name_scope(name):
        input_ = ensure_tensor(input_)
        if shape is None and batch_size is not None:
            shape = shape_as_list(input_)
            shape[0] = batch_size
        return tf.reshape(input_, shape)
