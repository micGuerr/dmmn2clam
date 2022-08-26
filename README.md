# DMMN 2 CLAM

This repository contains the code to allow [DMMN-ovary segmentation](https://github.com/MSKCC-Computational-Pathology/DMMN-ovary) approach to be integrated into the [CLAM framework](https://github.com/mahmoodlab/CLAM).

## Problem

...

## Solution

...

## Download and installation

Both CLAM and DMMN-Ovary GitHub repositories should be downloaded from their original project repos.

dmmn2clam repo can be downloaded here using the following command from command line:
```
git clone https://github.com/micGuerr/dmmn2clam.git
```

Let's assume CLAM's repo is downloaded in `<fullPath_to_CLAM_repo>`, DMMN-Ovary repo is downloaded in `<fullPath_to_DMMN-ovary_repo>` and dmmn2clam repo is downloaded in `<fullPath_to_dmmn2clam_repo>`.


### Installation

1. Configure both CLAM and DMMN-Ovary GitHub repositories in such a way they can be used in their standard configuration.

2. Run the following commands from command line:
```
ln -s <fullPath_to_dmmn2clam_repo>/create_patches_fp_dmmn2clam.py <fullPath_to_CLAM_repo>/create_patches_fp_dmmn2clam.py

ln -s <fullPath_to_dmmn2clam_repo>/WholeSlideImage_dmmn2clam.py <fullPath_to_CLAM_repo>/wsi_core/WholeSlideImage_dmmn2clam.py

ln -s <fullPath_to_dmmn2clam_repo>/batch_process_utils_dmmn2clam.py <fullPath_to_CLAM_repo>/wsi_core/batch_process_utils_dmmn2clam.py
```

```
ln -s <fullPath_to_dmmn2clam_repo>m/slidereader_coords_dmmn2clam.py <fullPath_to_DMMN-ovary_repo>/slidereader_coords_dmmn2clam.py

ln -s <fullPath_to_dmmn2clam_repo>/inference_dmmn2clam.py <fullPath_to_DMMN-ovary_repo>/inference_dmmn2clam.py
```

Note that in Windows the link can be constructed as:
```

```

## Usage

Below an example of the commands needed to integrate the DMMN-ovary segmentation into CLAM (here I assume that there are two conda environments configured for either DMMN-ovary or CLAM):
```
cd <fullPath_to_DMMN-ovary_repo>
conda activate <clam_conda_env_name>
python slidereader_coords_dmmn2clam.py --source <path_to_slideList>.txt --out_path <coord_file_name>.csv
python inference_dmmn2clam.py --coord_path <coord_file_name>.csv --source <source_data> --out_path <seg_folder_name>
conda deactivate
```

```
cd <fullPath_to_CLAM_repo>
conda activate <dmmn_conda_env_name>
python create_patches_fp_dmmn2clam.py --source <source_data> --dmmn_seg <seg_folder_name>  --save_dir <output_dir> --patch_size 256 --seg --patch --stitch
conda deactivate
```

## Issues

* I launched the segmentation from PyCharm. The following error was thrown which should be linked to a memory issue:
  ```
  Process finished with exit code 137 (interrupted by signal 9: SIGKILL)
  ```
* A couple of slide segmentations seem to have been stopped abruptly.

## Results

Check [here](tmp/img/) for some results.





