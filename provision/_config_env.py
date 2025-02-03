import argparse
import os
import sys
import boto3
import shutil

TACTEON_BUCKET = 'tacteon-ops'
JITGURU_BUCKET_KEY = "jitguru"
LOCAL_ENV_FILENAME = '.env_local'
LOCAL_DJANGO_SETTINGS_FILENAME = 'django_settings_local.py'
parser = None
args = None
WORKING_FOLDER = os.path.join(os.getcwd(), 'working')
if not os.path.isdir(WORKING_FOLDER):
    print(f"creating working folder: {WORKING_FOLDER}")
    os.mkdir(WORKING_FOLDER)

def config_local():
    status()
    download_env_local()
    shutil.copy(os.path.join(WORKING_FOLDER, LOCAL_ENV_FILENAME), os.path.join(os.getcwd(), '.env'))
    print(f"{"install env_local":32}: ok")
    shutil.copy(os.path.join(WORKING_FOLDER, LOCAL_DJANGO_SETTINGS_FILENAME), os.path.join(os.getcwd(), 'jitgurup', 'settings.py'))
    print(f"{"install django_settings_local":32}: ok")

def download_env_local():
    s3 = boto3.client('s3')
    s3.download_file(TACTEON_BUCKET, os.path.join(JITGURU_BUCKET_KEY, 'env_local'), os.path.join(WORKING_FOLDER, LOCAL_ENV_FILENAME))
    print(f"{"download env_local":32}: ok")
    s3.download_file(TACTEON_BUCKET, os.path.join(JITGURU_BUCKET_KEY, 'django_settings_local.py'), os.path.join(WORKING_FOLDER, LOCAL_DJANGO_SETTINGS_FILENAME))
    print(f"{"download django_settings_local":32}: ok")

def banner():
    print("""
================================================================    
  w w  w                                              d8b w      
  w w w8ww .d88 8   8 8d8b 8   8    .d8b .d8b. 8d8b.  8'  w .d88 
  8 8  8   8  8 8b d8 8P   8b d8    8    8' .8 8P Y8 w8ww 8 8  8 
  8 8  Y8P `Y88 `Y8P8 8    `Y8P8    `Y8P `Y8P' 8   8  8   8 `Y88 
wdP        wwdP                                             wwdP 
________________________________________________________________    
    """)
def status():
    if parser and args:
        print(f"environment: {args.environment}")
    else:
        print(f"no command line parser, args available. tool status unknown.")
def config():
    global parser, args
    # print(sys.argv)
    banner()
    parser = argparse.ArgumentParser('jitguru-config', 'configures runtime environment for jitguru micro-scheduler api', '@2025')
    parser.add_argument('-e', '--environment')
    args = parser.parse_args()
    if args.environment:
        if args.environment.lower() == 'local':
            config_local()
        else:
            print(f"unsupported environment: {args.environment}")
    else:
        print(f"require --e <environment>: found: {args.environment}")

if __name__ == '__main__':
    config()