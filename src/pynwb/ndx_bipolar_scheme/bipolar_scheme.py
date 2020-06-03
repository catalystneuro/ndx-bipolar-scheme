from pynwb import register_class, get_class
from pynwb.file import DynamicTable
from hdmf.utils import docval, call_docval_func, get_docval


@register_class('BipolarSchemeTable', 'ndx-bipolar-scheme')
class BipolarSchemeTable(DynamicTable):
    """
    Table for storing bipolar scheme data
    """

    __columns__ = (
        {'name': 'anodes', 'description': 'references the electrodes table', 'required': True, 'index': True, 
         'table': True},
        {'name': 'cathodes', 'description': 'references the electrodes table', 'required': True, 'index': True,
         'table': True}
    )

    @docval(dict(name='name', type=str, doc='name of this BipolarSchemeTable',
                 default='BipolarSchemeTable'),  # required
            dict(name='description', type=str, doc='Description of this DynamicTableRegion',
                 default='references the electrodes table'),
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'))
    def __init__(self, **kwargs):
        call_docval_func(super(BipolarSchemeTable, self).__init__, kwargs)


EcephysExt = get_class('EcephysExt', 'ndx-bipolar-scheme')

