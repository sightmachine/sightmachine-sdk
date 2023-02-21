from smsdk import client


# key = 'fe6cd4cd-7735-4634-be0e-ab3d497112b7'
# secret = 'sma_ZByjWtYzIA1wCalTRBDNOBljI9RRYYO7kN5RZOVSVOi_'

# tenant = 'westrock-dallas'
# cli = client.Client(tenant)
# cli.login('apikey', secret_id=secret, key_id=key)
# types = cli.get_machine_type_names()
# print(types)

tenant = "efmw-suzhou"
cli = client.Client(tenant)
cli.login('apikey',
key_id = '2c66709b-a691-4884-bef3-f4a89246faea',
secret_id = 'sma_oxmwHVNSvtpyeScktdeeZaRWgjplLQVazq7VfHjiKBk_')
machine_types = cli.get_machine_type_names()
print(f'Machine Types: {machine_types}')