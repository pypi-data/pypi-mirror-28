import argparse, os
from subprocess import call
from os.path import expanduser
from timeit import default_timer as timer

def easy_path(my_file):
    return expanduser(my_file)

def get_efs_name(client, file_system_id):
    return client.describe_tags(FileSystemId=file_system_id).get('Tags')[0].get('Value')

MOUNT_VERSION="4"
RSIZE="1048576"
WSIZE="1048576"
PROFILE="default"
REGION="us-west-2"
CREDENTIALS="~/.aws/credentials"
RESILIENCE="hard"
TIMEO="600"
RETRANS="2"

def speed_test(number_GB, out_file):
    in_file = '.temp-file'
    out_file = easy_path(out_file)
    f = open(in_file,"wb")
    f.seek(1073741824*int(number_GB)-1)
    f.write(b'\0')
    f.close()
    os.stat(in_file).st_size
    start = timer()
    os.rename(in_file, out_file)
    end = timer()
    print("Size of file moved: ", os.stat(out_file).st_size//1073741824, "GB")
    print("Time elapsed: ", end - start)

    os.remove(out_file)

def mount(args):
    # TODO: Need to check if file_system_id and efs_mount_point exists
    call("sudo mount -t nfs -o nfsvers={mount_version},rsize={rsize},wsize={wsize},{resilience},timeo={timeo},retrans={retrans} {file_system_id}.efs.{region}.amazonaws.com:/ {efs_mount_point}".format(
        mount_version=args.mount_version or MOUNT_VERSION,
        rsize=args.rsize or RSIZE,
        wsize=args.wsize or WSIZE,
        resilience=args.resilience or RESILIENCE,
        timeo=args.timeo or TIMEO,
        retrans=args.retrans or RETRANS,
        file_system_id=args.file_system_id,
        region=args.region or REGION,
        efs_mount_point=args.efs_mount_point
    ).split())

def unmount(args):
    call(['unmount', args.efs_mount_point])

def get_arguments():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands')
    subparsers.dest = '{mount,unmount}'

    parser.add_argument('--test', dest='test', default=0, required=False, help='Test the speed of file transfer')
    parser.add_argument('--profile', dest='aws_profile', default=PROFILE, required=False, help='The aws cli profile')
    parser.add_argument('--mount-version', dest='mount_version', default=MOUNT_VERSION, required=False, help='The version for your mount executable')
    parser.add_argument('--region', dest='region', default=REGION, required=False, help='The region your efs is in')
    parser.add_argument('--credentials', dest='aws_credentials', default=CREDENTIALS, required=False, help='The path to your aws credentials folder')
    parser.add_argument('--rsize', dest='rsize', default=RSIZE, required=False, help='The the rsize for your efs')
    parser.add_argument('--wsize', dest='wsize', default=WSIZE, required=False, help='The the wsize for your efs')
    parser.add_argument('--resilience', dest='resilience', default=RESILIENCE, required=False, help='Wheather to wait if for efs to come back online or not')
    parser.add_argument('--timeo', dest='timeo', default=TIMEO, required=False, help='Timeout wait for connection')
    parser.add_argument('--retrans', dest='retrans', default=RETRANS, required=False, help='Number of retries to connect')
    parser.add_argument('--mount-point', dest='efs_mount_point', action='store', required=True, help='The mount point for your efs')

    mount = subparsers.add_parser('mount', help='Mount to EFS')
    mount.add_argument('--file-system-id', dest='file_system_id', action='store', required=True, help='Your efs ID')

    unmount = subparsers.add_parser('unmount', help='Unmount from EFS')

    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    # boto3.setup_default_session(profile_name=args.aws_profile)
    # client = boto3.client('efs', region_name=args.region)

    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = easy_path(args.aws_credentials)

    print(get_efs_name(client, "fs-7e55eed7"))
    if vars(args).get('{mount,unmount}') == 'mount':
        mount(args)
    elif vars(args).get('{mount,unmount}') == 'unmount':
        unmount(args)

    if args.test:
        speed_test(args.test, args.efs_mount_point+'/.test-out-file')



if __name__ == "__main__":
    main()




# key for general purpose
# arn:aws:kms:us-west-2:368776568253:key/f835461b-c620-4bf5-801e-990439b6fd68

# max io
# arn:aws:kms:us-west-2:368776568253:key/f835461b-c620-4bf5-801e-990439b6fd68
