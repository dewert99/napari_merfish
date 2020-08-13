Setup:
1. Install conda https://docs.conda.io/en/latest/miniconda.html
2. Run "conda env create -f env.yml" from inside this directory
3. To run napari use "python __main__.py ..." from inside this directory or run "python path/to/napari ..."

Use the path to a directory outputted by the cambridge pipeline (the directory should contain "zarr", "offsets.json", "processed" ...) for the path argument

To speed up downloading of this type of directory, skip larger numbered subdirectories in the "zarr" amd "processed" directories
You still need to download all non-numbered sub-directories (x, y, z, bit, imgType)
When you do this set the --fov_number option to the number of numbered sub-directory downloaded (this should be the largest number + 1)
eg. download (000, 001, 002, 003, bit, imgType, x, y, z) and use --fov_number 4