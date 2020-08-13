import xarray as xr
import json
import numpy as np
import click
try:
    import napari
except Exception:
    pass


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path", type=click.Path("rb"))
@click.option("-n", "--fov_number", help="Number of fovs to show, starting with fov 0", type=int)
def base_mosaic(path: str, fov_number: int = None):
    zarr: xr.Dataset = xr.open_zarr(f"{path}/zarr")
    sp = json.load(open(f"{path}/offsets.json"))["stagepos"]
    sp = np.array(sp)
    fovs = range(fov_number) if fov_number else range(len(sp))
    offs = sp/np.diff(np.sort(sp, axis=0), axis=0).max(axis=0)
    colour_map = np.array(["red", "green", "blue"])[(np.sum(offs.round().astype("uint8"), axis=1) % 3)]
    with napari.gui_qt():
        viewer = napari.Viewer()
        for i in fovs:
            t = sp[i]
            viewer.add_image(zarr[f"{i:03d}"], translate=(0, 0, 0, t[0], t[1]),
                             blending="additive", colormap=colour_map[i], gamma=2, contrast_limits=(0, 5e3))


@cli.command()
@click.argument("path", type=click.Path("rb"))
@click.option("-n", "--fov_number", help="Number of fovs to show, starting with fov 0", type=int)
def rna_segmentation(path: str, fov_number: int = None, contrast_upper_limit: float = 2e4):
    im: xr.Dataset = xr.open_zarr(f"{path}/processed")
    sp = json.load(open(f"/{path}/offsets.json"))["stagepos"]
    fovs = range(fov_number) if fov_number else range(len(sp))
    sp = np.array(sp)
    with napari.gui_qt():
        viewer = napari.Viewer()
        for i in fovs:
            t = sp[i]
            viewer.add_image(im[f"{i:03d}"].sel(imgType=["bits", "bkg"]), translate=(0, 0, 0, t[0], t[1]), gamma=2, contrast_limits=(0, contrast_upper_limit))
            viewer.add_labels(im[f"{i:03d}"].sel(imgType="seg"), translate=(0, 0, t[0], t[1]))


def comp2(path: str, i: int, j: int):
    zarr: xr.Dataset = xr.open_zarr(f"{path}/zarr")
    sp = json.load(open(f"{path}/offsets.json"))["offsets"]
    sp = {**sp[0], **sp[1]}
    try:
        t = sp[f"{i}:{j}"]
    except KeyError:
        i, j = j, i
        t = sp[f"{i}:{j}"]
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(zarr[f"{i:03d}"], blending="additive", colormap="red", gamma=2, contrast_limits=(0, 5e3))
        viewer.add_image(zarr[f"{j:03d}"], translate=(0, 0, 0, t[0], t[1]),
                         blending="additive", colormap="green", gamma=2, contrast_limits=(0, 5e3))


if __name__ == '__main__':
    cli()
