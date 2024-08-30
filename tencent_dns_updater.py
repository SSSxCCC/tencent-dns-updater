import time
import requests
from tencentcloud.common import credential
from tencentcloud.dnspod.v20210323 import dnspod_client, models

# configurations
secret_id = 'todo'
secret_key = 'todo'
domain = 'todo'
region = 'ap-guangzhou'
update_interval = 3600

# update only records that match these parameters
record_id = None
record_type = 'A'
sub_domain = '@'

def get_external_ip() -> str:
    proxies = {
        "http": None,
        "https": None,
    }
    ip = requests.get('https://ident.me', proxies=proxies).text.strip()
    return ip

cred = credential.Credential(secret_id, secret_key)
client = dnspod_client.DnspodClient(cred, region)

def get_record_list() -> list[models.RecordListItem]:
    request = models.DescribeRecordListRequest()
    request.Domain = domain

    response = client.DescribeRecordList(request)
    return response.RecordList

def modify_record(record: models.RecordListItem, ip: str):
    request = models.ModifyRecordRequest()
    request.Domain = domain
    request.RecordType = record.Type
    request.RecordLine = record.Line
    request.Value = ip
    request.RecordId = record.RecordId
    request.SubDomain = record.Name

    client.ModifyRecord(request)

update_time = time.time()

while True:
    now_time = time.time()
    if now_time >= update_time:
        update_time += update_interval
        print('----- Update ----- ' + time.strftime("%Y-%m-%d %H:%M:%S"))

        try:
            ip = get_external_ip()
            print('get_external_ip: ' + ip)
        except Exception as e:
            print('get_external_ip error: ' + repr(e))
            continue

        try:
            records = [r for r in get_record_list() if # update only records that match these parameters
                (record_id is None or record_id == r.RecordId) and
                (record_type is None or record_type == r.Type) and
                (sub_domain is None or sub_domain == r.Name)]
            print('get_record_list:')
            for record in records:
                print(record)
        except Exception as e:
            print('get_record_list error: ' + repr(e))
            continue

        for record in [r for r in records if ip != r.Value]: # only update when ip changes
            try:
                modify_record(record, ip)
                print('modify_record: ' + str(record.RecordId))
            except Exception as e:
                print('modify_record error: ' + repr(e))
    else:
        time.sleep(update_time - now_time)
