# -*- coding: utf-8 -*-
import os.path
from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBDatasetSpec,
    NWBAttributeSpec,
)


def main():
    ns_builder = NWBNamespaceBuilder(
        doc="NWB Extension for storage of EXTRACT parameters and output",
        name="ndx-extract",
        version="0.2.0",
        author=list(map(str.strip, "Cesar Echavarria, Szonja Weigl".split(","))),
        contact=list(map(str.strip, "cesar.echavarria@catalystneuro.com, szonja.weigl@catalystneuro.com".split(","))),
    )

    ns_builder.include_type("ImageSegmentation", namespace="core")

    ExtractSegmentationExtension = NWBGroupSpec(
        doc="EXTRACT configuration parameters",
        neurodata_type_def="EXTRACTSegmentation",
        neurodata_type_inc="ImageSegmentation",
        attributes=[
            # preprocessing parameters
            NWBAttributeSpec(
                name="preprocess",
                doc="Boolean flag indicating data preprocessing before main EXTRACT function",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="pre_mask_on",
                doc="Boolean flag indicating whether to use an image mask for preprocessing.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="pre_mask_radius",
                doc="The radius of the image mask.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="fix_zero_FOV_strips",
                doc="Boolean flag. Find and fix spatial slices that are occasionally zero due to "
                "frame registration during preprocessing.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="medfilt_outlier_pixels",
                doc="Boolean flag determining whether outlier pixels in the movie should be replaced with their "
                "neighborhood median.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="skip_dff",
                doc="Boolean flag indicating whether to skip Df/F calculation in preprocessing.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="second_df",
                doc="No description available.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="skip_highpass",
                doc="Boolean flag. Skip highpass filtering in preprocessing.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="spatial_highpass_cutoff",
                doc="Cutoff determining the strength of butterworth spatial filtering of the movie. "
                "Values defined relative to the average cell radius. ",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="temporal_denoising",
                doc="Boolean flag that determines whether to apply temporal wavelet denoising.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="remove_background",
                doc="Boolean flag that determines whether to subtract the (spatial) background "
                "(largest spatiotemporal mode of the movie matrix).",
                dtype="float64",
            ),
            # general control parameters
            NWBAttributeSpec(
                name="use_default_gpu",
                doc="Boolean flag indicating whether to use the default GPU.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="use_gpu",
                doc="Boolean flag indicating whether to run EXTRACT on GPU."
                    "If False, EXTRACT was run on CPU.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="multi_gpu",
                doc="Boolean flag indicating whether multiple GPUs were used.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="parallel_cpu",
                doc="Boolean flag indicating whether to run EXTRACT on parallel CPU.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="avg_cell_radius",
                doc="Radius estimate for an average cell in the movie.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="avg_event_tau",
                doc="Determines the average event tau.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="avg_yield_threshold",
                doc="Determines the average yield threshold.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="num_partitions_x",
                doc="Number of movie partitions in x dimension.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="num_partitions_y",
                doc="Number of movie partitions in y dimension.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="trace_output_option",
                doc="Raw or non-negative output traces.",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="trace_quantile",
                doc="No description available.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="dendrite_aware",
                doc="Boolean flag, set it to true if dendrites exist in the movie & are desired in the output.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="crop_circular",
                doc="Boolean flag. For microendoscopic movies, set it to true for automatically cropping out "
                "the region outside the circular imaging region.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="use_sparse_arrays",
                doc="Boolean flag. If set to true, then the output cell images will be saved as sparse arrays.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="verbose",
                doc="Indicates the level of verbosity.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="compact_output",
                doc="Boolean flag. If set to true, then the output will not include bad components that were "
                "found but then eliminated.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="hyperparameter_tuning_flag",
                doc="Boolean flag indicating internal hyperparameter tuning.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="remove_duplicate_cells",
                doc="For movies processed in multiple partitions, this flag controls duplicate removal in the "
                "overlap regions.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="max_iter",
                doc="Maximum number of alternating estimation iterations.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="minimal_checks",
                doc="Minimum number of checks that are performed.",
                dtype="float64",
            ),
            # cell finding parameters
            NWBAttributeSpec(
                name="cellfind_min_snr",
                doc="Minimum peak SNR value for an object to be considered as a cell.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="cellfind_max_steps",
                doc="Maximum number of cell candidate initialization during cell finding step.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="cellfind_kappa_std_ratio",
                doc="Kappa will be set to this times the noise std for the component-wise EXTRACT during initialization.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="cellfind_filter_type",
                doc="Type of the spatial smoothing filter used for cell finding.",
                dtype="text",
            ),
            NWBAttributeSpec(
                name="cellfind_numpix_threshold",
                doc="During cell finding, objects with an area < cellfind_numpix_threshold are discarded.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="cellfind_adaptive_kappa",
                doc="Boolean flag. If True, then during cell finding, the robust esimation loss will adaptively "
                    "set its robustness parameter",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="cellfind_spatial_highpass_cutoff",
                doc="Cutoff determining the strength of butterworth spatial filtering of the movie. "
                    "Values defined relative to the average cell radius. ",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="moving_radius",
                doc="Deprecated variable for older EXTRACT file versions. Radius of moving average filter in the case when cellfind_filter_type = moveavg "
                "(moving average)",
                dtype="float32",
                required=False,
            ),
            NWBAttributeSpec(
                name="moving_radius_spatial",
                doc="Radius of moving average filter in the case when cellfind_filter_type = moveavg "
                    "(moving average) for the image.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="moving_radius_temporal",
                doc="Radius of moving average filter in the case when cellfind_filter_type = moveavg "
                    "(moving average) for the traces.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="init_with_gaussian",
                doc="Boolean flag. If True, then during cell finding, each cell is initialized with a gaussian shape "
                "prior to robust estimation. If False, then initialization is done with a "
                "correlation image (preferred for movies with dendrites).",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="high2low_brightness_ratio",
                doc="Threshold for ratio of pixel compared to most bright region in FOV. Used to determine when to "
                "stop cell finding process.",
                dtype="float64",
            ),
            # Visualizations during cell finding
            NWBAttributeSpec(
                name="visualize_cellfinding",
                doc="The visualization setting for cell finding.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="visualize_cellfinding_full_range",
                doc="The visualization setting for cell finding.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="visualize_cellfinding_max",
                doc="The visualization setting for cell finding.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="visualize_cellfinding_min",
                doc="The visualization setting for cell finding.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="visualize_cellfinding_show_bad_cells",
                doc="The visualization setting for cell finding.",
                dtype="float64",
            ),
            # cell refinement parameters
            NWBAttributeSpec(
                name="kappa_std_ratio",
                doc="Kappa will be set to this times the noise std during the cell refinement process. "
                "Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="T_dup_corr_thresh",
                doc="Through alternating estimation, cells that have higher trace correlation than T_dup_corr_thresh "
                "are eliminated. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="T_dup_thresh",
                doc="Threshold for traces. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="S_dup_corr_thresh",
                doc="Through alternating estimation, cells that have higher image correlation than S_dup_corr_thresh "
                "are eliminated. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="S_corr_thresh",
                doc="Image correlation threshold. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="T_corr_thresh",
                doc="Trace correlation threshold. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="temporal_corrupt_thresh",
                doc="Threshold for temporal corruption index. Traces above this threshold are eliminated duirng "
                "alternating minimization routine. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="spatial_corrupt_thresh",
                doc="Threshold for spatial corruption index. Images above this threshold are eliminated duirng "
                "alternating minimization routine. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="T_min_snr",
                doc="Threshold for temporal SNR. Cells with temporal SNR below this value will be eliminated. "
                "Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="size_lower_limit",
                doc="Lower size limit for found cells. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="size_upper_limit",
                doc="Lower size limit for found cells. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="eccent_thresh",
                doc="Upper limit of eccentricity for found cells. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="low_ST_index_thresh",
                doc="Lower limit of spatiotemporal activity index. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="low_cell_area_flag",
                doc="Boolean flag indicating lower limit of cell area.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="high_ST_index_thresh",
                doc="Upper limit limit of spatiotemporal activity index. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="low_ST_corr_thresh",
                doc="Lower limit of spatiotemporal corelation. Cell refinement parameter.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="confidence_thresh",
                doc="Confidence threshold for found cells. Cell refinement parameter.",
                dtype="float64",
            ),
            # other parameters
            NWBAttributeSpec(
                name="downsample_time_by",
                doc="Time downsampling factor. If set to auto downsampling factor based on avg cell radius and "
                "avg calcium event time constant.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="min_tau_after_downsampling",
                doc="Minimum event tau after downsampling. Used when downsample_time_by = auto",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="downsample_space_by",
                doc="Spatial downsampling factor. If set to auto downsampling factor based on avg cell radius and "
                "avg calcium event time constant.",
                dtype="float64",
                required=False,
            ),
            NWBAttributeSpec(
                name="min_radius_after_downsampling",
                doc="Minimum avg radius after downsampling. Used when downsample_space_by = auto.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="reestimate_S_if_downsampled",
                doc="Boolean flag. When set to True, images are re-estimated from full movie at the end. "
                "When False, images are upsampled by interpolation.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="reestimate_T_if_downsampled",
                doc="Boolean flag. When set to True, traces are re-estimated from full movie at the end. "
                "When False, traces are upsampled by interpolation.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="adaptive_kappa",
                doc="Boolean flag. If True, then during cell finding, the robust esimation loss will adaptively "
                "set its robustness parameter",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="arbitrary_mask",
                doc="Boolean flag indicating whether to use an arbitraty mask on the images.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="smoothing_ratio_x2y",
                doc="If the movie contains mainly objects that are elongated in one dimension "
                "(e.g. dendrites), this parameter is useful for more smoothing in either x or y dimension.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="spatial_lowpass_cutoff",
                doc="Cutoff determining the strength of butterworth spatial filtering of the movie. "
                "Values defined relative to the average cell radius. ",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="smooth_T",
                doc="Boolean flag indicating whether calculated traces are smoothed using median filtering.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="smooth_S",
                doc="Boolean flag indicating whether calculated images are smoothed using a 2-D Gaussian filter.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="l1_penalty_factor",
                doc="Strength of l1 regularization penalty to be applied when estimating the temporal components.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="max_iter_S",
                doc="Maximum number of iterations for S estimation steps",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="max_iter_T",
                doc="Maximum number of iterations for T estimation steps",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="TOL_sub",
                doc="If the 1-step relative change in the objective within each T and S optimization is less than this, "
                "the respective optimization is terminated.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="TOL_main",
                doc=" If the relative change in the main objective function between 2 consecutive alternating "
                "minimization steps is less than this, cell extraction is terminated.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="T_lower_snr_threshold",
                doc="Lower SNR threshold for found traces.",
                dtype="float64",
            ),
            NWBAttributeSpec(
                name="save_all_found",
                doc="Boolean flag that determines whether to save all spatial and temporal components found.",
                dtype="bool",
            ),
            NWBAttributeSpec(
                name="plot_loss",
                doc="Boolean flag indicating whether empirical risk was plotted against iterations during alternating estimation.",
                dtype="bool",
            ),
        ],
        datasets=[
            NWBDatasetSpec(
                name="baseline_quantile",
                doc="Baseline quantile for Df/F calculation in preprocessing.",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="S_init",
                doc="Cell images provided to algorithm as the initial set of cells, skipping its native initialization",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="T_init",
                doc="Cell traces provided to algorithm as the initial set of traces, skipping its native initialization",
                shape=(None, None),
                dtype="double",
                dims=("num_cells", "timepoints"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="movie_mask",
                doc="The circular mask to apply for microendoscopic movies during preprocessing.",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="is_pixel_valid",
                doc="No description available",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="num_frames",
                doc="No description available",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="num_iter_stop_quality_checks",
                doc="No description available",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
            NWBDatasetSpec(
                name="pick_gpu",
                doc="No description available",
                shape=(None, None),
                dtype="double",
                dims=("height", "width"),
                quantity="?",
            ),
        ],
    )

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    )
    export_spec(ns_builder, [ExtractSegmentationExtension], output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
