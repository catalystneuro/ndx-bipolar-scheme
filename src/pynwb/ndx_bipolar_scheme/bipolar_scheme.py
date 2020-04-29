from hdmf.common import DynamicTable, register_class, register_map
from hdmf.common.io.table import DynamicTableMap
from hdmf.utils import docval, call_docval_func, get_docval


@register_class('BipolarSchemeTable', 'ndx-bipolar-scheme')
class PointCloudTable(DynamicTable):
    """
    Table for storing point cloud data
    """

    __columns__ = (
        {'name': 'anodes', 'description': 'anode electrodes', 'required': True, 'index': True},
        {'name': 'cathods', 'description': 'cathode electrodes', 'required': True, 'index': True}
    )

    @docval(dict(name='name', type=str, doc='name of this BipolarSchemeTable', default='BipolarSchemeTable'),  # required
            dict(name='description', type=str, doc='Description of this TimeIntervals',
                 default="points from a tracking system"),
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'))
    def __init__(self, **kwargs):
        call_docval_func(super(BipolarSchemeTable, self).__init__, kwargs)


@register_map(BipolarSchemeTable)
class PointCloudTableMap(DynamicTableMap):
    pass
