from io import TextIOWrapper
import os
import sys
from typing import List
import json

statisticFile = 'statistic.json'

def simplePath(one, two) -> str: 
  return os.path.normpath(os.path.join(one, two))

# 处理json文件
def openJson(path: str, handleFile):
  if os.path.exists(path) and path.endswith('.json'):
    with open(path, encoding='utf-8') as file:
      handleFile(file)
  else:
    print(f"{path} not json file or not exists")

def handleStatisticFile(folder: str, handler):
  if not os.path.exists(folder) :
    pass
  else:
    with open(folder + '/' + statisticFile, encoding='utf-8') as file:
      handler(file)

# 获取文件夹的所有文件
def getFilesOfFolder(folder: str):
  if os.path.exists(folder) and os.path.isdir(folder):
    files = os.listdir(folder)
    return list(map(lambda file: simplePath(folder, file), files))
    # return list(map(lambda file: f"{folder}/{file}", files))
  else:
    print(f'{folder} is a file' if os.path.exists(folder) else f"{folder} not exists" )
    return []

poetryFolder = 'D:/workspace/chinese-poetry/'
tangPoetry = 'quan_tang_shi'

# 获取poetry类型的所有文件
def getFilesOfPoetry(poetry) -> List :
  return getFilesOfFolder(f"{getFolderOfPoetry(poetry)}/json")

# 获取poetry对应的文件夹
def getFolderOfPoetry(poetry) -> str : 
  return simplePath(simplePath(sys.path[0], poetryFolder), poetry)

def handleTangsPoetry(file: TextIOWrapper):
  jsonContent = json.load(file)
  print(f"{file.name} has {len(jsonContent)} poetries")
  
def poetrySizeOfOneTangsPoetry(file: TextIOWrapper) -> int :
  return len(json.load(file))


class FileMeta:
  def __init__(self, size: int, name: str) -> None:
    self.size = size
    self.name = name

class TangsStatistic:
  def __init__(self, total, fileMetas: List[FileMeta]) -> None:
    self.total = total
    self.fileMetas = fileMetas

  def __str__(self) -> str:
    res = f"total:{self.total} - file meta : size {len(self.fileMetas)} \n"
    for meta in self.fileMetas:
      res += f"{meta.name} - {meta.size} \n"
    return res   

def allSizesOfPoetry(poetry: str) -> List:
  tangs = getFilesOfPoetry(poetry)
  for tang in tangs:
    with open(tang, encoding='utf-8') as file :
      yield poetrySizeOfOneTangsPoetry(file)

def doStatisticsForTangs() -> FileMeta:
  tangs = getFilesOfPoetry(tangPoetry)
  total = 0
  fileMetas = []
  result = TangsStatistic(total, fileMetas)
  def handleOneFile(file: TextIOWrapper):
    content = json.load(file)
    result.total += len(content)
    fileMetas.append(FileMeta(len(content), file.name))
  for tang in tangs:
    openJson(tang, handleOneFile)
  return result
  
class JsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, TangsStatistic):
      fileMetas = []
      for meta in obj.fileMetas:
        fileMetas.append(self.default(meta))
      return {'total': obj.total, 'fileMetas': fileMetas}
    elif isinstance(obj, FileMeta):
      return {'size': obj.size, 'name': obj.name}
    else :
      return super(JsonEncoder, self).default(obj)

def writeToStatistic(poetry: str, content) -> None:
  folder = getFolderOfPoetry(poetry)
  fileName = simplePath(folder, statisticFile)
  if os.path.exists(fileName):
    print(f"{fileName} exists")
  else:
    jsonContent = json.dumps(content, cls=JsonEncoder, indent=2)
    with open(fileName,mode='x', encoding='utf-8') as file:
      file.write(jsonContent)

if __name__ == '__main__':
  # tangs = getFilesOfPoetry(tangPoetry)
  # if len(tangs) > 0:
  #   for file in tangs:
  #     openJson(file, handleTangsPoetry
  ans = doStatisticsForTangs()
  print(ans)
  # res = json.dumps(ans, cls=JsonEncoder, indent=2)
  writeToStatistic(tangPoetry, ans)
  # print(getFolderOfPoetry(tangPoetry))
