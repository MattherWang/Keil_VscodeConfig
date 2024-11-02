import os
import json
import xml.etree.ElementTree as ET

# 获取当前工作目录
current_directory = os.getcwd()
# print(current_directory)
directory_name = os.path.basename(current_directory)
# print(directory_name)

# 搜索 .uvprojx 文件
search_path = os.path.join(current_directory, 'MDK-ARM')
# print(search_path)
for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('.uvprojx'):
            file_name = os.path.join(root, file)
            # print(file_name)
            break

# print(file_name)


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

# 添加头文件路径
configurations_dict['includePath'] = includes_list

# 添加宏定义
configurations_dict['defines'] = defines_list                                           # 添加宏定义                             

# 添加C标准
configurations_dict['cStandard'] = 'gnu99'

# 添加intellisense模式
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

print('Generate c_cpp_properties.json successfully!')

# 生成 settings.json 文件
settings_dict = {}
settings_dict['editor.tabSize'] = 2

# 写入 settings.json 文件
settings_file_path = os.path.join(new_directory,'settings.json')
os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)  # 确保 .vscode 目录存在
with open(settings_file_path, 'w') as settings_file:
    json.dump(settings_dict, settings_file, indent=4)

print('Generate settings.json successfully!')
    