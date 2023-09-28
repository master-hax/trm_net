import leafmap.foliumap as leafmap
import os
from os.path import join
import argparse

#  Example: python download_maxar.py tonga-volcano21 --data_dir data

def parse_args():
    parser = argparse.ArgumentParser(description='trm-net data downloader for maxar open datasets')
    parser.add_argument('collection', help='Collection Name ex. tonga-volcano21')
    parser.add_argument(
        '--data_dir', help='the dir to save data')
    parser.add_argument('--all', action='store_true', help='download all collections')
    args = parser.parse_args()
    return args
  

# create function to download Maxar imagery
def download_maxar(collection_name,data_dir):
    try:
        collections = leafmap.maxar_child_collections(collection_name)
    except:
        print("The collection name is not valid.")
        return
    print("downloading " + collection_name + " collection")
    
    num_collections = len(collections)

    if num_collections == 0:
        print("The collection name is not valid.")
        return
    
    print("There are " + str(num_collections) + " child collections.")
    
    collections.sort()

    for i in range(len(collections)):
        gdf = leafmap.maxar_items(
            collection_id=collection_name, 
            child_id=collections[i],
            return_gdf=True, 
            assets=['visual'])
        images = gdf['visual'].tolist()
        download_dir = join(data_dir,(collection_name))
        print("reached")
        # leafmap.maxar_download(images, out_dir=download_dir)

    print("Download completed!")

# main function
def main():
    args = parse_args()
    if args.collection is None:
        print("Please specify the collection name.")
        return
    if args.data_dir is None:
        print("Please specify the data directory.")
        return
    if args.all is True:
        collections = leafmap.maxar_collections()
        for collection in collections:
            download_maxar(collection,args.data_dir)
    else:
        download_maxar(args.collection,args.data_dir)
    
if __name__ == "__main__":
    main()
