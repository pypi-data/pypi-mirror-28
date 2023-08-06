Installs script with usage as follows:

usage: xnat-uploader [-h] [--host HOST] [--username USERNAME]
                     [--password PASSWORD] [--project PROJECT]
                     [--subject SUBJECT] [--session SESSION]
                     [--logfile LOGFILE] [--tmpdir TMPDIR] [-V] [-r] [-v]
                     [-t TIMEOUT] [-s SESSIONTIMEOUT] [-j JOBS]
                     directory

Xnat upload script, takes a single directory and uploads to site. Target
directory is a session, with any number of scans within it. Directories within
are treated as scans, populated with either many separate dicom files or a
single compressed flat archive of dicom files. Zip files found in the top
level are treated as a scan and are expected to have a compressed archive of
dcm files. The session name is assumed as the same as the zip file name,
without the zip extension.

positional arguments:
  directory             Directory to upload from

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           URL of xnat host
  --username USERNAME   Username, if not set will pull from XNATCREDS env
                        variable as USERNAME:PASSWORD
  --password PASSWORD   Password, if not set will pull from XNATCREDS env
                        variable as USERNAME:PASSWORD
  --project PROJECT     Project to upload to
  --subject SUBJECT     Subject to upload for
  --session SESSION     Session name to use for upload
  --logfile LOGFILE     File to log upload events to, if not set use stdout
  --tmpdir TMPDIR       Directory to untar compress files to
  -V, --validate        Validate scan descriptions and filecounts after upload
  -r, --raw             Disable recompression as zip file uploading each scan
                        file individually. Severely impacts performance, but
                        can solve problems with extremely large sessions
  -v, --verbose         Produce verbose logging
  -t TIMEOUT, --timeout TIMEOUT
                        Read timeout in seconds, set to higher values if
                        uploads are failing due to timeout
  -s SESSIONTIMEOUT, --sessiontimeout SESSIONTIMEOUT
                        Session timeout for xnat site in minutes, to determine
                        session refresh frequency
  -j JOBS, --jobs JOBS  Run in X parallel processes to take advantage of
                        multiple cores

