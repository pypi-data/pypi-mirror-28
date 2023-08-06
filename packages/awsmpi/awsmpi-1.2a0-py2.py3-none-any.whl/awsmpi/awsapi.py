#!/usr/bin/env python

from __future__ import print_function
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import time
import boto3
import paramiko


class Client:

    # See: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html
    _placement_group_vm_types = (
        "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "m4.16xlarge",
        "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.12xlarge", "m5.24xlarge",
        "c3.large", "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge",
        "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge", "c4.8xlarge",
        "c5.large", "c5.xlarge", "c5.2xlarge", "c5.4xlarge", "c5.9xlarge", "c5.18xlarge",
        "cc2.8xlarge",
        "r3.large", "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
        "r4.large", "r4.xlarge", "r4.2xlarge", "r4.4xlarge", "r4.8xlarge", "r4.16xlarge",
        "x1.16xlarge", "x1.32xlarge",
        "x1e.xlarge", "x1e.2xlarge", "x1e.4xlarge", "x1e.8xlarge", "x1e.16xlarge", "x1e.32xlarge",
        "cr1.8xlarge",
        "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
        "h1.2xlarge", "h1.4xlarge", "h1.8xlarge", "h1.16xlarge",
        "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge",
        "i3.large", "i3.xlarge", "i3.2xlarge", "i3.4xlarge", "i3.8xlarge", "i3.16xlarge",
        "hs1.8xlarge",
        "f1.2xlarge", "f1.16xlarge",
        "g2.2xlarge", "g2.8xlarge",
        "g3.4xlarge", "g3.8xlarge", "g3.16xlarge",
        "p2.xlarge", "p2.8xlarge", "p2.16xlarge",
        "p3.2xlarge", "p3.8xlarge", "p3.16xlarge")

    # See https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html
    _all_vm_types = (
        "t2.nano", "t2.micro", "t2.small", "t2.medium", "t2.large", "t2.xlarge", "t2.2xlarge", "m3.medium", "m3.large",
        "m3.xlarge", "m3.2xlarge", "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "m4.16xlarge",
        "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "m5.12xlarge", "m5.24xlarge", "c3.large", "c3.xlarge",
        "c3.2xlarge", "c3.4xlarge", "c3.8xlarge", "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge", "c4.8xlarge",
        "c5.large", "c5.xlarge", "c5.2xlarge", "c5.4xlarge", "c5.9xlarge", "c5.18xlarge", "r3.large", "r3.xlarge",
        "r3.2xlarge", "r3.4xlarge", "r3.8xlarge", "r4.large", "r4.xlarge", "r4.2xlarge", "r4.4xlarge", "r4.8xlarge",
        "r4.16xlarge", "x1.16xlarge", "x1.32xlarge", "x1e.xlarge", "x1e.2xlarge", "x1e.4xlarge", "x1e.8xlarge",
        "x1e.16xlarge", "x1e.32xlarge", "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge", "h1.2xlarge",
        "h1.4xlarge", "h1.8xlarge", "h1.16xlarge", "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge", "i3.large",
        "i3.xlarge", "i3.2xlarge", "i3.4xlarge", "i3.8xlarge", "i3.16xlarge", "f1.2xlarge", "f1.16xlarge", "g2.2xlarge",
        "g2.8xlarge", "g3.4xlarge", "g3.8xlarge", "g3.16xlarge", "p2.xlarge", "p2.8xlarge", "p2.16xlarge", "p3.2xlarge",
        "p3.8xlarge", "p3.16xlarge")

    def __init__(self, args):
        # type: (list[str]) -> Client

        self._ec2 = boto3.client("ec2")
        self._args = args       # type: list[str]
        self._username = ""     # type: str
        self._region = ""       # type: str
        self._name = ""         # type: str
        self._fullname = ""     # type: str

        self._aws_vpc_id = ""        # type: str
        self._aws_subnet_id = ""     # type: str
        self._aws_sg_id = ""         # type: str
        self._aws_image_name = ""    # type: str
        self._aws_empty_snap_id = "" # type: str

        # Try to get current username
        try:
            # like "arn:aws-cn:iam::544013047112:user/houwenbin"
            user_arn = boto3.client('sts').get_caller_identity()["Arn"]  # type: str
            self._username = user_arn.split('/')[-1]
            print("Current user: %s" % self._username)
        except NoCredentialsError:
            print("No credentials found. Please run 'aws configure' first.")
            exit(1)
        except ClientError as ex:
            if ex.response["Error"]["Code"] == "InvalidClientTokenId":
                print("Credentials incorrect. Please rerun 'aws configure'. Note that 'region' is also necessary!")
                exit(1)
            raise

        # Try to get current region
        self._region = boto3.session.Session().region_name
        print("Current region: %s" % self._region)

        # Setup _name
        if len(args) > 1:
            self._name = args[1]
            if ' ' in self._name:
                print("Space character is not allowed in cluster name")
                exit(1)
            self._fullname = "%s-%s" % (self._username, self._name)

        # TODO: Currently these values are hard-coded
        self._aws_vpc_id = "vpc-c12ca0a5"
        self._aws_subnet_id = "subnet-38550c4f"
        self._aws_sg_id = "sg-02c68466"
        self._aws_empty_snap_id = "snap-0879d3294d7d8d88b"
        self._aws_image_name = "mpi-template"
        self._aws_public_key_name = "aws-mpi-key"

    def create(self):
        exist_instances = self._find_instances()
        # print(instances)
        if len(exist_instances) > 0:
            print("Cluster %s has already existed!" % self._name)
            return

        use_placement_group = True
        vm_count = int(self._args[2])
        vm_type = self._args[3]
        shared_volume = int(self._args[4])
        print("Try to create %d nodes (%s) with /share = %d GB" % (vm_count, vm_type, shared_volume))

        assert vm_count > 0
        assert shared_volume >= 4
        if vm_type not in Client._all_vm_types:
            print("%s is not a valid instance type!" % vm_type)
            exit(1)
        elif vm_type not in Client._placement_group_vm_types:
            use_placement_group = False
            print("Placement group is not supported in %s instances!" % vm_type)

        # Compute shared volume per node
        shared_volume_per_node = int(shared_volume / vm_count) + 1
        if shared_volume_per_node < 4:
            shared_volume_per_node = 4

        ami_info = self._ec2.describe_images(
            Owners=["self"],
            Filters=[{"Name": "tag:Name", "Values": [self._aws_image_name]}]
        )["Images"][0]
        image_id = ami_info["ImageId"]
        root_snap_id = ami_info["BlockDeviceMappings"][0]["Ebs"]["SnapshotId"]
        print("Using image: %s, root snapshot: %s" % (image_id, root_snap_id))

        # Create placement group if available
        if use_placement_group:
            try:
                self._ec2.create_placement_group(GroupName=self._fullname, Strategy='cluster')
            except ClientError as ex:
                if "InvalidPlacementGroup.Duplicate" not in str(ex):
                    raise

        # Prepares arguments
        create_instance_args = dict(
            BlockDeviceMappings=[
                {
                    'DeviceName': "/dev/sda1",
                    # 'VirtualName': 'string',
                    'Ebs': {
                        # 'Encrypted': False,
                        'DeleteOnTermination': True,
                        # 'Iops': 123,
                        # 'KmsKeyId': 'string',
                        'SnapshotId': root_snap_id,
                        'VolumeSize': 20 + shared_volume_per_node,
                        'VolumeType': 'gp2'  # 'standard' | 'io1' | 'gp2' | 'sc1' | 'st1'
                    },
                    # 'NoDevice': 'string'
                }
            ],
            ImageId=image_id,
            InstanceType=vm_type,
            # Ipv6AddressCount=123,
            # Ipv6Addresses=[{
            #     'Ipv6Address': 'string'
            # }],
            # KernelId='string',
            KeyName=self._aws_public_key_name,
            MaxCount=vm_count,
            MinCount=vm_count,
            Monitoring={
                'Enabled': False
            },
            # Placement=...,  # set later
            # RamdiskId='string',
            # SecurityGroupIds=[_id_sg],
            # SecurityGroups=['string', ],
            # SubnetId=_id_subnet,
            # UserData='string',
            # AdditionalInfo='string',
            # ClientToken=name,
            DisableApiTermination=False,
            DryRun=False,
            # EbsOptimized=False,  # TODO: leave it default?
            # IamInstanceProfile={
            #     'Arn': 'string',
            #     'Name': 'string'
            # },
            InstanceInitiatedShutdownBehavior='stop',  # 'stop' | 'terminate',
            NetworkInterfaces=[{
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                # 'Description': 'string',
                'DeviceIndex': 0,
                'Groups': [
                    self._aws_sg_id,
                ],
                # 'Ipv6AddressCount': 123,
                # 'Ipv6Addresses': [{
                #     'Ipv6Address': 'string'
                # }, ],
                # 'NetworkInterfaceId': 'string',
                # 'PrivateIpAddress': 'string',
                # 'PrivateIpAddresses': [{
                #     'Primary': True|False,
                #     'PrivateIpAddress': 'string'
                # }, ],
                # 'SecondaryPrivateIpAddressCount': 123,
                'SubnetId': self._aws_subnet_id
            }],
            # PrivateIpAddress='string',
            # ElasticGpuSpecification=[{
            #     'Type': 'string'
            # }, ],
            TagSpecifications=[{
                'ResourceType': 'instance',  # 'customer-gateway'|'dhcp-options'|'image'|'instance'|'internet-gateway'|'network-acl'|'network-interface'|'reserved-instances'|'route-table'|'snapshot'|'spot-instances-request'|'subnet'|'security-group'|'volume'|'vpc'|'vpn-connection'|'vpn-gateway',
                'Tags': [
                    {
                        "Key": "Group",
                        "Value": self._fullname,
                    }
                ]
            }],
            # LaunchTemplate={
            #     'LaunchTemplateId': 'string',
            #     'LaunchTemplateName': 'string',
            #     'Version': 'string'
            # },
            # InstanceMarketOptions={
            #     'MarketType': 'spot',
            #     'SpotOptions': {
            #         'MaxPrice': 'string',
            #         'SpotInstanceType': 'one-time'|'persistent',
            #         'BlockDurationMinutes': 123,
            #         'ValidUntil': datetime(2015, 1, 1),
            #         'InstanceInterruptionBehavior': 'hibernate'|'stop'|'terminate'
            #     }
            # },
            # CreditSpecification={
            #     'CpuCredits': 'string'
            # }
        )

        if use_placement_group:
            create_instance_args["Placement"] = {
                # 'AvailabilityZone': 'string',
                # 'Affinity': 'string',
                'GroupName': self._fullname,
                # 'HostId': 'string',
                'Tenancy': 'default'  # 'default' | 'dedicated' | 'host',
                # 'SpreadDomain': 'string'
            }

        # Create the instances
        instances = (self._ec2.run_instances(**create_instance_args))["Instances"]
        # print(instances)

        # Set node names individually
        for idx in range(0, len(instances)):
            instance_name = "%s-%d" % (self._fullname, idx + 1)
            instance_id = instances[idx]["InstanceId"]
            self._ec2.create_tags(
                DryRun=False,
                Resources=[instance_id],
                Tags=[{
                    'Key': 'Name',
                    'Value': instance_name
                }]
            )

        # Wait for all instances to be ready
        print("Waiting all instances to be running...")
        ec2 = boto3.resource('ec2')
        for idx in range(0, len(instances)):
            instance_id = instances[idx]["InstanceId"]
            instance = ec2.Instance(instance_id)
            instance.wait_until_running()

        # Allocate elastic IP & attach to master node
        master_instance_id = instances[0]["InstanceId"]
        master_public_ip = self._ec2.allocate_address(
            Domain='standard',
            # Address='string',
            DryRun=False)["PublicIp"]
        self._ec2.associate_address(
            # AllocationId='string',
            InstanceId=master_instance_id,
            PublicIp=master_public_ip,
            AllowReassociation=True,
            DryRun=False,
            # NetworkInterfaceId='string',
            # PrivateIpAddress='string'
        )

        for idx in range(0, len(instances)):
            instance_name = "%s-%d" % (self._name, idx + 1)
            instance_id = instances[idx]["InstanceId"]
            if instance_id == master_instance_id:
                print("%s: (%s) (master: %s)" % (instance_name, instance_id, master_public_ip))
            else:
                print("%s: (%s)" % (instance_name, instance_id))

        print("Connecting to cluster...")
        time.sleep(3)
        for retry in range(0, 5):
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(master_public_ip, 22, "ubuntu", "ubuntu", timeout=10)
                break
            except:
                continue

        print("Initializing the cluster...")
        # /opt/awsmpi/master.py <name> <count> <ip1> ... <ipN>
        ssh_args = [self._name, vm_count] + list(map(lambda ins: ins["PrivateIpAddress"], instances))
        ssh_cmd = ("/opt/awsmpi/master.sh" + " %s" * len(ssh_args)) % tuple(ssh_args)
        # print(ssh_cmd)
        stdin, stdout, stderr = ssh.exec_command(ssh_cmd)
        # print("==== stdout ====")
        # for line in stdout.readlines(): print(line, end='')
        # print("==== stderr ====")
        # for line in stderr.readlines(): print(line, end='')
        ssh.close()

        print("Done. Use 'ssh ubuntu@%s' (password: ubuntu) to login now!" % master_public_ip)

    def _find_instances(self):
        try:
            # print(self._fullname)
            reservations = self._ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'tag:Group',
                        'Values': [self._fullname]
                    },
                ],
                # InstanceIds=[
                #     'string',
                # ],
                DryRun=False,
                # MaxResults=1000,
                # NextToken='string'
            )["Reservations"]
            instances = []
            for reservation in reservations:
                instances += reservation["Instances"]
        except IndexError:
            return []

        real_instances = []
        for instance in instances:
            if instance["State"]["Name"] != "terminated":
                real_instances.append(instance)

        return real_instances

    def terminate(self):
        instances = self._find_instances()
        # print(instances)
        if len(instances) == 0:
            print("Cluster %s does not exist!" % self._name)
            return

        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = list(filter(lambda kv: kv["Key"] == "Name", instance["Tags"]))[0]["Value"] # type: str
            instance_name = instance_name[len(self._username)+1:]

            # Deallocate elastic IP if associated
            if "PublicIpAddress" in instance and instance_name.endswith("-1"):
                public_ip = instance["PublicIpAddress"]
                print("Terminating %s (%s). Release IP %s" % (instance_name, instance_id, public_ip))
                alloc_id = self._ec2.describe_addresses(PublicIps=[public_ip])["Addresses"][0]["AllocationId"]
                self._ec2.disassociate_address(PublicIp=public_ip)
                self._ec2.release_address(AllocationId=alloc_id)
            else:
                print("Terminating %s (%s)" % (instance_name, instance_id))

            self._ec2.terminate_instances(
                InstanceIds=[instance_id],
                DryRun=False)

        # Wait for all instance to be terminated
        print("Waiting all instances to be terminated...")
        ec2 = boto3.resource("ec2")
        for instance in instances:
            instance_id = instance["InstanceId"]
            ec2.Instance(instance_id).wait_until_terminated()

    def start(self):
        instances = self._find_instances()
        # print(instances)
        if len(instances) == 0:
            print("Cluster %s does not exist!" % self._name)
            return

        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = list(filter(lambda kv: kv["Key"] == "Name", instance["Tags"]))[0]["Value"]
            instance_name = instance_name[len(self._username)+1:]

            print("Starting %s (%s)" % (instance_name, instance_id))
            self._ec2.start_instances(InstanceIds=[instance_id])

        # Wait for all instance to be running
        print("Waiting all instances to be running...")
        ec2 = boto3.resource("ec2")
        for instance in instances:
            instance_id = instance["InstanceId"]
            ec2.Instance(instance_id).wait_until_running()

    def stop(self):
        instances = self._find_instances()
        # print(instances)
        if len(instances) == 0:
            print("Cluster %s does not exist!" % self._name)
            return

        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = list(filter(lambda kv: kv["Key"] == "Name", instance["Tags"]))[0]["Value"]
            instance_name = instance_name[len(self._username)+1:]

            print("Stopping %s (%s)" % (instance_name, instance_id))
            self._ec2.stop_instances(InstanceIds=[instance_id])

        # Wait for all instance to be running
        print("Waiting all instances to be stopped...")
        ec2 = boto3.resource("ec2")
        for instance in instances:
            instance_id = instance["InstanceId"]
            ec2.Instance(instance_id).wait_until_stopped()

    def describe(self):
        instances = self._find_instances()
        # print(instances)
        if len(instances) == 0:
            print("Cluster %s does not exist!" % self._name)
            return

        print("\nCluster %s information:" % self._fullname)
        for instance in instances:
            instance_id = instance["InstanceId"]
            instance_name = list(filter(lambda kv: kv["Key"] == "Name", instance["Tags"]))[0]["Value"]  # type: str
            instance_state = instance["State"]["Name"]

            instance_name = instance_name[len(self._username)+1:]
            if instance_name.endswith("-1"):
                print("Node %s: %s (master: %s)" % (instance_name, instance_state, instance["PublicIpAddress"]))
            else:
                print("Node %s: %s" % (instance_name, instance_state))
