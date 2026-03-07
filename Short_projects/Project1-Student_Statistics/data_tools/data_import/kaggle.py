import kagglehub
import os
import shutil

def download_data(url):
    """Download dataset from kaggle and automatically moves data to the main directory.
    
    The initial program is run without sudo privileges. The second step uses `sudo`, which requires that
    the user has access to the terminal in order to input the password. 

    Args:
        url (string): The kaggle url that is in the form `username/dataset_short_name`
        
    Returns:
        None
    """
    
    #TODO: 'Unexpected error: expected str, bytes or os.PathLike object, not CompletedProcess'
    pwd = os.getcwd()
    path = kagglehub.dataset_download(url)
    print("Path to dataset files:", path)
    #shutil.move(path, pwd)