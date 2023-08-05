import os
from ftplib import FTP

ftp_client = None


def create_ftp_client():
    ftp = FTP()
    ftp.connect(host="172.16.8.151")
    ftp.login("ftp", "ftp@123456")
    ftp.cwd("off-images")


def save_file_to_ftp(remote_path, local_path):
    if not ftp_client:
        create_ftp_client()
    buffer_size = 1024
    fp = open(local_path, 'rb')
    ftp_client.storbinary('STOR ' + remote_path, fp, buffer_size)
    ftp_client.set_debuglevel(0)
    fp.close()


if __name__ == "__main__":
    cover_dir = "G:/spider/ready/cover"
    for local_file in os.listdir(cover_dir):
        remote_path = "cover" + "/" + os.path.basename(local_file)
        local_path = cover_dir + "/" + local_file
        print "put ftp file:", remote_path, local_path
        save_file_to_ftp(remote_path, local_path)
