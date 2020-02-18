#!/usr/bin/python

import httplib2
import os, io, sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

import auth

PREFIX_FILENAME = '_'

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def _localWriteFile(filename, filepath, data):
    fname = PREFIX_FILENAME+filename
    fid = open(filepath+'/'+fname, 'w')
    fid.write(data)
    fid.close()

def _localSearchFile(filename, filepath):
    ret_filename = ""

    print("%s, %s" % (filename, filepath))
    file_list = os.listdir(filepath)

    #print(file_list)
    for for_file in file_list :
        #print(for_file)
        if filename == for_file:
            ret_filename = for_file

    #print(ret_filename)

    return ret_filename

def _checkUploadMetafileID(filename, filepath):
    metafileID = ""
    metafilename = PREFIX_FILENAME+filename
    if _localSearchFile(metafilename, filepath) != "" :
        #print("aaaaaaaaaaaaa")
        fid = open(filepath+"/"+metafilename, 'r')
        metafileID = fid.readline()
        #print(metafileID)
        fid.close()

    #print("bbbbbbbbbbbbb")
    return metafileID

def _listFiles(strings=""):
    #print("aaaaaa")
    #results = drive_service.files().list(pageSize=size,fields="nextPageToken, files(id, name)").execute()
    results = drive_service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if items:
    #if not items:
        #print('No files found.')
    #else:
        for item in items:
            if strings == item['name'] :
                print("%s" % item['id'])
                return item['id']
            elif strings == item['id'] :
                print("%s" % item['name'])
                return item['id']
            elif strings == "" :
                print("%s, %s" % (item['name'], item['id']))

def _uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    file_path = filepath+'/'+filename
    #print(file_path)
    media = MediaFileUpload(file_path, mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))
    #_localWriteFile(filename, filepath, file.get('id'))

def _deleteFile(fileid):
    is_success = 0
    
    if fileid == "" :
        return is_success

    try:
        print(fileid)
        drive_service.files().delete(fileId=fileid).execute()
        is_success = 1
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
        is_success = 0

    return is_success

def downloadFile(file_id,filepath):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(filepath,'wb') as f:
        fh.seek(0)
        f.write(fh.read())

def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))

def searchFile(size,query):
    results = drive_service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            print('{0} ({1})'.format(item['name'], item['id']))

def main(method, length) :
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json

    cmd = method[1]

    #print(cmd)
    if cmd == 'upload':
        if length == 5:
            _uploadFile(method[2], method[3], method[4])
        elif length == 4:
            _uploadFile(method[2], method[3], 'text/csv')
        elif length == 3:
            _uploadFile(method[2], os.getcwd(), 'text/csv')
        else:
            print("ERROR : ./main.py upload [filename] [path of file] [file type]")
    elif cmd == 'list':
        if length == 2:
            _listFiles()
        elif length == 3:
            #print(method[2])
            _listFiles(method[2])
    elif cmd == 'delete':
        if length == 4:
            #print(_localSearchFile(method[2], method[3]))
             _deleteFile(_checkUploadMetafileID(method[2], method[3]))
            #if _deleteFile(_checkUploadMetafileID(method[2], method[3]))
                #os.remove(method[3]+'/'+PREFIX_FILENAME+method[2])
        elif length == 3:
            #print(_checkUploadMetafileID(method[2], os.getcwd()))
            _deleteFile(_listFiles(method[2]))
        else:
            print("ERROR : ./main.py delete [filename] [path of file]")
    elif cmd == 'download':
        download(sys.argv[2], sys.argv[3])
    elif cmd == 'share':
    	share(sys.argv[2], sys.argv[3])
    elif method == 'folder':
        print("*********************")
        createfolder(sys.argv[2])
    elif cmd == 'debug':
        print(os.getcwd())


if __name__ == '__main__' :

    if len(sys.argv) >= 2 :
        #print(len(sys.argv))
        main(sys.argv, len(sys.argv))

#uploadFile('unnamed.txt', os.getcwd(),'text/csv')
#downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg'
#createFolder('Google')
#searchFile(10,"name contains 'Getting'")
