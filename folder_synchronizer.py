# Szilagyi-Pap David, Internal Development in QA Test Task, Folder synchronizer
import os, shutil, sys, hashlib, datetime, time

# Tested on linux and windows, it is a cross platform solution
# The source and replica paths are going to be the first two arguments
# while the log path is going to be the third one, and interval the fourth (given in seconds)
source = str(sys.argv[1])
replica = str(sys.argv[2])
log = str(sys.argv[3])
interval = int(sys.argv[4])

# here we set up the synchronization's log file
filepath = os.path.join(log, 'synchronization.log')
if not os.path.exists(log):
    os.makedirs(log)
f = open(filepath, "a")

# a logging function so the code looks a bit cleaner
def logging(message, filename):
    current_time = datetime.datetime.now().strftime(("%d/%m/%Y-%H:%M:%S: "))
    print(current_time + message + filename)
    f.write(current_time + message + filename + "\n")
 
# The following function calculates a file's sha256 hash
# so we can compare files
def file_hash(file_path):
    hash_object = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hash_object.update(data)
    return hash_object.hexdigest()

def source_traversal():
    for root, dirs, files in os.walk(source):
        # for starters we are going to take every file in the source folder
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica, os.path.relpath(source_file_path, source))
            # if the file doesn't exist in the replica folder we copy it there
            if not os.path.exists(replica_file_path):
                shutil.copy2(source_file_path, replica_file_path)
                logging("Copied the following file from source to replica folder: ", file)
            # if the replica folder contains a file with a different hash, we recopy the file from the source
            else:
                source_file_hash = file_hash(source_file_path)
                replica_file_hash = file_hash(replica_file_path)
                if source_file_hash != replica_file_hash:
                    shutil.copy2(source_file_path, replica_file_path)
                    logging("Recopied the following file from source to replica folder: ", file)

def replica_traversal():
    for root, dirs, files in os.walk(replica):
        # we check every file in the replica folder, and if we find one not in the source folder, we delete it
        for file in files:
            replica_file_path = os.path.join(root, file)
            source_file_path = os.path.join(source, os.path.relpath(replica_file_path, replica))
            if not os.path.exists(source_file_path):
                os.remove(replica_file_path)
                logging("Deleted the following file from replica folder: ", file)
def main():
    logging("Beginning of logs", "")

    start_time = time.time()
    while True: 
        source_traversal()
        replica_traversal()
        time.sleep(interval - ((time.time() - start_time) % interval))

main()