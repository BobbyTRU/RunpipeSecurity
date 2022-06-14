from azure.storage.blob import BlobServiceClient
import os
import time


STORAGEACCOUNTURL = "https://powerappsblobconsti.blob.core.windows.net"
STORAGEACCOUNTKEY = "eWotIhZtPl6UTxidPxGufuI/fotsO70uWVmctpg2Oj/R4UIA3T+N1az3VRy6Aj84N3FHsMyDTbdvNo3e+oseGg=="
CONTAINERNAME = "securitymonitoring"

blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)

def downloadApps():
    start = time.time() 
    container_client = blob_service_client_instance.get_container_client("securitymonitoring")
    appCounter = 0
    for blob in container_client.list_blobs():        
        parent_dir = "./BlobFolder"
        blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, blob.name, snapshot=None)
        blob_data = blob_client_instance.download_blob()
        
        justTheName = blob.name.split("apps/",1)[1]  
        folderName = justTheName + " folder"

        parent_dir = os.path.join(parent_dir, folderName)

        if(not os.path.exists(parent_dir)):
            os.mkdir(parent_dir)
        

        fileName = justTheName   
        path = os.path.join(parent_dir, fileName)

        if(not os.path.exists(path)):
            with open(path, "wb") as download_file:
                download_file.write(blob_client_instance.download_blob().readall())

        unpack_dir_name = justTheName + " unpacked"
        unpack_dir_path = os.path.join(parent_dir,unpack_dir_name)
        if(not os.path.exists(unpack_dir_path)):
            os.mkdir(unpack_dir_path)
            os.system('pac canvas unpack --msapp "' + path + '" --sources "' + unpack_dir_path +'"')
        appCounter += 1
        
    end = time.time()
    dif = end - start
    print("downloading and unpacking took:", dif,"s") 
    return dif, appCounter


