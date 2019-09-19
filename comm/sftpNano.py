from paramiko import Transport, SFTPClient
from configuration.ateConfig import *
from configuration import ateConfig
import time
import errno
import shutil
import os
import pexpect
import subprocess
import json
import stat
class SftpNano():
    def __init__(self):
        self._sftpConnection = None

    def create_connection(self, host, port, username, password):
        try:
            port = int(port)
            ssh_conn = Transport(sock=(host, port), default_window_size = 2147483647)
            ssh_conn.packetizer.REKEY_BYTES = pow(2, 40)
            ssh_conn.packetizer.REKEY_PACKETS = pow(2, 40)
            ssh_conn.connect(username=username, password=password)
            self.port = port
            self.username = username
            self.host = host
            self.password = password

            USB_NANO_PATH = '/dev/nano'
            self.chmod(USB_NANO_PATH, 0o777)
            # ssh_conn.get_transport().window_size = 3 * 1024 * 1024
            self._sftpConnection = SFTPClient.from_transport(ssh_conn)
            self._file_to_be_sent = ''
            # self._sftpConnection.get_transport().window_size = 3 * 1024 * 1024

        except Exception as exc:
            ateConfig.log.logger.error("Error creating sftp communication: %s" % str(exc))
            raise

    def chmod(self, object, mode):
        child = None
        try:
            child = pexpect.spawn('sudo chmod {} {}'.format(mode, object), timeout=14400)
            self._handle_sftp_prompt(child)
            child.expect(pexpect.EOF)
        finally:
            if child:
                child.close()
                if child.isalive():
                    ateConfig.log.logger.warning('Child did not exit gracefully.')
                else:
                    ateConfig.log.logger.warning('Child exited gracefully.')

        # if child:
        #     if child.status > 0:
        #         raise Exception('')
        #     else:
        #         ateConfig.log.logger.info('Removing file completed')

    def uploading_info(self, uploaded_file_size, total_file_size):
        ateConfig.log.logger.debug('uploaded_file_size : {} total_file_size : {}'.format(uploaded_file_size,
                                                                                         total_file_size))

    def local_file_exists(self, localFilePath):
        try:
            if os.path.isfile(localFilePath):
                return True
        except Exception as e:
            ateConfig.log.logger.debug("Error: %s" %str(e))
            return False
        else:
            # ateConfig.log.logger.debug("File does not exist")
            return False

    def local_dir_exists(self, localPath):
        try:
            if os.path.exists(localPath):
                return True
        except Exception as e:
            ateConfig.log.logger.debug("Error: %s" %str(e))
            return False
        else:
            # ateConfig.log.logger.debug("File does not exist")
            return False

    def remote_file_exists(self, remoteFilePath):
        try:
            self._sftpConnection.stat(remoteFilePath)
        except Exception as e:
            # if e.errno == errno.ENOENT:
            #     ateConfig.log.logger.debug("File does not exist")
            #     return False
            ateConfig.log.logger.debug("File does not exist %s" %str(e))
        else:
            ateConfig.log.logger.debug("File exists")
            return True

    def remove_remote_file(self, remoteFilePath):
        if self.remote_file_exists(remoteFilePath):
            ateConfig.log.logger.debug("Remove remote file: %s" % str(remoteFilePath))
            self._sftpConnection.remove(remoteFilePath)

    def remove_local_file(self, localFilePath):
        child = None
        if self.local_file_exists(localFilePath):
            ateConfig.log.logger.debug("Remove local file...: %s" %localFilePath)
            try:
                child = pexpect.spawn('/bin/rm {}'.format(localFilePath),timeout=14400)
                self._handle_sftp_prompt(child)
                child.expect(pexpect.EOF)
            finally:
                if child:
                    child.close()
                    if child.isalive():
                        ateConfig.log.logger.warning('Child did not exit gracefully.')
                    else:
                        ateConfig.log.logger.warning('Child exited gracefully.')

            if child:
                if child.status > 0:
                    raise Exception('')
                else:
                    ateConfig.log.logger.info('Removing file completed')

    def remove_files_in_local_directory(self, localPath):
        child = None
        if len(os.listdir(localPath)) != 0:
            for the_file in os.listdir(localPath):
                file_path = os.path.join(localPath, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

    def remove_local_empty_dir(self, localPath):
        os.rmdir(localPath)

    def remote_folder_exists(self, remotePath):
        try:
            self._sftpConnection.chdir(remotePath)
            return True
        except IOError as e:
            return False


    def get_file(self, remoteFilePath, localFilePath):
        # 1st method
        # self._sftpConnection.get(remoteFilePath, localFilePath)

        # 2nd method: SFTP terminal command
        child = None
        if self.remote_file_exists(remoteFilePath):
            ateConfig.log.logger.debug("Getting remote file...")
            # with self._sftpConnection.open(remoteFilePath, 'r') as remote_file:
            #     shutil.copyfileobj(remote_file, open(localFilePath, 'w'))
            # self._sftpConnection.get(remoteFilePath, localFilePath, callback=None)
            try:
                child = pexpect.spawn(
                    '/usr/bin/sftp -r -P {} {}@{}:{} {}'.format(self.port, self.username, self.host, remoteFilePath, localFilePath),
                                      timeout=14400)
                self._handle_sftp_prompt(child)
                child.expect(pexpect.EOF)
            finally:
                if child:
                    child.close()
                    if child.isalive():
                        ateConfig.log.logger.warning('Child did not exit gracefully.')
                    else:
                        ateConfig.log.logger.warning('Child exited gracefully.')

            # if child:
            #     if child.status > 0:
            #         raise Exception('Still exists')
            #     else:
            #         ateConfig.log.logger.info('Getting file completed')

        # 3rd method: SCP terminal command
        # child = None
        # if self.remote_file_exists(remoteFilePath):
        #     ateConfig.log.logger.debug("Getting remote file...")
        #     # with self._sftpConnection.open(remoteFilePath, 'r') as remote_file:
        #     #     shutil.copyfileobj(remote_file, open(localFilePath, 'w'))
        #     # self._sftpConnection.get(remoteFilePath, localFilePath, callback=None)
        #     try:
        #         child = pexpect.spawn(
        #             '/usr/bin/scp -r -P {} {}@{}:{} {}'.format(self.port, self.username, self.host, remoteFilePath, localFilePath),
        #                               timeout=14400)
        #         self._handle_sftp_prompt(child)
        #         child.expect(pexpect.EOF)
        #     finally:
        #         if child:
        #             child.close()
        #             if child.isalive():
        #                 ateConfig.log.logger.warning('Child did not exit gracefully.')
        #             else:
        #                 ateConfig.log.logger.warning('Child exited gracefully.')
        #
        #     if child:
        #         if child.status > 0:
        #             raise Exception('Still exists')
        #         else:
        #             ateConfig.log.logger.info('Getting file completed')

    def put_file(self, localFilePath, remoteFilePath):
        # sftp {user}@{host}:{remote_dir} <<< $'put {local_file_path}'
        # ateConfig.log.logger.debug('Putting file %s to %s' %(localFilePath, remoteFilePath))

        remoteFolderName = '/'.join(remoteFilePath.split('/')[:-1]) + '/'

        # 1st method
        # if self.local_file_exists(localFilePath):
        #     if not self.remote_folder_exists(remoteFolderName):
        #         self._sftpConnection.mkdir(remoteFolderName)
        #     ateConfig.log.logger.info('Putting file %s to %s' %(localFilePath, remoteFilePath))
        #     self._sftpConnection.put(localFilePath, remoteFilePath)

        #2nd method: SFTP terminal cmds
        child = None
        if self.local_file_exists(localFilePath):
            if not self.remote_folder_exists(remoteFolderName):
                self._sftpConnection.mkdir(remoteFolderName)
            ateConfig.log.logger.info('Putting file %s to %s' %(localFilePath, remoteFilePath))
            try:
                self._file_to_be_sent = localFilePath
                child = pexpect.spawn("/usr/bin/sftp -q {}@{}:{}".format(self.username, self.host, remoteFolderName), timeout=14400)

                self._handle_sftp_prompt(child)
                child.expect(pexpect.EOF)

            finally:
                if child:
                    child.close()
                    if child.isalive():
                        ateConfig.log.logger.warning('Child did not exit gracefully.')
                    else:
                        ateConfig.log.logger.warning('Child exited gracefully.')

            if child:
                if child.status > 0:
                    raise Exception('')
                else:
                    ateConfig.log.logger.info('Putting file completed')

        #3rd method: SCP terminal cmds
        # child = None
        # if self.local_file_exists(localFilePath):
        #     if not self.remote_folder_exists(remoteFolderName):
        #         self._sftpConnection.mkdir(remoteFolderName)
        #     ateConfig.log.logger.info('Putting file %s to %s' %(localFilePath, remoteFilePath))
        #     try:
        #         self._file_to_be_sent = localFilePath
        #         child = pexpect.spawn("/usr/bin/scp {} -q {}@{}:{}".format(localFilePath, self.username, self.host, remoteFolderName), timeout=14400)
        #
        #         self._handle_sftp_prompt(child)
        #         child.expect(pexpect.EOF)
        #
        #     finally:
        #         if child:
        #             child.close()
        #             if child.isalive():
        #                 ateConfig.log.logger.warning('Child did not exit gracefully.')
        #             else:
        #                 ateConfig.log.logger.warning('Child exited gracefully.')
        #
        #     if child:
        #         if child.status > 0:
        #             child.close()
        #             ateConfig.log.logger.warning('Child status: %s' %child.status)
        #         else:
        #             ateConfig.log.logger.info('Putting file completed')

    def _handle_sftp_prompt(self, child):
        # ateConfig.log.logger.debug('Expecting prompt...')
        i = child.expect(['.*password:.*', '.*continue connecting.*', '.*Connected.*', 'replace .*', pexpect.EOF, 'sftp>'])
        # ateConfig.log.logger.debug(child.after)
        if i == 0:
            ateConfig.log.logger.debug('Supplying pass to sftp server')
            child.sendline(self.password)
            ateConfig.log.logger.debug('sent pw')
            self._handle_sftp_prompt(child)
        elif i == 1:
            ateConfig.log.logger.debug('Answering yes to host check')
            child.sendline('yes')
            ateConfig.log.logger.debug('Sent yes')
            self._handle_sftp_prompt(child)
        elif i == 2:
            ateConfig.log.logger.debug('Connected to sftp server')
            child.sendline('yes')
            self._handle_sftp_prompt(child)
        elif i == 3:
            ateConfig.log.logger.debug('Answering A to replace case when unzip: replace [A]ll')
            child.sendline('A')
            self._handle_sftp_prompt(child)
        elif i == 4:
            # ateConfig.log.logger.debug('Received EOF')
            # self._handle_sftp_prompt(child)
            pass

        elif i == 5:
            ateConfig.log.logger.debug('Inside SFTP session')
            if self._file_to_be_sent:
                ateConfig.log.logger.debug('Putting file %s' % self._file_to_be_sent)
                child.sendline('put {}'.format(self._file_to_be_sent))
                self._file_to_be_sent = ''
                self._handle_sftp_prompt(child)
            else:
                child.sendline('bye')

        else:
            ateConfig.log.logger.debug('Invalid case')

    def compress_local_folder(self, localFolderPath, localOutputFilePath):
        parentFolder = '/'.join(localFolderPath.split('/')[:-2]) + '/'
        folderName = localFolderPath.split('/')[-2]

        print(localFolderPath, parentFolder, folderName)

        if self.local_dir_exists(localFolderPath):
            ateConfig.log.logger.debug('Compressing folder %s to %s' % (localFolderPath, localOutputFilePath))
            os.system(" cd {}/ && tar -cvf {} {}/".format(parentFolder, localOutputFilePath, folderName))

    def decompress_local_file(self, localFilePath, localOutputFolderPath):
        if not self.local_dir_exists(localOutputFolderPath):
            os.mkdir(localOutputFolderPath)

        else:
            ateConfig.log.logger.debug('Decompressing file %s to %s' % (localFilePath, localOutputFolderPath))
            os.system("tar xf {} -C {}".format(localFilePath, localOutputFolderPath))

    def parse_local_json(self, localFilePath):
        with open(localFilePath, 'r') as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return obj

    def close_connection(self):
        self._sftpConnection.close()

