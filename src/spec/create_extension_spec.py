# -*- coding: utf-8 -*-
import os.path
from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBDatasetSpec,
    NWBAttributeSpec
)

def main():
    name = 'ndx-extract'
    ns_path = name + ".namespace.yaml"
    ext_source = name + ".extensions.yaml"

    ns_builder = NWBNamespaceBuilder(
        doc='NWB:N Extension for storage of EXTRACT parameters and output',
        name='ndx-extract',
        version='0.1.1',
        author=list(map(str.strip, 'Cesar Echavarria'.split(','))),
        contact=list(map(str.strip, 'cesar.echavarria@catalystneuro.com'.split(',')))
    )

    ns_builder.include_type('ImageSegmentation', namespace='core')

    configs = NWBGroupSpec(
        doc='EXTRACT configuration parameters',
        neurodata_type_def='EXTRACTSegmentation',
        neurodata_type_inc='ImageSegmentation',
        attributes = [
            # preprocessing parameters
            NWBAttributeSpec(
                name='preprocess',
                doc='int32ean flag indicating data preprocessing before main EXTRACT function',
                dtype='int32'
            ),
            NWBAttributeSpec(
                name = 'fix_zero_FOV_strips',
                doc = 'int32ean flag. Find and fix spatial slices that are occasionally zero due to '\
                'frame registration during preprocessing.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'medfilt_outlier_pixels',
                doc = 'int32ean flag determining whether outlier pixels in the movie should be replaced with their '\
                'neighborhood median.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'skip_dff',
                doc = 'int32ean flag. Skip Df/F calculation in preprocessing.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'baseline_quantile',
                doc = 'Baseline quantile for Df/F calculation in preprocessing.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'skip_highpass',
                doc = 'int32ean flag. Skip highpass filtering in preprocessing.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'spatial_highpass_cutoff',
                doc = 'Cutoff determining the strength of butterworth spatial filtering of the movie. '\
                'Values defined relative to the average cell radius. ',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'temporal_denoising',
                doc = 'int32ean flag that determines whether to apply temporal wavelet denoising.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'remove_background',
                doc = 'int32ean flag that determines whether to subtract the (spatial) background '\
                '(largest spatiotemporal mode of the movie matrix).',
                dtype = 'int32'
            ),
            # general control parameters
            NWBAttributeSpec(
                name = 'avg_cell_radius',
                doc = 'Radius estimate for an average cell in the movie.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'num_partitions_x',
                doc = 'Number of movie partitions in x dimension.',
                dtype = 'uint32',
                required = False
            ),
            NWBAttributeSpec(
                name = 'num_partitions_y',
                doc = 'Number of movie partitions in y dimension.',
                dtype = 'uint32',
                required = False
            ),
            NWBAttributeSpec(
                name = 'trace_output_option',
                doc = 'Raw or non-negative output traces',
                dtype = 'text'
            ),
            NWBAttributeSpec(
                name = 'dendrite_aware',
                doc = 'int32ean flag, set it to true if dendrites exist in the movie & are desired in the output.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'crop_circular',
                doc = 'int32ean flag. For microendoscopic movies, set it to true for automatically cropping out '\
                'the region outside the circular imaging region.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'use_sparse_arrays',
                doc = 'int32ean flag. If set to true, then the output cell images will be saved as sparse arrays',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'compact_output',
                doc = 'int32ean flag. If set to true, then the output will not include bad components that were '\
                'found but then eliminated',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'hyperparameter_tuning_flag',
                doc = 'int32ean flag indicating internal hyperparameter tuning.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'remove_duplicate_cells',
                doc = 'For movies processed in multiple partitions, this flag controls duplicate removal in the '\
                'overlap regions.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'max_iter',
                doc = 'Maximum number of alternating estimation iterations.',
                dtype = 'uint32'
            ),
            #cell finding parameters
            NWBAttributeSpec(
                name = 'cellfind_min_snr',
                doc = 'Minimum peak SNR value for an object to be considered as a cell.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'cellfind_max_steps',
                doc = 'Maximum number of cell candidate initialization during cell finding step.',
                dtype = 'int'
            ),
            NWBAttributeSpec(
                name = 'cellfind_kappa_std_ratio',
                doc = 'Kappa will be set to this times the noise std for the component-wise EXTRACT during initialization.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'cellfind_filter_type',
                doc = 'Type of the spatial smoothing filter used for cell finding.',
                dtype = 'text'
            ),
            NWBAttributeSpec(
                name = 'cellfind_numpix_threshold',
                doc = 'During cell finding, objects with an area < cellfind_numpix_threshold are discarded.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'moving_radius',
                doc = 'Radius of moving average filter in the case when cellfind_filter_type = moveavg '\
                '(moving average)',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'init_with_gaussian',
                doc = 'int32ean flag. If true, then during cell finding, each cell is initialized with a gaussian shape '\
                'prior to robust estimation. If false, then initialization is done with a '\
                'correlation image (preferred for movies with dendrites).',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'high2low_brightness_ratio',
                doc = 'Threshold for ratio of pixel compared to most bright region in FOV. Used to determine when to '\
                'stop cell finding process.',
                dtype = 'float32'
            ),
            # cell refinement parameters
            NWBAttributeSpec(
                name = 'kappa_std_ratio',
                doc = 'Kappa will be set to this times the noise std during the cell refinement process. '\
                'Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'T_dup_corr_thresh',
                doc = 'Through alternating estimation, cells that have higher trace correlation than T_dup_corr_thresh '\
                'are eliminated. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'S_dup_corr_thresh',
                doc = 'Through alternating estimation, cells that have higher image correlation than S_dup_corr_thresh '\
                'are eliminated. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'temporal_corrupt_thresh',
                doc = 'Threshold for temporal corruption index. Traces above this threshold are eliminated duirng '\
                'alternating minimization routine. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'spatial_corrupt_thresh',
                doc = 'Threshold for spatial corruption index. Images above this threshold are eliminated duirng '\
                'alternating minimization routine. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'T_min_snr',
                doc = 'Threshold for temporal SNR. Cells with temporal SNR below this value will be eliminated. '\
                'Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'size_lower_limit',
                doc = 'Lower size limit for found cells. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'size_upper_limit',
                doc = 'Lower size limit for found cells. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'eccent_thresh',
                doc = 'Upper limit of eccentricity for found cells. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'low_ST_index_thresh',
                doc = 'Lower limit of spatiotemporal activity index. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'high_ST_index_thresh',
                doc = 'Upper limit limit of spatiotemporal activity index. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'low_ST_corr_thresh',
                doc = 'Lower limit of spatiotemporal corelation. Cell refinement parameter.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'confidence_thresh',
                doc = 'Confidence threhsold for found cells. Cell refinement parameter.',
                dtype = 'float32'
            ),
            #other parameters
            NWBAttributeSpec(
                name='downsample_time_by',
                doc='Time downsampling factor. If set to auto downsampling factor based on avg cell radius and '\
                'avg calcium event time constant.',
                dtype='float32',
                required = False
            ),
            NWBAttributeSpec(
                name = 'min_tau_after_downsampling',
                doc = 'Minimum event tau after downsampling. Used when downsample_time_by = auto',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name='downsample_space_by',
                doc='Spatial downsampling factor. If set to auto downsampling factor based on avg cell radius and '\
                'avg calcium event time constant.',
                dtype='float32',
                required = False
            ),
            NWBAttributeSpec(
                    name='min_radius_after_downsampling',
                    doc='Minimum avg radius after downsampling. Used when downsample_space_by = auto.',
                    dtype='float32'
            ),
            NWBAttributeSpec(
                name = 'reestimate_S_if_downsampled',
                doc = 'int32ean flag. When set to true, images are re-estimated from full movie at the end. '\
                'When false, images are upsampled by interpolation.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'reestimate_T_if_downsampled',
                doc = 'int32ean flag. When set to true, traces are re-estimated from full movie at the end. '\
                'When false, traces are upsampled by interpolation.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'adaptive_kappa',
                doc = 'int32ean flag. If true, then during cell finding, the robust esimation loss will adaptively '\
                'set its robustness parameter',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name='smoothing_ratio_x2y',
                doc='If the movie contains mainly objects that are elongated in one dimension '\
                '(e.g. dendrites), this parameter is useful for more smoothing in either x or y dimension.',
                dtype='float32'
            ),
            NWBAttributeSpec(
                name = 'spatial_lowpass_cutoff',
                doc = 'Cutoff determining the strength of butterworth spatial filtering of the movie. '\
                'Values defined relative to the average cell radius. ',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'smooth_T',
                doc = 'int32ean flag indicating whether calculated traces are smoothed using median filtering.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'smooth_S',
                doc = 'int32ean flag indicating whether calculated images are smoothed using a 2-D Gaussian filter.',
                dtype = 'int32'
            ),
            NWBAttributeSpec(
                name = 'l1_penalty_factor',
                doc = 'Strength of l1 regularization penalty to be applied when estimating the temporal components.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'max_iter_S',
                doc = 'Maximum number of iterations for S estimation steps',
                dtype = 'uint32'
            ),
            NWBAttributeSpec(
                name = 'max_iter_T',
                doc = 'Maximum number of iterations for T estimation steps',
                dtype = 'uint32'
            ),
            NWBAttributeSpec(
                name = 'TOL_sub',
                doc = 'If the 1-step relative change in the objective within each T and S optimization is less than this, '\
                'the respective optimization is terminated.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'TOL_main',
                doc = ' If the relative change in the main objective function between 2 consecutive alternating '\
                'minimization steps is less than this, cell extraction is terminated.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'T_lower_snr_threshold',
                doc = 'Lower SNR threshold for found traces.',
                dtype = 'float32'
            ),
            NWBAttributeSpec(
                name = 'save_all_found',
                doc = 'int32ean flag. Save all spatial and temporal components found',
                dtype = 'int32'
            ),
        ],
        datasets = [
            NWBDatasetSpec(
                name = 'S_init',
                doc = 'Cell images provided to algorithm as the initial set of cells, skipping its native initialization',
                shape = (None, None),
                dtype = 'double',
                dims = ('heightxwidth','num_cells'),
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'T_init',
                doc = 'Cell traces provided to algorithm as the initial set of traces, skipping its native initialization',
                shape = (None, None),
                dtype = 'double',
                dims = ('num_cells','timepoints'),
                quantity = '?'
            ),
            NWBDatasetSpec(
                name = 'movie_mask',
                doc = 'Movie mask.',
                shape = (None, None),
                dtype = 'double',
                dims = ('height', 'width'),
                quantity = '?'
            ),
        ],
    )


    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, [configs], output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
