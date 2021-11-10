from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec

name = 'EXTRACTSegmentation'
ns_path = name + ".namespace.yaml"
ext_source = name + ".extensions.yaml"

ns_builder = NWBNamespaceBuilder(doc='NWB:N Extension for storage of EXTRACT parameters and output',
                                     name='ndx-extract',
                                     version='0.1.0'
                                )

ns_builder.include_type('ImageSegmentation', namespace='core')

configs = NWBGroupSpec(
    doc='EXTRACT configuration parameters',
    neurodata_type_def='EXTRACTSegmentation',
    neurodata_type_inc='ImageSegmentation',
)
configs.add_attribute(
    name='preprocess',
    doc='Boolean indicating data preprocessing before main EXTRACT',
    dtype='bool'
)
configs.add_attribute(
    name='downsample_time_by',
    doc='time downsampling factor. If set to auto downsampling factor based on avg cell radius and \
    avg calcium event time constant.',
    dtype='text'
)
configs.add_attribute(
    name='downsample_space_by',
    doc='spatial downsampling factor. If set to auto downsampling factor based on avg cell radius and \
    avg calcium event time constant.',
    dtype='text'
)
configs.add_attribute(
    name='smoothing_ratio_x2y',
    doc='If the movie contains mainly objects that are elongated in one dimension \
    (e.g. dendrites), this parameter is useful for more smoothing in either x or y dimension.',
    dtype='float'
)

#keep adding more

ns_builder.add_spec(ext_source, configs)
ns_builder.export(ns_path)