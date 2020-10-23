**TG2CF** is a python3 script that reads template groups and creates the same structure in the “Management Templates/Aspects” section of “Monitoring” in OBM/OMi. Additionally, the script will read the policies in the template groups and bundle them into an aspect and then copy that aspect into the related configuration folder.

This can be the most work for a legacy OM upgrade, and while Monitoring Automation dictates a new thought process around policy grouping, sometimes, one needs to forklift in the legacy structure and deploy “as-is”

Instructions are for Windows, but should work with Linux/Unix by changing the paths accordingly.

![](https://github.com/WhitlockIS/Scripts/blob/master/Micro%20Focus/TG2CF/images/tg2cf_image1.png)

**Instructions for use:**

1. Ensure you have credentials to a user with admin access to the CLI
2. Obtain the template group ID. Navigate to Administration > Monitoring > Policy Templates and right click on the template group you want to convert. Copy the ID for use in the script.
![](https://github.com/WhitlockIS/Scripts/blob/master/Micro%20Focus/TG2CF/images/tg2cf_image2.png)
3. Create a directory for the log and temporary files. For example: E:/TG2CF
4. Update the code near the top with the directory you just created:
```python
logging.basicConfig(filename='E:/TG2CF/TG2CF.log', level=logging.INFO) #Update path to log file


aspect_path='E:/TG2CF/aspects'
```
5. Update "base_cmd" to the correct path for your system. Update the username and password as well. Ensure the slashes in the path are "/" not "\"
6. Update "path1" with the desired root configuration folder. This folder will appear under "Configuration Folders"
```python
def processGroups(list):
    for name, id in list.items():
        if name not in exclude:
            path1 = f'/Migrated/{name}'
```
7. Update "top_level" with the copied template group ID, or use the ID in the command execution.
```python
if args.policy_group != None:
    top_level = args.policy_group
else:
    top_level = '1f8c168f-6cbb-2b1a-8f92-51ff58ab8250'
```
or
`>python tg2cf.py -p <ID>`
