.. _sec-EXTRACTSegmentation-src:

EXTRACTSegmentation
^^^^^^^^^^^^^^^^^^^

**Extends:** :ref:`ImageSegmentation <sec-ImageSegmentation>`

**Description:** see :numref:`sec-EXTRACTSegmentation`

**YAML Specification:**

.. code-block:: yaml
    :linenos:

    attributes:
    - doc: Boolean flag indicating data preprocessing before main EXTRACT function
      dtype: bool
      name: preprocess
    - doc: Boolean flag. Find and fix spatial slices that are occasionally zero due to
        frame registration during preprocessing.
      dtype: bool
      name: fix_zero_FOV_strips
    - doc: Boolean flag determining whether outlier pixels in the movie should be replaced
        with their neighborhood median.
      dtype: bool
      name: medfilt_outlier_pixels
    - doc: Boolean flag. Skip Df/F calculation in preprocessing.
      dtype: bool
      name: skip_dff
    - doc: Baseline quantile for Df/F calculation in preprocessing.
      dtype: float32
      name: baseline_quantile
    - doc: Boolean flag. Skip highpass filtering in preprocessing.
      dtype: bool
      name: skip_highpass
    - doc: 'Cutoff determining the strength of butterworth spatial filtering of the movie.
        Values defined relative to the average cell radius. '
      dtype: float32
      name: spatial_highpass_cutoff
    - doc: Boolean flag that determines whether to apply temporal wavelet denoising.
      dtype: bool
      name: temporal_denoising
    - doc: Boolean flag that determines whether to subtract the (spatial) background (largest
        spatiotemporal mode of the movie matrix).
      dtype: bool
      name: remove_background
    - doc: Radius estimate for an average cell in the movie.
      dtype: float32
      name: avg_cell_radius
    - doc: Number of movie partitions in x dimension.
      dtype: uint
      name: num_partitions_x
      required: false
    - doc: Number of movie partitions in y dimension.
      dtype: uint
      name: num_partitions_y
      required: false
    - doc: Raw or non-negative output traces
      dtype: text
      name: trace_output_option
    - doc: Boolean flag, set it to true if dendrites exist in the movie & are desired
        in the output.
      dtype: bool
      name: dendrite_aware
    - doc: Boolean flag. For microendoscopic movies, set it to true for automatically
        cropping out the region outside the circular imaging region.
      dtype: bool
      name: crop_circular
    - doc: Boolean flag. If set to true, then the output cell images will be saved as
        sparse arrays
      dtype: bool
      name: use_sparse_arrays
    - doc: Boolean flag. If set to true, then the output will not include bad components
        that were found but then eliminated
      dtype: bool
      name: compact_output
    - doc: Boolean flag indicating internal hyperparameter tuning.
      dtype: bool
      name: hyperparameter_tuning_flag
    - doc: For movies processed in multiple partitions, this flag controls duplicate removal
        in the overlap regions.
      dtype: bool
      name: remove_duplicate_cells
    - doc: Maximum number of alternating estimation iterations.
      dtype: uint
      name: max_iter
    - doc: Minimum peak SNR value for an object to be considered as a cell.
      dtype: float32
      name: cellfind_min_snr
    - doc: Maximum number of cell candidate initialization during cell finding step.
      dtype: int
      name: cellfind_max_steps
    - doc: Kappa will be set to this times the noise std for the component-wise EXTRACT
        during initialization.
      dtype: float32
      name: cellfind_kappa_std_ratio
    - doc: Type of the spatial smoothing filter used for cell finding.
      dtype: text
      name: cellfind_filter_type
    - doc: During cell finding, objects with an area < cellfind_numpix_threshold are discarded.
      dtype: float32
      name: cellfind_numpix_threshold
    - doc: Radius of moving average filter in the case when cellfind_filter_type = moveavg
        (moving average)
      dtype: float32
      name: moving_radius
    - doc: Boolean flag. If true, then during cell finding, each cell is initialized with
        a gaussian shape prior to robust estimation. If false, then initialization is
        done with a correlation image (preferred for movies with dendrites).
      dtype: bool
      name: init_with_gaussian
    - doc: Threshold for ratio of pixel compared to most bright region in FOV. Used to
        determine when to stop cell finding process.
      dtype: float32
      name: high2low_brightness_ratio
    - doc: Kappa will be set to this times the noise std during the cell refinement process.
        Cell refinement parameter.
      dtype: float32
      name: kappa_std_ratio
    - doc: Through alternating estimation, cells that have higher trace correlation than
        T_dup_corr_thresh are eliminated. Cell refinement parameter.
      dtype: float32
      name: T_dup_corr_thresh
    - doc: Through alternating estimation, cells that have higher image correlation than
        S_dup_corr_thresh are eliminated. Cell refinement parameter.
      dtype: float32
      name: S_dup_corr_thresh
    - doc: Threshold for temporal corruption index. Traces above this threshold are eliminated
        duirng alternating minimization routine. Cell refinement parameter.
      dtype: float32
      name: temporal_corrupt_thresh
    - doc: Threshold for spatial corruption index. Images above this threshold are eliminated
        duirng alternating minimization routine. Cell refinement parameter.
      dtype: float32
      name: spatial_corrupt_thresh
    - doc: Threshold for temporal SNR. Cells with temporal SNR below this value will be
        eliminated. Cell refinement parameter.
      dtype: float32
      name: T_min_snr
    - doc: Lower size limit for found cells. Cell refinement parameter.
      dtype: float32
      name: size_lower_limit
    - doc: Lower size limit for found cells. Cell refinement parameter.
      dtype: float32
      name: size_upper_limit
    - doc: Upper limit of eccentricity for found cells. Cell refinement parameter.
      dtype: float32
      name: eccent_thresh
    - doc: Lower limit of spatiotemporal activity index. Cell refinement parameter.
      dtype: float32
      name: low_ST_index_thresh
    - doc: Upper limit limit of spatiotemporal activity index. Cell refinement parameter.
      dtype: float32
      name: high_ST_index_thresh
    - doc: Lower limit of spatiotemporal corelation. Cell refinement parameter.
      dtype: float32
      name: low_ST_corr_thresh
    - doc: Confidence threhsold for found cells. Cell refinement parameter.
      dtype: float32
      name: confidence_thresh
    - doc: Time downsampling factor. If set to auto downsampling factor based on avg cell
        radius and avg calcium event time constant.
      dtype: text
      name: downsample_time_by
    - doc: Minimum event tau after downsampling. Used when downsample_time_by = auto
      dtype: float32
      name: min_tau_after_downsampling
    - doc: Spatial downsampling factor. If set to auto downsampling factor based on avg
        cell radius and avg calcium event time constant.
      dtype: text
      name: downsample_space_by
    - doc: Minimum avg radius after downsampling. Used when downsample_space_by = auto.
      dtype: float32
      name: min_radius_after_downsampling
    - doc: Boolean flag. When set to true, images are re-estimated from full movie at
        the end. When false, images are upsampled by interpolation.
      dtype: bool
      name: reestimate_S_if_downsampled
    - doc: Boolean flag. When set to true, traces are re-estimated from full movie at
        the end. When false, traces are upsampled by interpolation.
      dtype: bool
      name: reestimate_T_if_downsampled
    - doc: Boolean flag. If true, then during cell finding, the robust esimation loss
        will adaptively set its robustness parameter
      dtype: bool
      name: adaptive_kappa
    - doc: If the movie contains mainly objects that are elongated in one dimension (e.g.
        dendrites), this parameter is useful for more smoothing in either x or y dimension.
      dtype: float32
      name: smoothing_ratio_x2y
    - doc: 'Cutoff determining the strength of butterworth spatial filtering of the movie.
        Values defined relative to the average cell radius. '
      dtype: float32
      name: spatial_lowpass_cutoff
    - doc: Boolean flag indicating whether calculated traces are smoothed using median
        filtering.
      dtype: bool
      name: smooth_T
    - doc: Boolean flag indicating whether calculated images are smoothed using a 2-D
        Gaussian filter.
      dtype: bool
      name: smooth_S
    - doc: Strength of l1 regularization penalty to be applied when estimating the temporal
        components.
      dtype: float32
      name: l1_penalty_factor
    - doc: Maximum number of iterations for S estimation steps
      dtype: uint
      name: max_iter_S
    - doc: Maximum number of iterations for T estimation steps
      dtype: uint
      name: max_iter_T
    - doc: If the 1-step relative change in the objective within each T and S optimization
        is less than this, the respective optimization is terminated.
      dtype: float32
      name: TOL_sub
    - doc: ' If the relative change in the main objective function between 2 consecutive
        alternating minimization steps is less than this, cell extraction is terminated.'
      dtype: float32
      name: TOL_main
    - doc: Lower SNR threshold for found traces.
      dtype: float32
      name: T_lower_snr_threshold
    - doc: Boolean flag. Save all spatial and temporal components found
      dtype: bool
      name: save_all_found
    datasets:
    - dims:
      - heightxwidth
      - num_cells
      doc: Cell images provided to algorithm as the initial set of cells, skipping its
        native initialization
      dtype: double
      name: S_init
      quantity: '?'
      shape:
      - null
      - null
    - dims:
      - num_cells
      - timepoints
      doc: Cell traces provided to algorithm as the initial set of traces, skipping its
        native initialization
      dtype: double
      name: T_init
      quantity: '?'
      shape:
      - null
      - null
    - dims:
      - height
      - width
      doc: Movie mask.
      dtype: double
      name: movie_mask
      quantity: '?'
      shape:
      - null
      - null
    doc: EXTRACT configuration parameters
    neurodata_type_def: EXTRACTSegmentation
    neurodata_type_inc: ImageSegmentation


