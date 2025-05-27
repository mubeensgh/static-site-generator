import os
import shutil

def _helper_recursive_copyer(originpath: str, destpath:str):
    '''
    Internal Helper function.
    '''
    if not os.path.exists(destpath):
        print(f'creating subdirectory {destpath}...')
        os.mkdir(destpath)
    
    print(f'DEBUG: Listing contents of {originpath} for copying...')
    items_in_originpath = os.listdir(originpath)
    print(f"  DEBUG: Items found: {items_in_originpath}")

    for item in items_in_originpath:
        origin_item_path = os.path.join(originpath,item)
        dest_item_path = os.path.join(destpath,item)

        if os.path.isfile(origin_item_path):
            print(f"copying file: {origin_item_path} to {dest_item_path}")
            shutil.copy(origin_item_path, dest_item_path)
        elif os.path.isdir(origin_item_path):
            _helper_recursive_copyer(origin_item_path, dest_item_path)

def copy_static_to_public(originpath:str, destpath:str):
    if os.path.exists(destpath):
        shutil.rmtree(destpath)
    os.mkdir(destpath)
    _helper_recursive_copyer(originpath,destpath)

