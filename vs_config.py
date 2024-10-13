import os
import json
import xml.etree.ElementTree as ET

# 获取当前工作目录
current_directory = os.getcwd()
directory_name = os.path.basename(current_directory)
print(directory_name)
file_name = 'MDK-ARM/' + directory_name + '.uvprojx'


# 解析 XML 文件
tree = ET.parse(file_name)
root = tree.getroot()

# print(root.findall('SchemaVersion')[0].text)
# print(root.findall('Header')[0].text)

# 找到定义的宏和包含头文件
defines = root.findall('Targets')[0].findall('Target')[0].findall('TargetOption')[0].findall('TargetArmAds')[0].findall('Cads')[0].findall('VariousControls')[0].findall('Define')[0].text
includes = root.findall('Targets')[0].findall('Target')[0].findall('TargetOption')[0].findall('TargetArmAds')[0].findall('Cads')[0].findall('VariousControls')[0].findall('IncludePath')[0].text

# print(defines)
# print(includes)

includes = includes.replace('..', '${workspace}')
defines_list = defines.split(',')
includes_list = includes.split(';')

# print(defines_list)
# print(includes_list)

dict_path = {}
configurations = []
configurations_dict = {}
configurations_dict['name'] = 'ARM'
configurations_dict['compilerPath'] = 'C:/Keil_v5/ARM/ARMCC/bin/armcc'

configurations_dict['includePath'] = includes_list
configurations_dict['includePath'].append("C:/Keil_v5/ARM/ARMCC/include")
configurations_dict['includePath'].append("C:/Keil_v5/ARM/ARMCC/include/rw")

configurations_dict['defines'] = defines_list
configurations_dict['defines'].append("__ARMCC_VERSION")

configurations_dict['cStandard'] = 'gnu99'

configurations_dict['intelliSenseMode'] = 'clang-arm'

configurations.append(configurations_dict)
dict_path['configurations'] = configurations
dict_path['version'] = 4

# 创建一个目录 .vscode
new_directory = '.vscode'
os.makedirs(new_directory, exist_ok=True)  # 使用 makedirs，可以创建多级目录

# 将结果写入 JSON 文件
json_file_path = os.path.join(new_directory, 'c_cpp_properties.json')
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)  # 确保 .vscode 目录存在
with open(json_file_path, 'w') as json_file:
    json.dump(dict_path, json_file, indent=4)

print('Configuration Done!')