# TG2CF Converts Micro Focus OM template groups to configuration folders
# Copyright (C) 2020 Whitlock Infrastructure Solutions
# https://whitlockis.com 
#
# This program is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published by 
# the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import io, sys, os
import subprocess
from subprocess import call
import logging
import argparse
import re
import datetime
import uuid

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--policy_group', required=False)
args = parser.parse_args()
if args.policy_group != None:
    top_level = args.policy_group
else:
    top_level = '1f8c168f-6cbb-2b1a-8f92-51ff58ab8250'  #ID of top level template group

session_id = uuid.uuid1()
logging.basicConfig(filename='E:/TG2CF/TG2CF.log', level=logging.INFO) #Update path to log file

aspect_path='E:/TG2CF/aspects'
exclude = []

def loggy(message):
    dt = str(datetime.datetime.now())
    logging.info(dt+ ' '+ str(message))
    print(f'{dt} {session_id} '+ str(message))

base_cmd = 'C:/HPBSM/opr/bin/opr-config-tool -user admin -pw OMI4fun!' #Update path. Be mindful of the slashes

def getTemplateGroups(tg_id):
    parsed_list = {}
    cmd_args = f' -lc -t tg -wp -parent_type template_group -pid {tg_id}'
    full_cmd = base_cmd + cmd_args
    #print(full_cmd)
    tmp_list = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    #print(tmp_list)
    for match in re.finditer(r"""["']([\w\s]+)['"]:?\s?'?(?:\d+\.\d+)?\s([\w\d-]+)""", tmp_list):
        parsed_list[match.group(1)] = match.group(2)
    #print('Total groups: ' + str(len(parsed_list)))
    loggy('Total groups: ' + str(len(parsed_list)))
    return parsed_list

def fetchTemplates(tg_id):
    parsed_list = {}
    cmd_args = f' -lc -t t -wp -parent_type template_group -pid {tg_id}'
    full_cmd = base_cmd + cmd_args
    tmp_list = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    for match in re.finditer(r"""["']([\w\s]+)['"]:?\s?'?(?:\d+\.\d+)?\s([\w\d-]+)""", tmp_list):
        parsed_list[match.group(1)] = match.group(2)
    #print('Total policies: ' + str(len(parsed_list)))
    loggy('Total policies: ' + str(len(parsed_list)))
    return parsed_list

def buildCF(path):
    loggy(f'building {path}')
    cmd_args = f' -c -t cf -n "{path}"'
    full_cmd = base_cmd + cmd_args
    tmp_out = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')

#Only configured for three levels. 
def processGroups(list):
    for name, id in list.items():
        if name not in exclude:
            path1 = f'/Migrated/{name}' #Set this to the desired root configuration folder (Under Configuration Folders)
            buildCF(path1)
            level2 = getTemplateGroups(f'"{id}"') 
            #print(f'Total groups under {name}: ' + str(len(level2)))
            loggy(f'Total groups under {name}: ' + str(len(level2)))
            tmp_list2 = fetchTemplates(f'"{id}"')
            loggy(tmp_list2)
            lvl2_dict = {}
            lvl2_dict[name] = tmp_list2
            buildAspect(lvl2_dict, path1)
            if len(level2) > 0:
                for name2, id2 in level2.items():
                    path2 = path1 + f'/{name2}'
                    buildCF(path2)
                    level3 = getTemplateGroups(f'"{id2}"')
                    #print(f'Total groups under {name2}: ' + str(len(level3)))
                    loggy(f'Total groups under {name2}: ' + str(len(level3)))
                    tmp_list3 = fetchTemplates(f'"{id2}"')
                    lvl3_dict = {}
                    loggy(tmp_list3)
                    lvl3_dict[name2] = tmp_list3
                    buildAspect(lvl3_dict, path2)
                    if len(level3) > 0:
                        for name3, id3 in level3.items():
                            path3 = path2 + f'/{name3}'
                            buildCF(path3)
                            level4 = getTemplateGroups(f'"{id3}"')
                            #print(f'Total groups under {name3}: ' + str(len(level4)))
                            loggy(f'Total groups under {name3}: ' + str(len(level4)))
                            tmp_list4 = fetchTemplates(f'"{id3}"') 
                            lvl4_dict = {}
                            lvl4_dict[name3] = tmp_list4
                            buildAspect(lvl4_dict, path3)
                    
def buildAspect(parts, path):
    for group, tmpls in parts.items():
        if group not in exclude:
            file_group = group.replace(' ','_')
            loggy(f'Building aspect {group}')
            #print(f'Building aspect {group}')
            cmd_args = f' -c -t a -n "{group}" -o {aspect_path}/{file_group}.xml'
            full_cmd = base_cmd + cmd_args
            tmp_out = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            for name, id in tmpls.items():
                loggy(f'Adding {name} to {group}')
                cmd_args2 = f' -cc -t t -n "{name}" -i {aspect_path}/{file_group}.xml -o'
                full_cmd2 = base_cmd + cmd_args2
                tmp_out2 = subprocess.check_output(full_cmd2, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            cmd_args3 = f' -ud -i {aspect_path}/{file_group}.xml'
            loggy(f'uploading {group}')
            full_cmd3 = base_cmd + cmd_args3
            tmp_out3 = subprocess.check_output(full_cmd3, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            cmd_args4 = f' -cc -pt cf -pn "{path}" -t a -n "{group}"'
            loggy(f'moving {group} to {path}')
            full_cmd4 = base_cmd + cmd_args4
            tmp_out4 = subprocess.check_output(full_cmd4, shell=True, stderr=subprocess.STDOUT).decode('utf-8')

if __name__ == "__main__":
    loggy('Starting TG2CF')
    topLevel = getTemplateGroups(top_level)
    loggy(topLevel)
    #print(topLevel)
    processGroups(topLevel)
    loggy('TG2CF End' + os.linesep)