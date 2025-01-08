。、#!/usr/bin/env bash

# 当发生错误时中止脚本
set -e

# 拉取代码
# git pull

# 输入环境变量
read -p "请输入您要构建的环境变量(staging/prod,默认staging):" env
if [ "$env" == "" ]
  then
    env="staging"
fi

echo $env

read -p "请输入您要上传的服务器别名(默认：azureuser@20.38.36.240):" serverAlias
if [ "$serverAlias" == "" ]
  then
    serverAlias="azureuser@20.38.36.240"
fi

echo $serverAlias

read -p "请输入您要上传的服务器位置(默认：/var/www/):" remoteDir
if [ "$remoteDir" == "" ]
  then
    remoteDir="/var/www/"
fi
echo $remoteDir

read -p "请输入您在远程部署的文件夹名称（默认：e_front）:" deployDir
if [ "$deployDir" == "" ]
  then
    deployDir="e_front"
fi
echo $deployDir

# 编译压缩文件
echo -e "\033[32m 编译压缩文件，生成dist文件夹... \033[0m"

if [ "$env" == "staging" ]
  then
    npm run build:staging
else
    npm run build
fi

# 获取当前目录
path=`pwd`
echo -e "\033[32m 要将"$path"/dist文件夹上传到服务器\033[0m"
echo -e "\033[32m 执行命令scp -P 22222 -r $path/dist $serverAlias:$remoteDir\033[0m"

scp -P 22222 -r $path/dist $serverAlias:$remoteDir

#登录服务器
#####CyQ38NL2Vahg
ssh -p 22222 -Tq ${serverAlias} <<remotessh
rm -rf ${remoteDir}/${deployDir}.bak.*
mv ${remoteDir}/${deployDir} ${remoteDir}/${deployDir}.bak.$(date '+%Y%m%d%H%M%S');
mv ${remoteDir}/dist ${remoteDir}/${deployDir};
exit;
remotessh
