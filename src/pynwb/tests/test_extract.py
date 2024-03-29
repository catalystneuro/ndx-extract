from datetime import datetime
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

import numpy as np
from hdmf.testing import TestCase
from numpy.testing import assert_array_equal
from pynwb import NWBFile, NWBHDF5IO
from pynwb.ophys import OpticalChannel

from ndx_extract import EXTRACTSegmentation


class TestExtractSegmentation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session_start_time = datetime.now().astimezone()

        cls.image_segmentation_name = "ExtractSegmentation"

    def setUp(self):
        self.nwbfile = NWBFile(
            session_description="session_description",
            identifier="file_id",
            session_start_time=self.session_start_time,
        )
        # Create the device and optical channel for the imaging plane object.
        device = self.nwbfile.create_device(
            name="Microscope",
            description="My two-photon microscope",
            manufacturer="The best microscope manufacturer"
        )
        optical_channel = OpticalChannel(
            name="OpticalChannel",
            description="My optical channel",
            emission_lambda=500.
        )
        # The imaging plane is required for creating a plane segmentation which
        # in turn is a required attribute for an image segmentation.
        self.imaging_plane = self.nwbfile.create_imaging_plane(
            name="ImagingPlane",
            description='A very interesting part of the brain.',
            optical_channel=optical_channel,
            device=device,
            excitation_lambda=600.,
            indicator="GFP",
            location="V1",
        )
        self.tmpdir = Path(mkdtemp())
        self.nwbfile_path = self.tmpdir / "test_nwb.nwb"

    def tearDown(self):
        rmtree(self.tmpdir)

    def test_extract_defaults(self):
        image_segmentation = EXTRACTSegmentation()
        self.assertEqual(image_segmentation.name, "ImageSegmentation")

    def test_extract_name_propagates(self):
        image_segmentation = EXTRACTSegmentation(name=self.image_segmentation_name)
        self.assertEqual(image_segmentation.name, self.image_segmentation_name)

    def test_extract_roundtrip(self):
        image_segmentation = EXTRACTSegmentation(
            name="test_name",
            version="1.1.0",
            preprocess=True,
            movie_mask=np.ones((15, 15)),
        )

        # Create a plane segmentation and add it to the image segmentation object.
        image_segmentation.create_plane_segmentation(
            imaging_plane=self.imaging_plane,
            description="The description about this plane segmentation."
        )

        ophys_module = self.nwbfile.create_processing_module(
            name="ophys",
            description="optical physiology processed data",
        )

        ophys_module.add(image_segmentation)

        with NWBHDF5IO(self.nwbfile_path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.nwbfile_path, mode="r") as io:
            nwbfile_in = io.read()

            movie_mask = (
                nwbfile_in.processing["ophys"]
                .data_interfaces["test_name"]
                .movie_mask[:]
            )

            assert_array_equal(
                movie_mask,
                np.ones((15, 15)),
            )

        self.assertEqual(
            nwbfile_in.processing["ophys"].data_interfaces["test_name"].version,
            "1.1.0",
        )

        self.assertEqual(
            nwbfile_in.processing["ophys"].data_interfaces["test_name"].preprocess,
            True,
        )
