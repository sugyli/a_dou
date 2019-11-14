#!/bin/bash
id=`ps -ef | grep "spiderkeeper" | grep -v grep | awk '{print $2}'`
if [ "${id}" != "" ];then
    cpulimit -p ${id} -l 40
fi
