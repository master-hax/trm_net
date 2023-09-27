import leafmap.foliumap as leafmap
import os

# create function to download Maxar imagery
def download_maxar(collection_name,data_dir):
    try:
        collections = leafmap.maxar_child_collections(collection_name)
    except:
        print("The collection name is not valid.")
        return
    if len(collections) == 0:
        print("No child collections found.")
        return
    
    collections.sort()

    for i in range(len(collections)):
        gdf = leafmap.maxar_items(
            collection_id=collection_name, 
            child_id=collections[i],
            return_gdf=True, 
            assets=['visual'])
        images = gdf['visual'].tolist()
        download_dir = os.join(data_dir,(collection_name+'/'))
        print(download_dir)
        # leafmap.maxar_download(images, out_dir=download_dir)


# main function
def main():
    args = parse_args()
    if args.collection_name is None:
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
        download_maxar(args.collection_name,args.data_dir)
    
if __name__ == "__main__":
    main()
