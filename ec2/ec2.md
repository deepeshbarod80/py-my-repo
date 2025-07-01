
```py

def get_instance_ids():
    instance_ids = []
    response = ec2_client.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_ids.append(instance['InstanceId'])
    return instance_ids

get_instance_ids()
print(get_instance_ids())
```