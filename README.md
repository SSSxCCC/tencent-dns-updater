# 腾讯云域名ip更新器

自动更新腾讯云域名的ip的python脚本。

## 使用方式

1. 购买[腾讯云域名][https://buy.cloud.tencent.com/domain]
2. 打开[云解析DNS][https://console.cloud.tencent.com/cns]，在你的域名中添加一条记录
3. 安装[python][https://www.python.org/]
4. 安装[tencentcloud-sdk-python][https://github.com/TencentCloud/tencentcloud-sdk-python]，并获取安全凭证SecretID和SecretKey
5. 下载本仓库源码：
```
git clone https://github.com/SSSxCCC/tencent-dns-updater
```
6. 修改脚本tencent_dns_updater.py中的配置：
```python
# 脚本配置
secret_id = 'todo' # 改成你的SecretID
secret_key = 'todo' # 改成你的SecretKey
domain = 'todo' # 改成你的域名，例如domain.com
region = 'ap-guangzhou'
update_interval = 3600 # 更新的时间间隔，默认是3600秒也就是1小时

# 记录参数匹配，为None则不匹配这一项
record_id = None # 改成你的记录id或None
record_type = 'A' # 改成你的记录类型或None
sub_domain = '@' # 改成你的域名前缀或None
```
7. 执行脚本：
```
cd tencent-dns-updater
python .\tencent_dns_updater.py
```
