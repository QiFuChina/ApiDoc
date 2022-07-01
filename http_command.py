# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:34:50 2022

@author: admin
"""
import queue
import uuid
import os,subprocess
from fastapi import FastAPI, Path, Query,Body
from pydantic import BaseModel,Field,HttpUrl
from typing import Union
app = FastAPI()

mock_dict={'mock':'E:/ResourceCode/MockingBird/gen_voice.py'
          ,'--input_txt':''
          ,'--input_wav':''
          ,'--synthesizer_path':'F:/Test/mock/input/sample01.pt'
          ,'--output_wav':'F:/Test/mock/output/svdsf.wav'
          }
rvm_dict={'rvm':'E:/ResourceCode/RobustVideoMatting/inference.py'
          ,'--input-source':'F:/Test/rvm/input/input.mp4'
          ,'--output-composition':'F:/Test/rvm/output/dfbbbbbd.mp4'
          }
lip_dict={'lip':'E:/ResourceCode/Wav2Lip/inference.py'
          ,'--face':rvm_dict['--output-composition']
          ,'--audio':mock_dict['--output_wav']
          ,'--outfile':'--outfile F:/Test/lip/results/test/result.mp4'
          }

api_dict={'mock':mock_dict
          ,'rvm':rvm_dict
          ,'lip':lip_dict
          }



#http下需要的结构参数
class Api(BaseModel):
    mock_input_txt:str = ' '
    mock_input_wav:str = ' '
    mock_synthesizer_path:str = ' '
    mock_output_wav:str = ' '
    rvm_input_source:str = ' '
    rvm_output_composition:str = ' '
    lip_outfile:str = ' '


@app.post("/api/")
#http接收修改的方法参数，更新字典内的值
def api_dict_update(api:Api= Body(embed=True)):
    mock_dict['--input_txt']=api.mock_input_txt
    mock_dict['--input_wav']=api.mock_input_wav
    mock_dict['--synthesizer_path']=api.mock_synthesizer_path
    mock_dict['--output_wav']=api.mock_output_wav
    rvm_dict['--input-source']=api.rvm_input_source
    rvm_dict['--output-composition']=api.rvm_output_composition
    lip_dict['--outfile']=api.lip_outfile
    api_command()
    pass
    
@app.get("/api/")
#http接收修改的方法参数，更新字典内的值
def api_dict_update(input_txt:str,
                    input_wav:str,
                    synthesizer_path:str,
                    output_wav:str,
                    input_source:str,
                    output_composition:str,
                    outfile:Union[str, None] = None):
    mock_dict['--input_txt']=input_txt
    mock_dict['--input_wav']=input_wav
    mock_dict['--synthesizer_path']=synthesizer_path
    mock_dict['--output_wav']=output_wav
    rvm_dict['--input-source']=input_source
    rvm_dict['--output-composition']=output_composition
    lip_dict['--outfile']=outfile
    api_command()
    pass 

#本地接收修改的方法参数，更新字典内的值
def api_dict_update(args1,args2,args3,args4,args5,args6):
    mock_dict['--input_txt']=args1
    mock_dict['--input_wav']=args2
    mock_dict['--output_wav']=args3
    rvm_dict['--input-source']=args4
    rvm_dict['--output-composition']=args5
    lip_dict['--outfile']=args6
    api_command()
    pass

#单个任务的信息
class task_info:
    def __init__(self,uuid,cmd,status):
        self.uuid=uuid
        self.cmd=cmd
        self.status=status
        
all_task_list=[]        
#获取更新后的字典值，并转化为外部执行命令
def api_command():
    task_list=[]
    for key,value in api_dict.items():
        api_cmd=''
       
        for k,v in value.items():
            if v=='':
                continue
            api_cmd=api_cmd+k+'  '+v+' '
        api_cmd=api_cmd.split(' ',maxsplit=1)
        #print('conda activate {} && python {}'.format(api_cmd[0], api_cmd[1]))
        id=get_uuid()
        cmd='conda activate {} && python {}'.format(api_cmd[0], api_cmd[1])
        sta=None
        task_list.append(task_info(id,cmd,sta))
        print(len(task_list))
        
    all_task_list_append(task_list)
    show_task_info()
    #execute_task(0)
    return


#将三个执行语句整合成一个列表对象，存入总任务列表中
def all_task_list_append(list):
    all_task_list.append(list)
    print('update task_list')
    
    
    
#输出所有任务的信息
def show_task_info():
    #print(all_task_list[0])
    for task in all_task_list:
        for task_info in task:
            print(task_info.uuid)
            print(task_info.cmd)
            print(task_info.status)
        #print(task)
        '''
        
        '''
        
    pass

#执行对应任务，目前在添加到任务列表后自动调用，并根据外部程序执行结果修改执行状态；后续可能修改为被用户自主调用
def execute_task(i):
    for task in all_task_list[i]:
        print(task.uuid)
        task.status="*"
        q=subprocess.Popen(task.cmd,shell=True)
        q.wait()
        task.status=q.returncode
    show_task_info()
    pass



def add_queue():
    pass

#确保生成的uuid没有重复
uid_check=[]
def get_uuid():

    uid=uuid.uuid4()
    if uid in uid_check:
        get_uuid()
    else:
        uid_check.append(uid)
        return uid
    
    

if __name__=='__main__':
    #api_dict_update()
    api_command()
    '''
    for api in api_dict:
        api_queue.put(api)
    '''

    #print(api_dict[api_queue.get()])
    