import itertools
from duckduckgo_search import ddg_images

#!pip install fastai duckduckgo_search
from fastai.vision.all import *
from fastai import *
from pathlib import Path

from fastai.vision.utils import download_images

# SETTINGS

imgs_per_category = 10
img_size=200

categories = (
    'Dall-E', 'Midjourney', 'Stable Diffusion',
)

search_terms = (
    'Generated with %s',
)

#%%
from fastai.data.transforms import get_image_files
from fastai.vision.utils import resize_images, verify_images
from fastcore.all import *

def search_images(term, max_images=200):
    return L(ddg_images(term, max_results=max_images)).itemgot('image')

# Categories should work both as search term and directory name
#For simplicity: keep these in alphabetical order

path = Path('midge_or_not')
for label in categories:
    dest = path/label
    dest.mkdir(exist_ok=True, parents=True)
    urls = []
    for search_term in search_terms:
        urls.extend(search_images(search_term % label, imgs_per_category))
    download_images(dest, urls=urls)
    resize_images(dest, max_size=400, dest=dest)

failed = verify_images(get_image_files(path))
failed.map(Path.unlink)
print(f'removed {len(failed)} bad images')

#%%
def randomcrop(filepath, source_dir, dest_dir, size):
    print(f'randomcrop called with {filepath} ')
    full_src = source_dir / filepath
    full_dest = dest_dir / filepath
    if full_dest.exists():
        return
    full_dest.parent.mkdir(exist_ok=True)
    img = Image.open(full_src)
    w, h = img.size
    if w<size or h<size:
        print('skipping small image')
        return
    left = random.randint(0, w - size)
    top = random.randint(0, h - size)
    right = left + size
    bottom = top + size#
    cropped = img.crop((left, top, right, bottom))
    cropped.save(full_dest)

def crop_all_images(source_path: Path, dest_path:Path, crop_size:int):
    """
    take a random n x n crop of each image in path, recursing through directories
    """
    dest_path.mkdir(exist_ok=True)
    files = get_image_files(source_path, recurse=True)
    files = [o.relative_to(source_path) for o in files]
    parallel(randomcrop, files, source_dir=source_path, dest_dir=dest_path, size=crop_size)

dest = Path('midge_or_not_cropped')
crop_all_images(path, dest, img_size)
#%%
from fastai.vision.augment import Resize
from fastai.data.transforms import RandomSplitter, parent_label
from fastai.vision.data import ImageBlock
from fastai.data.block import DataBlock, CategoryBlock

datablock = DataBlock(
    blocks=(ImageBlock, CategoryBlock),
    get_items=get_image_files,
    splitter=RandomSplitter(valid_pct=0.2),
    get_y=parent_label,
    item_tfms=[Resize(img_size, method='squish')]
)
loaders = datablock.dataloaders(path)
loaders.show_batch()

