# LeanShell

## Description

This is a Shell for LeanCloud, by Python(master branch) and Nodejs(NodeJS branch).

## How it work

It provide some API, in API, it use <procstreams> library to shell the command, and print output of shell command in console.

## API

* ls:   A test API, shell command such as "ls -l".
* top:  top -b -n 1 -H
* ps:   ps -eLf
* cpuinfo:  cat /etc/issue && cat /proc/cpuinfo
* shell:    shell command use subprocess.Popen method.

## Features


## Requirements

* psutil>=5.4.3(Python)

* procstreams >= 0.3.0(Nodejs)

## Installation

* just deploy 

## How to use

open https://leancloud.cn/dashboard/apionline/index.html

## How to use in miniapp of wechat 

        var paramsJson = {
            paramsJson: {
                pr_string: "ls -l",
                pr_int: 123,
                pr_date: Date.now(),
                pr_pointer:'5b5b42b4808ca4006fc6e1e4',
                pr_json:{
                    pr_string: "type string",
                    pr_int: 456,
                    pr_date: Date.now(),
                }
            }
        };
        AV.Cloud.run('test', paramsJson).then(console.log('call cloudfun test ok'))

## Credits



## License



