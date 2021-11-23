classdef TestInterface < matlab.unittest.TestCase
    properties
        file
    end
    methods (TestMethodSetup)
        function setupMethod(testCase)
            % define NWB file
            testCase.file = NwbFile( ...
                'session_description', 'a test NWB File', ...
                'identifier', 'TEST123', ...
                'session_start_time', '2018-12-02T12:57:27.371444-08:00', ...
                'file_create_date', '2017-04-15T12:00:00.000000-08:00',...
                'timestamps_reference_time', '2018-12-02T12:57:27.371444-08:00' ...
            );
            % define processing module
            ophys_module = types.core.ProcessingModule( ...
                'description', 'test processing module' ...
            );
            testCase.file.processing.set('test_ophys', ophys_module);
            % define segmentation
            img_seg = types.ndx_extract.EXTRACTSegmentation();
            % set segmentation properties
            img_seg.trace_output_option = 'nonneg';
            img_seg.save_all_found = 0;
            img_seg.dendrite_aware = 0;
            img_seg.adaptive_kappa = 0;
            img_seg.use_sparse_arrays = 0;
            img_seg.dendrite_aware = 0;
            img_seg.hyperparameter_tuning_flag = 0;
            img_seg.remove_duplicate_cells = 0;
            img_seg.max_iter = 6;
            img_seg.S_init = rand(100,10);
            img_seg.T_init = rand(100,10);
            img_seg.preprocess = 1;
            img_seg.fix_zero_FOV_strips = 0;
            img_seg.medfilt_outlier_pixels = 0;
            img_seg.skip_dff = 0;
            img_seg.baseline_quantile = .4;
            img_seg.skip_highpass = 0;
            img_seg.spatial_highpass_cutoff = 0;
            img_seg.temporal_denoising = 0;
            img_seg.remove_background = 1;
            img_seg.cellfind_filter_type = 'butter';
            img_seg.spatial_lowpass_cutoff = 2;
            img_seg.moving_radius = 3;
            img_seg.cellfind_min_snr = 1;
            img_seg.cellfind_max_steps = 1000;
            img_seg.cellfind_kappa_std_ratio = 1;
            img_seg.init_with_gaussian = 0;
            img_seg.kappa_std_ratio = 1;
            img_seg.downsample_time_by = 1;
            img_seg.downsample_space_by = 1;
            img_seg.min_radius_after_downsampling = 5;
            img_seg.min_tau_after_downsampling = 5;
            img_seg.reestimate_S_if_downsampled = 0;
            img_seg.reestimate_T_if_downsampled = 1;
            img_seg.crop_circular = 0;
            img_seg.movie_mask = randi(2,100,100)-1;
            img_seg.smoothing_ratio_x2y = 0;
            img_seg.compact_output = 1;
            img_seg.cellfind_numpix_threshold = 9;
            img_seg.high2low_brightness_ratio = Inf;
            img_seg.l1_penalty_factor = 0;
            img_seg.T_lower_snr_threshold = 10;
            img_seg.smooth_T = 0;
            img_seg.smooth_S = 1;
            img_seg.max_iter_S = 100;
            img_seg.max_iter_T = 100;
            img_seg.TOL_sub = 1.0000e-06;
            img_seg.TOL_main = 0.0100;
            img_seg.avg_cell_radius = 0;
            img_seg.T_min_snr = 10;
            img_seg.size_lower_limit = .1000;
            img_seg.size_upper_limit = 10;
            img_seg.temporal_corrupt_thresh = 0.7000;
            img_seg.spatial_corrupt_thresh = 0.7000;
            img_seg.eccent_thresh = 6;
            img_seg.low_ST_index_thresh = 0.0100;
            img_seg.low_ST_corr_thresh = 0;
            img_seg.S_dup_corr_thresh = 0.9500;
            img_seg.T_dup_corr_thresh = 0.9500;
            img_seg.confidence_thresh = 0.8000;
            img_seg.high_ST_index_thresh = 0.8000;
            ophys_module.nwbdatainterface.set('ImgSegmentation', img_seg);
        end
    end
    methods (Test)
        function RoundTrip(testCase)
            % get ImageSegmentation before writing
            writeSeg = testCase.file.processing.get('test_ophys').nwbdatainterface.get('ImgSegmentation');
            filename = ['ndx_extract.testRoundTrip.nwb'];
            nwbExport(testCase.file, filename);
            readFile = nwbRead(filename);
            % get ImageSegmentation from read file
            readSeg = readFile.processing.get('test_ophys').nwbdatainterface.get('ImgSegmentation');
            % recast boolean parameters as logical. Boolean types not
            % supported when writing to HDF5 - causing test to fail
            props = properties(writeSeg);
            for i = 1:numel(props)
                if isa(writeSeg.(props{i}),'logical')
                    readSeg.(props{i}) = logical(readSeg.(props{i}));
                end
            end
            % verify containers are the same
            tests.util.verifyContainerEqual(testCase,readSeg,writeSeg)
        end
    end
end