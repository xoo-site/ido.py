#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: cluster.py
# Desc:
# Author: Jeyrce.Lu
# Email: jianxin.lu@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/29 下午7:44
# History:
#=============================================================================
"""
import json

payload = {
    "cluster": {
        # todo 不能和已经有的一体机重名
        "name": "用户输入的一体机集群名称",
        "description": "",
        #
        "position": "",
        # 机房
        "room": "",
        # 通道
        "channel": "",
        # 机架
        "rack": "",
        # 一体机序列号
        "uuid": "QD-00047T2I"
    },
    "nodes": [
        {
            "ibcard_ip": [
                "172.16.131.218",
                "172.16.130.218",
                "172.16.128.218",
                "172.16.129.218"
            ],
            "name": "com-218",
            "hostname": "com-218",
            "ip": "10.10.100.218",

            "oracle_listener_port": 1521,
            "vip": "10.10.100.101",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",

            "type_name": "\u8ba1\u7b97\u8282\u70b9",
            "type": "compute",
            "uuid": "QD-00047T2I",

            "ipmi": "10.10.100.217",
            "ipmiuser": "ADMIN",
            "ipmipwd": "MTIzNDU2Nzg=",
        },
        {
            "ibcard_ip": [
                "172.16.128.216",
                "172.16.129.216",
                "172.16.131.216",
                "172.16.130.216"
            ],
            "name": "com-216",
            "ip": "10.10.100.216",
            "type_name": "\u8ba1\u7b97\u8282\u70b9",
            "type": "compute",
            "uuid": "QD-00047T2I",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",
            "hostname": "com-216",

            "oracle_listener_port": 1521,
            "vip": "10.10.100.102",

            "ipmi": "10.10.100.217",
            "ipmiuser": "ADMIN",
            "ipmipwd": "MTIzNDU2Nzg=",

        },
        {
            "ibcard_ip": [
                "172.16.129.220",
                "172.16.128.220"
            ],
            "name": "sto-220",
            "ip": "10.10.100.220",
            "type_name": "\u5b58\u50a8\u8282\u70b9",
            "type": "storage",
            "uuid": "QD-00047T2I",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",
            "hostname": "sto-220",

            "ipmi": "10.10.100.217",
            "ipmiuser": "ADMIN",
            "ipmipwd": "MTIzNDU2Nzg=",
        },
        {
            "ibcard_ip": [
                "172.16.131.21",
                "172.16.129.21",
                "172.16.130.21",
                "172.16.128.21"
            ],
            "name": "qbo-com21",
            "ip": "10.10.100.21",
            "type_name": "\u8ba1\u7b97\u8282\u70b9",
            "type": "compute",
            "uuid": "QD-00047T2I",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",
            "hostname": "qbo-com21",

            "oracle_listener_port": 1521,
            "vip": "10.10.100.101",

            "ipmi": "10.10.100.217",
            "ipmiuser": "ADMIN",
            "ipmipwd": "MTIzNDU2Nzg=",
        },
        {
            "ibcard_ip": [
                "172.16.128.25",
                "172.16.129.25"
            ],
            "name": "qbo-sto25",
            "ip": "10.10.100.25",
            "type_name": "\u5b58\u50a8\u8282\u70b9",
            "type": "storage",
            "uuid": "QD-00047T2I",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",
            "hostname": "qbo-sto25",

            # "ipmi": "10.10.100.217",
            # "ipmiuser": "ADMIN",
            # "ipmipwd": "MTIzNDU2Nzg=",

            "ipmi": "",
            "ipmiuser": "",
            "ipmipwd": "",
        },
        {
            "ibcard_ip": [
                "172.16.129.77",
                "172.16.128.77",
                "172.16.130.77",
                "172.16.131.77"
            ],
            "name": "qbo-com77",
            "ip": "10.10.100.77",
            "type_name": "\u8ba1\u7b97\u8282\u70b9",
            "type": "compute",
            "uuid": "QD-00047T2I",

            "port": 22,
            "pub_key": "",
            "username": "sendoh",
            "password": "Y2xqc2xybDA2MjA=",
            "hostname": "qbo-com77",

            "oracle_listener_port": 1521,
            "vip": "10.10.100.72",

            "ipmi": "10.10.100.217",
            "ipmiuser": "ADMIN",
            "ipmipwd": "MTIzNDU2Nzg=",
        }
    ],
    #
    "switches": [
        {
            "uuid": "",
            "room": "",
            "type": "",
            "ip": "10.10.90.247",
            "port": 22,
            "username": "admin",
            "password": "YWRtaW4=",
            "guid": "",
            "port_count": 0
        }
    ],
    "rac_clusters": [
        {
            "rac_info": {
                # todo 用户输入的rac名字，这个rac名字不能和任何一体的任何rac名字重复，否则用户容易搞不清楚，所以强制用户不能输入重复rac名字，尽管是不同的一体机
                "cluster_alias_name": "2168",
                # ’olsnodes -c‘采集的rac名称
                "cluster_name": "rac",
                "grid_home": "/opt/grid/products/12.2.0",
                "grid_user": "grid",
                "oracle_home": "/opt/oracle/products/12.2.0",
                "oracle_user": "oracle",
                "asm_user": "ASMSNMP",
                "asm_pass": "QSRNJE5NUA==",
                # todo 计划删除
                # "db_user": "DBSNMP",
                # todo 计划删除
                # "db_pass": "REIkTk1Q",
                "scan_port": 1521,
                "cluster_scan_ip": [
                    {
                        "scan_ip": "10.10.100.103",
                        "scan_name": "com-218-216-scan",
                        "scan_port": 1521
                    }
                ]
            },
            "hosts": [
                # 直接引用一体机上的节点的hostname，hostname不会重复
                "com-216", "com-218"
            ],
            "pools": [
                {
                    "importance": "0",
                    "max": "-1",
                    "pool_name": "Generic",
                    "min": "0",
                    "active_hosts": [
                        "com-216",
                        "com-218"
                    ]
                },
                {
                    "importance": "1",
                    "max": "0",
                    "pool_name": "test",
                    "min": "0",
                    "active_hosts": [

                    ]
                },
                {
                    "importance": "0",
                    "max": "-1",
                    "pool_name": "Free",
                    "min": "0",
                    "active_hosts": [

                    ]
                },
                {
                    "importance": "1",
                    "max": "0",
                    "pool_name": "jft",
                    "min": "0",
                    "active_hosts": [

                    ]
                }
            ],
            "databases": [
                {
                    "connect_method": "scanIpWithSid",
                    "managed": "administrator",
                    "db_name": "test",
                    "service_name": "test",
                    "scan_port": 1521,
                    "o_user": "c##oracle",
                    "o_pass": "oracle",
                    "containers": [
                        {
                            "container_uid": 1,
                            "container_id": 1,
                            "name": "CDB$ROOT"
                        },
                        {
                            "container_uid": 2605602673,
                            "container_id": 3,
                            "name": "PDB1"
                        }
                    ],
                    "instances": [
                        {
                            "inst_name": "test1",
                            "inst_stat": "running",
                            "hostname": "com-216",
                            "pdbs": [
                                {
                                    "container_uid": 1,
                                    "container_id": 1,
                                    "name": "CDB$ROOT",
                                    "open_mode": "READ WRITE"
                                },
                                {
                                    "container_uid": 2605602673,
                                    "container_id": 3,
                                    "name": "PDB1",
                                    "open_mode": "READ WRITE"
                                }
                            ]
                        },
                        {
                            "inst_name": "test2",
                            "inst_stat": "running",
                            "hostname": "com-218",
                            "pdbs": [
                                {
                                    "container_uid": 1,
                                    "container_id": 1,
                                    "name": "CDB$ROOT",
                                    "open_mode": "READ WRITE"
                                },
                                {
                                    "container_uid": 2605602673,
                                    "container_id": 3,
                                    "name": "PDB1",
                                    "open_mode": "MOUNTED"
                                }
                            ]
                        }
                    ],
                    "role": "PRIMARY",
                    "is_container": True,
                    "type": "RAC",
                    "server_pools": [

                    ],
                    "database_version": "12.2.0.1.0"
                }
            ],
        }
    ]
}

if __name__ == '__main__':
    json_data = json.dumps(payload)
    with open("cluster.json", "wt") as f:
        f.write(json_data)
    print("over")
