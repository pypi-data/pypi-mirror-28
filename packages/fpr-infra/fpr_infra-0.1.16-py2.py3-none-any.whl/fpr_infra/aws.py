# coding: utf-8

import boto3
import time


class Image:
    def __init__(self, image):
        self.image = image

    @property
    def id(self):
        return self.image['ImageId']

    @property
    def name(self):
        return self.image['Name']


class EC2:
    client = boto3.client('ec2')
    resource = boto3.resource('ec2')

    subnet = list(resource.subnets.all())[0]
    security_groups = [
        'sg-4ed6492b',
        'sg-7b7ee61e',
        'sg-0bcb9f6e',
    ]

    @classmethod
    def create_instance(cls, *, id=None, pattern=None, name=None, type='t2.nano', **kwargs):

        if id is None:
            if pattern is None:
                raise ValueError("pattern must be defined if id isn't")

            images = cls.client.describe_images(Filters=[{'Name': 'name', 'Values': [pattern]}],
                                                Owners=['760589174259'])
            image = Image(images['Images'][0])
            id = image.id
            if name is None:
                name = image.name

        kwargs.setdefault("MinCount", 1)
        kwargs.setdefault("MaxCount", 1)

        cls.resource.Image(id).wait_until_exists()

        instances = cls.resource.create_instances(
            ImageId=id,
            InstanceType=type,
            KeyName='fpr',
            Placement={
                'AvailabilityZone': cls.subnet.availability_zone,
            },
            SecurityGroupIds=cls.security_groups,
            SubnetId=cls.subnet.id,
            **kwargs
        )

        try:
            assert len(instances) == 1
            instance = instances[0]
            instance.create_tags(
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ]
            )
            return instance
        except:
            for inst in instances:
                inst.terminate()
            raise

    @classmethod
    def create_ebs(cls, id, instance, name=None, desc=None):

        # Creates snapshot
        desc = desc or f"snapshot from {id}"
        snap = cls.client.create_snapshot(
            Description=desc,
            VolumeId=id,
        )
        snap = cls.resource.Snapshot(snap['SnapshotId'])
        snap.wait_until_completed()

        # Creates volume
        tags = [{'Key': 'Name', 'Value': name}] if name else []
        vol = cls.client.create_volume(
            AvailabilityZone=instance.subnet.availability_zone,
            Encrypted=False,
            Size=snap.volume_size,
            SnapshotId=snap.snapshot_id,
            VolumeType='gp2',
            TagSpecifications=[{
                'ResourceType': 'volume',
                'Tags': tags,
            }],
        )

        # Attaches volume to instance
        vol = cls.resource.Volume(vol['VolumeId'])
        count = 0
        while vol.state != 'available':
            count += 1
            if count > 10:
                raise TimeoutError()
            time.sleep(2)
            vol = cls.resource.Volume(vol.volume_id)

        vol.attach_to_instance(
            Device='xvdf',
            InstanceId=instance.id,
        )
        snap.delete()
        return vol
