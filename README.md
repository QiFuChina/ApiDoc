# API接口文档

相关程序的Api接口


# 要求


配置需要的运行环境,相关依赖和资源库后续补充

 MockingBird
 
 RobustVideoMatting
 
 Wav2Lip

目录结构
   ```
├── MockingBird
├── RobustVideoMatting
├── Wav2Lip
├── http_command.py  
   ```
   
   
## 任务结构

![image](https://github.com/QiFuChina/ApiDoc/blob/main/res/img/%E4%BB%BB%E5%8A%A1%E7%BB%93%E6%9E%84%E5%9B%BE.jpg)
   
## 接口、结构和执行命令



### 字典数据结构
每个执行程序以字典结构存储外部程序执行命令、输入和输出参数(*目前相关输入参数数量固定，其他调整参数已设置默认值*)
    
字典结构为{键：值}多对键值通过冒号分隔，若键对应的值为空，则命令行中此参数将使用程序内置的默认参数。其中```lip_dict``` 的两个输入参数为其他两个的输出结果，故通过引用获取执行时的参数信息(*参数的文件路径目前以使用中的电脑文件存储路径为标准，后续根据配置环境和存储位置进行修改*)
    
    
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




各个程序执行方式为：打开终端并激活配置好的虚拟环境 ```conda activate environment_name``` →输入启动命令和需要设置的参数```python xxx.py args1 args2......argsn```

    conda activate mock
    python E:/ResourceCode/MockingBird/gen_voice.py --input_txt F:/Test/mock/input/input.txt --input_wav F:/Test/mock/input/input.mp3 --synthesizer_path F:/Test/mock/input/sample01.pt --output_wav F:/Test/mock/output/svdsf.wav
    

总字典结构，具备引用和存储功能

    api_dict={'mock':mock_dict
          ,'rvm':rvm_dict
          ,'lip':lip_dict
          }
      

### 本地环境调用方式
    
执行环境和执行文件路径已经设置好，此方法目前仅获取文件输入的相关参数

    def api_dict_update(args1,args2,args3,args4,args5,args6):
        mock_dict['--input_txt']=args1                          
        mock_dict['--input_wav']=args2                          
        mock_dict['--output_wav']=args3                         
        rvm_dict['--input-source']=args4                        
        rvm_dict['--output-composition']=args5                  
        lip_dict['--outfile']=args6                             
        api_command()
        pass
    
    
### http调用方式
#### 目前通过[Fastapi](https://github.com/tiangolo/fastapi)提供的服务执行，根据文档内容配置执行环境
   调用服务方式 ```uvicorn http_command:app --reload```
   
   浏览器输入 ```http://127.0.0.1:8000/docs``` 进入Api页面
  
### 相关方法说明

    
Api获取的Json数据结构，以字符串形式传递

    class Api(BaseModel):
        mock_input_txt:str = ' '
        mock_input_wav:str = ' '
        mock_synthesizer_path:str = ' '
        mock_output_wav:str = ' '
        rvm_input_source:str = ' '
        rvm_output_composition:str = ' '
        lip_outfile:str = ' '
   
Post请求，Json格式的```Request body``` 将根据输入参数更新字典结构中的各字典值，随后通过调用```api_command()``` 准备执行外部程序命令
<font color='red'>目前jason传递手动复制的参数时由于反斜杠的格式不匹配，部分路径传递值转换不完全</font>

    @app.post("/api/")
    def api_dict_update(api:Api= Body(embed=True)):
        mock_dict['--input_txt']=api.mock_input_txt                         #需要获取的文本文件(目前为获取txt文件路径例如'F:/Test/mock/input_txt/input.txt')
        mock_dict['--input_wav']=api.mock_input_wav                         #需要参考的音频文件(目前为获取wav文件路径的方式,例如'F:/Test/mock/input_wav/input.wav')    
        mock_dict['--synthesizer_path']=api.mock_synthesizer_path           #需要参考的模型文件(目前为获取wav文件路径的方式,例如'F:/Test/mock/synthesizer_path/input.pt')
        mock_dict['--output_wav']=api.mock_output_wav                       #生成的音频文件保存路径(例如'F:/Test/mock/output/svdsf.wav')
        rvm_dict['--input-source']=api.rvm_input_source                     #需要输入的视频文件(目前为获取mp4文件路径的方式,例如'F:/Test/rvm/input/input.mp4')
        rvm_dict['--output-composition']=api.rvm_output_composition         #生成的视频文件保存路径(例如'F:/Test/rvm/output/dfbbbbbd.mp4')
        lip_dict['--outfile']=api.lip_outfile                               #最后合成的视频文件保存路径(例如'F:/Test/lip/results/test/result.mp4')
        api_command()
        pass

Get请求结构与Post类似，可通过Json格式的```Request body``` 或输入框输入相关参数传递方法参数，随后通过调用```api_command()``` 准备执行外部程序命令

生成外部程序执行命令的方法

    def api_command():
        task_list=[]
                                          
        for key,value in api_dict.items():                      #解析api_dict字典格式，转化为可被terminal执行的语句
            api_cmd=''
            for k,v in value.items():                           #对字典内的字典结构继续解析，分别解析出对应字典结构的执行命令
                if v=='':                                       #如果某参数传递值为空，执行命令中将不添加此参数，执行时会使用默认的参数值
                    continue
                api_cmd=api_cmd+k+'  '+v+' '
            api_cmd=api_cmd.split(' ',maxsplit=1)               #分割1次字符串，分割的第一部分为对应的虚拟环境名称，第二部分为需要执行的外部程序命令
            id=get_uuid()                                       #创建uuid
                                                                #创建外部程序执行命令的语句
            cmd='conda activate {} && python {}'.format(api_cmd[0], api_cmd[1])
            sta=None                                            #定义执行状态
            
            task_list.append(task_info(id,cmd,sta))             #一次获取一个功能的执行命令，随后实例化任务信息类(任务ID、任务语句和任务执行状态)并添加到子任务列表中
        all_task_list_append(task_list)                         #每一个子任务列表包含3个子任务，作为一个任务元素添加进总任务列表中
        return           


单个任务的类结构(*生成外部程序执行命令时实例化子任务类，被添加到子任务列表中*)    

    class task_info:
        def __init__(self,uuid,cmd,status):
            self.uuid=uuid
            self.cmd=cmd
            self.status=status



简单查阅输出任务类的信息


    def show_task_info():
        #print(all_task_list[0])
        for task in all_task_list:
            for task_info in task:
                print(task_info.uuid)
                print(task_info.cmd)
                print(task_info.status)
        
        pass


   调用外部程序执行命令的方法
   
       def execute_task(i):
           for task in all_task_list[i]:                        #根据输入参数i的索引值执行任务列表里对应的任务，每个任务内下分3个子任务
               print(task.uuid)
               task.status="*"                                  
               q=subprocess.Popen(task.cmd,shell=True)          #subprocess模块调用外部程序执行命令，执行结束获得returncode，并将状态更新为returncode的值
               q.wait()                                         #wait确保子进程的执行顺序
               task.status=q.returncode
           pass
