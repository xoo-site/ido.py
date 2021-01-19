#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import commands
import re
import socket
import sys
import os
import time
import subprocess
import threading
import logging

color = lambda c, s: "\033[3%sm%s\033[0m" % (c, s)
black = lambda s: color(0, s)
red = lambda s: color(1, s)
green = lambda s: color(2, s)
yellow = lambda s: color(3, s)
blue = lambda s: color(4, s)
purple = lambda s: color(5, s)
cyan = lambda s: color(6, s)
gray = lambda s: color(7, s)
blink = lambda s: "\033[5m%s\033[25m" % s
underline = lambda s: "\033[4m%s\033[24m" % s


def print_ok(check_status):
    fmt = green("[  OK  ]    %s" % check_status)
    print fmt


def print_error(check_status, recomm=''):
    if not check_status.endswith("."):
        check_status += "."
    fmt = red("[  ERROR  ]    %s %s" % (check_status, recomm))
    print fmt


def print_warn(check_status, recomm=''):
    if not check_status.endswith("."):
        check_status += "."
    fmt = yellow("[  WARN  ]    %s %s" % (check_status, recomm))
    print fmt


def print_title(title):
    print "\n"
    t = "%s  %s  %s" % ("=" * 30, title, "=" * 30)
    print t


def get_logger():
    logging.basicConfig(filename='install.log',
                        level=logging.DEBUG,
                        mode="w",
                        format='%(asctime)s %(levelname)s  %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        )
    _logger = logging.getLogger("qdata.install")
    _logger.setLevel(logging.INFO)
    return _logger


logger = get_logger()


def run(cmd):
    logging.info("cmd: %s" % cmd)
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    stdout, stderr = p.communicate()
    if stderr:
        logger.info("cmd stderr: %s" % stderr)
        raise Exception("cmd: %s, stderr: %s" % (cmd, stderr))
    else:
        logger.info("cmd result: %s" % stdout)
        return stdout


def run_cmd(cmd):
    logger.info("cmd: %s" % cmd)
    status = subprocess.check_call(cmd, shell=True)
    return status


def get_system_version():
    """获取系统版本, 6.7/6.8或者7.4

    :rtype str
    :return 系统版本
    """
    version = "unknown"
    file_path = "/etc/redhat-release"
    # Red Hat Enterprise Linux Server release 6.7 (Santiago)
    # Red Hat Enterprise Linux Server release 7.4 (Maipo)
    # CentOS Linux release 7.4.1708 (Core)
    pattern = re.compile(r"release[\s\t]*(\d\.?\d)")
    with open(file_path, "r") as f:
        output = f.read()
    match = pattern.search(output)
    if match:
        version = match.group(1)
    return version, output


# ===============设置supervisord开机自启=================
supervisord = """#!/bin/sh
#
# /etc/rc.d/init.d/supervisord
#
# Supervisor is a client/server system that
# allows its users to monitor and control a
# number of processes on UNIX-like operating
# systems.
#
# chkconfig: - 64 36
# description: Supervisor Server
# processname: supervisord

# Source init functions
. /etc/rc.d/init.d/functions

prog="supervisord"

prefix="/home/sendoh/qdata-cloud/packages/python"
exec_prefix="${prefix}"
prog_bin="${exec_prefix}/bin/supervisord"
conf=/home/sendoh/qdata-cloud/conf/supervisor/supervisord.conf
prog_stop_bin="${exec_prefix}/bin/supervisorctl"

PIDFILE="/var/run/sendoh_supervisord.pid"

ulimit -n 65535
ulimit -u 16384

start()
{
       echo -n $"Starting $prog: "
       daemon $prog_bin --pidfile $PIDFILE -c $conf
       [ -f $PIDFILE ] && success $"$prog startup" || failure $"$prog startup"
       echo
}

stop()
{
       [ -f $PIDFILE ] && action "Stopping $prog"  $prog_stop_bin -c $conf shutdown || success $"$prog shutdown"
       echo
}

case "$1" in

 start)
   start
 ;;

 stop)
   stop
 ;;

 status)
       status $prog
 ;;

 restart)
   stop
   start
 ;;

 *)
   echo "Usage: $0 {start|stop|restart|status}"
 ;;

esac

"""


class QDataBaseInstall(object):
    ALLOWED_SYSTEM_VERSIONS = ["6.6", "6.7", "7.4", "7.5", "7.6"]
    ALLOWED_SYSTEM_TYPES = ["centos", "rehl", "redhat", "red hat"]

    def __init__(self):
        self.check_pass = 0
        self.check_error = 0
        self.check_warn = 0
        self.env_name = "sendoh-web-env"
        self.port_list = ["9307", "6379", "11100", "80", "10011", "10012", "3000", "10002", "10003"]
        self.file_list = ["qdata-cloud"]
        self.username = "sendoh"
        self.password = "cljslrl0620"
        self.mysql_user = "pig"
        self.mysql_passwd = "p7tiULiN0xSp2S03ZHJmHoVBaEYg3NYoRF0h4O7TIEk="
        self.mysql_ok = False
        self.mysql_tar_ok = False
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.MYSQL_NAME = os.path.join(self.env_name, "packages/mysql-5.7.28-linux-glibc2.12-x86_64.tar.gz")
        self.log_dir = "logs"  # 保留qdata cloud log的目录名称
        self.log_sub_dirs = ["mysql", "nginx", "qdata-cloud", "redis", "supervisor", "qflame"]

    # ==========================  属性设置 ======================
    @property
    def home(self):
        return os.path.join("/home", self.username)

    @property
    def root(self):
        return os.path.join(self.home, "qdata-cloud")

    @property
    def log_path(self):
        return os.path.join(self.home, self.log_dir)

    @property
    def mysql_home(self):
        return os.path.join(self.root, "packages", "mysql")

    @property
    def mysql(self):
        return os.path.join(self.mysql_home, "bin", "mysql")

    @property
    def mysql_sock(self):
        return os.path.join(self.root, "data/mysql/mysql.sock")

    @property
    def mysqld(self):
        return os.path.join(self.mysql_home, "bin/mysqld")

    @property
    def packages(self):
        return os.path.join(self.root, "packages")

    @property
    def mysql_conf(self):
        return os.path.join(self.root, "conf/my.cnf")

    @property
    def mysql_sh(self):
        return os.path.join(self.current_path, "mysql_install.sh")

    @property
    def mysql_server(self):
        return os.path.join(self.mysql_home, "support-files/mysql.server")

    @property
    def mysql_alias(self):
        return '%s -upig -pp7tiULiN0xSp2S03ZHJmHoVBaEYg3NYoRF0h4O7TIEk= -S %s' % (self.mysql, self.mysql_sock)

    @property
    def openipmit_rpm(self):
        return os.path.join(self.current_path, "packages/OpenIPMI-modalias-2.0.23-2.el7.x86_64.rpm")

    @property
    def ipmitool_rpm(self):
        return os.path.join(self.current_path, "packages/ipmitool-1.8.18-7.el7.x86_64.rpm")

    @property
    def snmp_lib_rpm(self):
        return os.path.join(self.current_path, "packages/net-snmp-*")

    @property
    def snmp_utils_rpm(self):
        return os.path.join(self.current_path, "packages/net-snmp-utils-5.7.2-37.el7.x86_64.rpm")

    # ===================   基础函数  ===================
    def flash(self):
        """
        清空相关参数，以重新使用
        """
        self.check_pass = 0
        self.check_error = 0
        self.check_warn = 0

    def yes_or_no(self):
        result = raw_input("Ignore warnings?(yes/no):")
        result = result.lower()
        while True:
            if result == 'no' or result == 'n':
                print("your choice is no, install cancled")
                sys.exit(1)
            elif result == 'yes' or result == 'y':
                break
            else:
                result = raw_input("ignore warnings？(yes/no):")

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            try:
                IP_list = commands.getoutput("hostname -I")
                for ip in IP_list.split():
                    if ip.startswith("10.") or ip.startswith("192."):
                        IP = ip
                        break
                else:
                    IP = IP_list.split()[0]
            except:
                IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def set_ip_of_product_yaml(self):
        cmd = "sed -i 's/127.0.0.1/%s/g' %s" % (
            self.get_ip(), os.path.join(self.root, "apps/ci/web_service/product.yaml")
        )
        try:
            run(cmd)
            print_ok("change ip of product.yaml success")
            self.check_pass += 1
        except Exception as e:
            print_error("change ip of product.yaml failed: %s" % str(e))
            self.check_error += 1

    def print_result(self, operation):
        """
        打印汇总结果
        :param operation:操作名称
        :return:
        """
        is_ok = green(self.check_pass)
        is_warn = yellow(self.check_warn) if self.check_warn > 0 else self.check_warn
        is_error = red(self.check_error) if self.check_error > 0 else self.check_error

        print '\n\n*******************************************************************\n\n'
        print "\t\t %s passed: %s\n" % (operation, is_ok)
        print "\t\t %s warnning: %s\n" % (operation, is_warn)
        print "\t\t %s error: %s" % (operation, is_error)
        print '\n\n*******************************************************************'
        if self.check_error > 0:
            sys.exit(1)
        if self.check_warn > 0:
            self.yes_or_no()

    def operation_service_server(self, name, option):
        """启动/停止系统服务

        :rtype str
        :return 执行输出结果
        """
        raise NotImplementedError

    # ======================  check ==================
    def check_os_version(self):
        """
        检查系统版本
        """
        check_ok = False
        system_version, system_version_output = get_system_version()
        for name in self.ALLOWED_SYSTEM_TYPES:
            if name in system_version_output.lower():
                check_ok = True
                break
        version_info = "Check os version: %s" % system_version
        if check_ok and system_version in self.ALLOWED_SYSTEM_VERSIONS:
            print_ok(version_info)
            self.check_pass += 1
        else:
            recomm = "Supported os: %s for version in %s" % (
                "/".join(self.ALLOWED_SYSTEM_TYPES), "/".join(self.ALLOWED_SYSTEM_VERSIONS))
            print_error(version_info, recomm)
            self.check_error += 1

    def check_os_bit(self):
        """
        检查32bit还是64bit
        """
        cmd = "getconf LONG_BIT"
        result = run(cmd).strip()
        if result == "64":
            print_ok("check os 64 bit")
            self.check_pass += 1
        else:
            print_error("check os 64 bit")
            self.check_error += 1

    def check_os_disk(self):
        """
        检查home目录大小是否超过512G
        """
        cmd = """df -Pm /home|sed -n '2p'|awk '{print $4}'"""
        check_result = run(cmd).strip()
        os_home_size = float(check_result) / 1024
        check_status = "Check disk space on /home"
        recomm = "need no less 512G space on /home ,Now is %s G" % round(os_home_size, 1)
        if int(os_home_size) >= 512:
            self.check_pass += 1
            print_ok(check_status=check_status)
        else:
            self.check_warn += 1
            print_warn(check_status=check_status, recomm=recomm)

    def check_os_cpu(self):
        """
        检查cpu数量是否大于4个,如果小于4个，进行warn提示
        """
        cmd = '''lscpu |grep "^CPU(s):"|cut -d':' -f2'''
        result = run(cmd).strip()
        cpu_num = int(result)
        check_status = "Check CPU number"
        recomm = "Need no less 4 cpus ,Now cpu is %s cpus" % cpu_num
        if cpu_num >= 4:
            self.check_pass += 1
            print_ok(check_status=check_status)
        else:
            self.check_warn += 1
            print_warn(check_status=check_status, recomm=recomm)

    def check_os_mem(self):
        """
        检查操作系统内存是否大于8G
        """
        cmd = "cat /proc/meminfo"
        result = run(cmd).lower()
        mem_total = "0 kb"
        for line in result.splitlines():
            if line.startswith("memtotal"):
                mem_total = line.split(":")[-1].strip()
                break

        mem_size = float(mem_total.split()[0])

        if mem_total.endswith("kb"):
            mem_size = mem_size / 1024 / 1024
        elif mem_total.endswith("mb"):
            mem_size = mem_size / 1024
        elif mem_total.endswith("gb"):
            mem_size = mem_size

        check_status = "Check total memory"
        recomm = "need no less 8G Memory ,Now Memory is %s G" % round(mem_size, 1)
        if mem_size >= 8:
            self.check_pass += 1
            print_ok(check_status=check_status)
        else:
            self.check_warn += 1
            print_warn(check_status=check_status, recomm=recomm)

    def check_os_user(self):
        """
        检查用户是否存在，不存在则创建
        """
        cmd_check = "id %s" % self.username
        try:
            run(cmd_check).strip()
            run("echo %s:%s | chpasswd" % (self.username, self.password))
            if os.path.exists(self.home):
                run("sudo chown -R %s:%s %s" % (self.username, self.username, self.home))
            else:
                run("sudo mkdir %s" % self.home)
                run("sudo chown -R %s:%s %s" % (self.username, self.username, self.home))
            print_ok("Check user %s" % self.username)
        except Exception as e:
            print_warn("no user %s, now create_rsync" % self.username)
            cmd_add = "sudo useradd -m -p `openssl passwd -1 -salt  'woqu' %s` %s" % (self.password, self.username)
            try:
                run(cmd_add)
            except Exception as e:
                pass
            if os.path.exists(self.home):
                print_ok("create_rsync user %s" % self.username)
            else:
                print_error("create_rsync user %s" % self.username)
        try:
            # 再次检查
            run(cmd_check).strip()
            print_ok("check user %s exist" % self.username)
            self.check_pass += 1
        except Exception as e:
            print_error("check user %s exist" % self.username)
            self.check_error += 1

    def check_os_port(self):
        """
        检测端口是否被占用
        """
        cmd = "sudo netstat -lnpa | grep LISTEN"
        output = run(cmd)
        all_post = '|'.join(self.port_list)
        use_port = re.findall(r':(%s)\s+.*LISTEN\s+(\d+)/(\S+)\s' % all_post, output)
        use_port = list(set(use_port))
        for port in use_port:
            print_error("port: %s, pid:%s, program:%s in use" % (port[0], port[1], port[2]))
            self.check_error += 1
            if port[0] in self.port_list:
                self.port_list.remove(port[0])
        for port in self.port_list:
            print_ok("check port %s ok" % port)
            self.check_pass += 1

    def do_check(self):
        """
        check部分主函数
        """
        print_title("check")
        self.check_os_version()
        self.check_os_bit()
        self.check_os_disk()
        self.check_os_cpu()
        self.check_os_mem()
        self.check_os_user()
        self.check_os_port()
        self.print_result("check")

    #  ============================    copy ========================
    def get_exist_files(self):
        """
        返回file_list中创建成功的目录
        """
        exist_file = []
        for file in self.file_list:
            file_path = os.path.join(self.home, file)
            if os.path.exists(file_path):
                exist_file.append(file)
        return exist_file

    def change_usermode(self):
        try:
            run("sudo chown -R %s:%s %s" % (self.username, self.username, self.home))
        except:
            print_error("change file owner to %s in %s" % (self.username, self.home))
            sys.stdout.flush()
            self.check_error += 1
        else:
            print_ok("change file owner to %s in %s" % (self.username, self.home))
            sys.stdout.flush()
            self.check_pass += 1

    def copy_files(self):
        """拷贝文件"""

        # 在home目录下，sendoh-web-env则不用进行拷贝
        def _copy_files():
            path_list = ["apps", "conf", "data", "logs", "metadata.yml", "packages", "static", "venvs", ".env", "tmp", "batch_update_qflame_exporter"]
            run_cmd("cp -R %s %s" % (" ".join(path_list), self.root))
            print_ok("copy package files success")
            sys.stdout.flush()
            self.check_pass += 1

        run_cmd("mkdir -p %s" % self.root)
        t = threading.Thread(target=_copy_files)
        t.start()
        while t.isAlive():
            a = ["|", "/", "-", "\\"]
            for i in a:
                sys.stdout.write("\b%s\b" % i)
                sys.stdout.flush()
                time.sleep(0.1)

    def do_copy(self):
        """
        copy部分主函数
        """
        print_title("copy files")
        self.flash()
        self.copy_files()
        self.change_usermode()
        self.print_result("copy file")

    # ========================== install mysql  ====================

    def check_mysql_libaio(self):
        """检查libaio包是否存在

        :rtype result bool
        :return result 包是否存在
            True: 包存在
            False: 包不存在
        """
        cmd = "rpm -qa | grep libaio |wc -l"
        count = int(run(cmd))
        result = False
        if count > 0:
            result = True
        return result

    def set_oracle_ld_library_path(self):
        cmd = "echo '%s' > /etc/ld.so.conf.d/oracle-qdata.conf && sudo ldconfig" % os.path.join(
            self.root, "packages/instantclient_12_2"
        )
        run_cmd(cmd)

    def set_mysql_autostart(self):
        """设置mysql服务， 开机自启动 """
        mysql_init = "/etc/init.d/mysql"
        profile_file = "/etc/profile"

        start_list = list()
        # 1.删除/etc/init.d中原本的mysql
        rm_on = "rm -f %s" % mysql_init
        start_list.append(rm_on)

        # 2.重新复制mysql.server
        cp_on = "cp %s %s" % (self.mysql_server, mysql_init)
        start_list.append(cp_on)
        # 设置执行权限
        chmod_mysql = "chmod +x %s" % mysql_init
        start_list.append(chmod_mysql)

        # 3.检查是否添加过环境变量
        file_home = "export MYSQL_HOME=%s" % self.mysql_home
        file_path = "export PATH=$PATH:$MYSQL_HOME/bin"
        with open(profile_file) as f:
            file_content = f.read()
        with open(profile_file, "a") as f:
            if file_home not in file_content:
                f.write(file_home)
                f.write("\n")
            if file_path not in file_content:
                f.write(file_path)
                f.write("\n")

        # 4.设置开机启动
        chkconfig = "chkconfig --add mysql"
        start_list.append(chkconfig)
        chkconfig_on = "chkconfig --level 2345 mysql on"
        start_list.append(chkconfig_on)

    def start_mysql(self):
        """启动mysql"""
        # 启动前，先杀死老的mysql进程
        # cmd = "pkill "
        # run(cmd)
        # 启动
        cmd_start = "service mysql start > /dev/null"
        os.system(cmd_start)
        logger.info("cmd: %s" % cmd_start)

        output = self.operation_service_server(name="mysql", option="status")

        T = 60
        while "MySQL is not running, but " in output and T >= 0:
            print "\rwaitting for mysql start up %s" % "." * (60 - T)
            sys.stdout.flush()
            time.sleep(1)
            output = self.operation_service_server(name="mysql", option="start")
            T -= 1

        if "not running" in output:
            print_error("start mysql failed: %s " % output)
            sys.exit(1)
        else:
            print_ok("start mysql server")

    def set_mysql_user(self):
        """
        连接mysql，初始密码为空，并添加用户
        """

        grant_cmd = """
        delete from mysql.user;
        delete from mysql.db;
        grant all on *.* to root@'localhost' identified by 'letsg0' with grant option;
        GRANT ALL PRIVILEGES ON *.* TO 'pig'@'%' IDENTIFIED BY '{password}';
        flush privileges;
        """.format(password=os.environ['QDATA_MYSQL_PASSWORD'])
        sock_cmd = 'source %s && %s -uroot -S %s -e "%s"' % (
            os.path.join(self.root, ".env"), self.mysql, self.mysql_sock, grant_cmd
        )
        try:
            run(sock_cmd)
            print_ok("set mysql user success")
        except Exception as e:
            logger.exception(e)
            print_error("set mysql user failed")
            sys.exit(1)

    def create_database(self):
        """
        创建qdata数据库
        """
        create_sql = "CREATE DATABASE  IF NOT EXISTS %s /*!40100 DEFAULT CHARACTER SET utf8 */;" % ("qdata_cloud")
        cmd_list = list()
        # 创建qdata数据库
        create_qdata_cmd = '%s -e "%s"' % (self.mysql_alias, create_sql)
        cmd_list.append(create_qdata_cmd)
        is_ok = True
        for cmd in cmd_list:
            try:
                run(cmd)
            except Exception as e:
                # 这里可能会报警告出来，如果其中有error，则认为是错误
                if "error" in str(e):
                    print_error(str(e))
                    self.check_error += 1
                    is_ok = False
        if is_ok:
            print_ok("create db success")
        else:
            print_error("create db failed")
            sys.exit(1)

    def create_tables(self):
        """
        初始化数据库表
        """
        for name in ["cloud", "ci"]:
            is_ok = True
            python = os.path.join(self.root, 'venvs', name, 'bin/python')
            cmd = "source %s && %s %s" % (os.path.join(self.root, ".env"),
                                          python, os.path.join(self.root, 'apps', name, 'init.py'))
            try:
                run_cmd(cmd)
                print_ok("init %s database success" % name)
            except Exception as e:
                if "error" in str(e):  # 执行mysql语句出现的waring会被送往stderr管道，但是确实执行成功了
                    print_error("%s: %s" % ("init %s database failed" % (name,), str(e)))
                    is_ok = False
                else:
                    print_ok("init %s database success" % name)
            if not is_ok:
                sys.exit(1)

    def install_mysql(self):
        install_log_path = os.path.join(os.getcwd(), "install.log")
        cmd = "sh %s >> %s 2>&1" % (self.mysql_sh, install_log_path)
        result = run_cmd(cmd)
        if result:
            print_error("install mysql failed")
            sys.exit(result)
        print_ok("install mysql success")

    def do_mysql(self):
        """
        mysql部分主函数
        """
        print_title("install mysql")
        if not self.check_mysql_libaio():
            print_error("The libaio package is not installed")
            sys.exit(1)
        self.install_mysql()
        self.set_mysql_autostart()

        self.start_mysql()
        self.set_mysql_user()
        self.create_database()
        self.create_tables()

    def set_environment(self):
        with open(os.path.join(self.root, '.env')) as f:
            output = f.readlines()
            for line in output:
                if line:
                    key, _, value = ''.join(line.strip().split(' ')[1:]).partition('=')
                    os.environ[key] = value

    # =========================  settings ================
    def set_hostname(self, check_again=False):
        """
        检测/etc/hosts是否有相应的设置，如果没有，则进行设置
        :param check_again: True再次检查
        :return:
        """
        cmd = "hostname"
        hostname = run(cmd).strip()
        with open("/etc/hosts") as f:
            lines = f.read()
        pattern = re.compile("127.0.0.1\s+%s" % hostname, re.M)
        match = pattern.search(lines)
        if not match:
            if check_again:
                line = "127.0.0.1   %s" % hostname
                print_error("set hostname in /etc/hosts failed, please add line %s at the end of file %s" % (
                    blink(underline(line)), blink(underline("/etc/hosts"))))
                self.check_error += 1
                return
            else:
                run("echo 127.0.0.1 `hostname` >> /etc/hosts")
                self.set_hostname(True)
        else:
            print_ok("check hostname settings in /etc/hosts")
            self.check_pass += 1

    def set_nginx_lib(self):
        """设置niginx链接
        """
        raise NotImplementedError

    def start_open_firewall(self):
        """启动防火墙服务
        """
        raise NotImplementedError

    def set_firewall(self):
        """
        设置防火墙，开启端口
        """
        raise NotImplementedError

    def set_alias(self):
        """设置alias"""
        supervisord = os.path.join(self.root, "packages/python/bin/supervisord")
        supervisord_conf = os.path.join(self.root, "conf/supervisor/supervisord.conf")
        supervisorctl = os.path.join(self.root, "packages/python/bin/supervisorctl")
        alias_list = list()
        mystart = "alias mystart=\\'%s -c %s\\'" % (supervisord, supervisord_conf)
        alias_list.append(mystart)
        mysuper = "alias mysuper=\\'%s -c %s\\'" % (supervisorctl, supervisord_conf)
        alias_list.append(mysuper)
        senv_cloud = "alias senv_cloud=\\'source %s\\'" % os.path.join(self.root, "venvs/cloud/bin/activate")
        alias_list.append(senv_cloud)
        senv_ci = "alias senv_ci=\\'source %s\\'" % os.path.join(self.root, "venvs/ci/bin/activate")
        alias_list.append(senv_ci)
        mymysql = "alias my9307=\\'%s\\'" % os.path.join(self.mysql_alias)
        alias_list.append(mymysql)
        try:
            now_home = run("echo $HOME").strip()
            no_such_home = False
        except Exception as e:
            print_error(str(e))
            self.check_error += 1
            no_such_home = True
            now_home = ''
        if not no_such_home:
            bashrc = os.path.join(now_home, ".bashrc")
            with open(bashrc) as f:
                alias_content = f.read()
            set_alias_ok = True
            for alias in alias_list:
                res = alias.split("=")
                if res[0] not in alias_content:
                    alias_bash = "echo %s >> %s" % (alias, bashrc)
                    try:
                        run(alias_bash)
                    except Exception as e:
                        print_error(str(e))
                        set_alias_ok = False
                        self.check_error += 1
                        print_error(str(alias_bash))
            if set_alias_ok:
                self.check_pass += 1
                print_ok("set alias success")

    def do_settings(self):
        """
        settings 部分的主函数
        """
        print_title("do settings")
        self.flash()
        self.set_hostname()
        # self.set_crontab()
        self.start_open_firewall()
        self.set_oracle_ld_library_path()
        self.set_nginx_lib()
        self.set_firewall()
        self.set_alias()

    # =============================   start supervisor =====================
    def unlink_supervisor(self):
        """清除supervisor.sock文件
        """
        # 停止supervisor
        try:
            self.operation_service_server(name="supervisord", option="stop")
        except:
            pass
        # 清除supervisor.sock文件
        try:
            sock = run("find /var/run/ -name *supervisor.sock -maxdepth 1")
            ret = sock.split('\n')
            unlink_ok = True
            for res in ret:
                if res:
                    unlink = "unlink %s" % res
                    try:
                        run(unlink)
                    except Exception as e:
                        print_error(str(e))
                        self.check_error += 1
                        unlink_ok = False
            if unlink_ok:
                self.check_pass += 1
                print_ok("unlink supervisor.sock success!")
        except Exception as e:
            print_error(str(e))
            self.check_error += 1

    def start_supervisor(self):
        """启动superviord
        """
        output = self.operation_service_server(name="supervisord", option="status")
        T = 60
        # 确定停止完成
        while self.stop_keyword not in output and T >= 0:
            time.sleep(1)
            output = self.operation_service_server(name="supervisord", option="status")
            T -= 1
        # 启动
        self.operation_service_server(name="supervisord", option="start")

        output = self.operation_service_server(name="supervisord", option="status")
        T = 60
        # 启动后检查是否启动成功
        while self.running_keyword not in output and T >= 0:
            print "\rwaitting for supervisor start up %s" % "." * (60 - T)
            sys.stdout.flush()
            time.sleep(1)
            output = self.operation_service_server(name="supervisord", option="status")
            T -= 1
        if self.stop_keyword in output:
            print_error("start supervisor failed")
            sys.exit(1)
        else:
            print_ok("start supervisor success")

    def set_supervisor_autostart(self):
        """
        supervisor 开机自启动
        """
        global supervisord
        supervisord_path = '/etc/rc.d/init.d/supervisord'
        with open(supervisord_path, 'w') as f:
            f.write(supervisord)
            f.close()
        cmd_list = list()
        chmod_x = "chmod +x %s" % supervisord_path
        cmd_list.append(chmod_x)
        chkconfig_add = "chkconfig --add supervisord"
        cmd_list.append(chkconfig_add)
        chkconfig_on = "chkconfig supervisord on"
        cmd_list.append(chkconfig_on)
        supervisor_boot_start = True
        for cmd in cmd_list:
            try:
                run(cmd)
            except Exception as e:
                print_error(str(e))
                self.check_error += 1
                supervisor_boot_start = False
        if supervisor_boot_start:
            self.check_pass += 1
            print_ok("set supervisor auto start boot success")
        else:
            print_error("set supervisor auto start on boot failed")

    def do_supervisor(self):
        """
        supervisor部分主函数
        """
        print_title("supervisor")
        self.set_supervisor_autostart()
        self.unlink_supervisor()
        self.start_supervisor()

    # =============================   set time zone =====================
    def get_local_time(self):
        """
        获取本地系统时间
        :return:
        """
        cmd = "date"
        try:
            result = run(cmd)
            system_time = result.strip()
            print_ok("you system current time: %s" % system_time)
        except Exception as e:
            print_error("get you system time error: %s" % e.message)

    def show_time_zone(self):
        """
        显示系统当前时区
        :return:
        """
        zone_cmd = "date -R"
        try:
            result = run(zone_cmd)
            time_zone = result.strip()
            print_ok("you system current time zone: %s" % time_zone)
        except Exception as e:
            print_error("get you system time zone error: %s" % e.message)

    def set_system_zone(self):
        """
        设置系统时区
        """
        cmd = "rm -rf /etc/localtime && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime"
        try:
            run(cmd)
            print_ok("set system time zone ok")
        except Exception as e:
            print_error("set system time zone error: %s" % e.message)

    def do_time_zone(self):
        """
        设置系统时区为 上海时区
        """
        print_title("time zone")
        self.get_local_time()
        self.show_time_zone()
        self.set_system_zone()
        self.show_time_zone()
        self.get_local_time()

    # =============================   set system conf =====================

    def set_system_conf(self):
        """
        设置系统参数
        """
        sed_list = [
            "sed -i '/* soft nproc [0-9]/d' /etc/security/limits.conf",
            "sed -i '/* hard nproc [0-9]/d' /etc/security/limits.conf",
            "sed -i '/* soft nofile [0-9]/d' /etc/security/limits.conf",
            "sed -i '/* hard nofile [0-9]/d' /etc/security/limits.conf",
            "sed -i '/sendoh soft nproc [0-9]/d' /etc/security/limits.conf",
            "sed -i '/sendoh hard nproc [0-9]/d' /etc/security/limits.conf"]
        limit_list = [
            "* soft nproc 16384",
            "* hard nproc 16384",
            "* soft nofile 65536",
            "* hard nofile 65536",
            "sendoh soft nproc 16384",
            "sendoh hard nproc 16384"]
        conf_ok = True
        for item in sed_list:
            try:
                run(item)
            except Exception as e:
                conf_ok = False
                print_error("delete conf error, %s" % e.message)
        for item in limit_list:
            try:
                cmd = """ echo "%s" >> /etc/security/limits.conf""" % item
                run(cmd)
            except Exception as e:
                conf_ok = False
                print_error("insert conf error, %s" % e.message)
        if conf_ok:
            print_ok("set system conf")

    def do_system(self):
        """
        设置系统参数
        """
        print_title("system conf")
        self.set_system_conf()

    def check_ipmitool(self):
        try:
            result = run("which ipmitool").strip()
            logger.info(result)
        except Exception:
            result = ""
        if bool(result):
            print_ok("ipmitool already installed")
            print_ok("path: {0}".format(result))
            return True
        else:
            print_warn("ipmitool is not installed")
            return False

    def install_ipmitool(self):
        cmd_list = ["rpm -ivh {0}".format(self.openipmit_rpm),
                    "rpm -ivh {0}".format(self.ipmitool_rpm)]
        for cmd in cmd_list:
            try:
                result = run(cmd)
                print_ok(result)
            except Exception as e:
                print_warn(e.message)

    def do_install_ipmitool(self):
        if not self.check_ipmitool():
            print_ok("now install ipmitool")
            self.install_ipmitool()
            if not self.check_ipmitool():
                print_error("ipmitool install failed")
                self.check_error += 1
                return
        self.check_pass += 1
        return

    def check_snmpwalk(self):
        try:
            result = run("which snmpwalk").strip()
            logger.info(result)
        except Exception:
            result = ""
        if bool(result):
            print_ok("snmpwalk already installed")
            print_ok("path: {0}".format(result))
            return True
        else:
            print_warn("snmpwalk is not installed")
            return False

    def install_snmpwalk(self):
        cmd = "rpm -ivh {0} --force".format(self.snmp_lib_rpm)
        try:
            result = run(cmd)
            print_ok(result)
        except Exception as e:
            print_warn(e.message)

    def do_install_snmpwalk(self):
        if not self.check_snmpwalk():
            print_ok("now install snmpwalk")
            self.install_snmpwalk()
            if not self.check_snmpwalk():
                print_error("snmpwalk install failed")
                self.check_error += 1
                return
        self.check_pass += 1
        return

    def do_install_tool(self):
        print_title("install ipmitool and snmpwalk")
        self.do_install_snmpwalk()
        self.do_install_ipmitool()

    def remind_qflame_exporter_update(self):
        """
        此版本新增指标需要更新一体机端的qflame_exporter, 因此加入提醒
        :return:
        """
        print_title("remind update qflame_exporter on node")
        print_warn("Please check the qflame_export version for all nodes in cloud(/usr/local/qlame/bin/qflame_export --version)")
        print_warn("If qflame_export version < 1.4.2.2, please upgrade it; For qflame_export upgrade, plese check README.md in /home/sendoh/qdata-cloud/batch_update_qflame_exporter/")
        print_ok("Good Luck!")


class QDataSevenInstall(QDataBaseInstall):
    """７.4系统部署
    """

    def __init__(self):
        super(QDataSevenInstall, self).__init__()
        self.stop_keyword = "inactive (dead)"
        self.running_keyword = "active (running)"

    def operation_service_server(self, name, option):
        """启动/停止系统服务

        :rtype str
        :return 执行输出结果
        """
        cmd = "systemctl %s %s" % (option, name)
        output = run(cmd)
        return output

    def set_nginx_lib(self):
        """设置niginx链接
        """
        if not os.path.exists("/lib64/libpcre.so.1"):
            cmd = "ln -s /lib64/libpcre.so.1 /lib64/libpcre.so.0"
            run(cmd)

        if not os.path.exists("/usr/lib64/libpcre.so.0"):
            cmd = "ln -s /lib64/libpcre.so.1 /usr/lib64/libpcre.so.0"
            run(cmd)

    def start_open_firewall(self):
        """启动防火墙服务
        """
        cmd = "systemctl start firewalld.service"
        try:
            run(cmd)
        except Exception as e:
            logger.exception(e)

    def set_firewall(self):
        """设置防火墙，开启端口
        """
        for port in self.port_list:
            result = True
            message = "Set firewall,start %s port success" % port
            try:
                cmd = "firewall-cmd --zone=public --add-port=%s/tcp --permanent  && firewall-cmd --reload" % port
                run(cmd)
            except Exception as e:
                if "Warning: ALREADY_ENABLED:" not in e.message:
                    result = False
                    message = e.message
            if result:
                self.check_pass += 1
                print_ok(message)
            else:
                self.check_error += 1
                print_error(message)

    def set_supervisor_autostart(self):
        """
        7.x 的操作系统中更推荐systemctl 来管理服务，如果系统中本身存在supervisord.service服务，
        则我们系统所用的chkconfig 来设置supervisord开机自启将会失效， 因此重构此方法
        """
        global supervisord
        supervisor_boot_start = True
        old_super = "/etc/init.d/supervisord"

        if os.path.exists(old_super):
            try:
                self.operation_service_server(old_super, "stop")
            except:
                pass
            cmds = [
                "/usr/sbin/chkconfig --del %s" % old_super,
                "/usr/bin/mv %s /etc/init.d/old_supervisord" % old_super,
            ]
            for cmd in cmds:
                try:
                    run(cmd)
                except Exception as e:
                    print_warn(str(e))
                    self.check_warn += 1
                    print_warn("something wrong while remove old supervisord")

        supervisord_path = '/etc/rc.d/init.d/cloudsupervisord'
        with open(supervisord_path, 'w') as f:
            f.write(supervisord)
            f.close()
        cmd_list = list()
        chmod_x = "chmod +x %s" % supervisord_path
        cmd_list.append(chmod_x)
        chkconfig_add = "chkconfig --add cloudsupervisord"
        cmd_list.append(chkconfig_add)
        chkconfig_on = "chkconfig cloudsupervisord on"
        cmd_list.append(chkconfig_on)
        for cmd in cmd_list:
            try:
                run(cmd)
            except Exception as e:
                print_error(str(e))
                self.check_error += 1
                supervisor_boot_start = False
        if supervisor_boot_start:
            self.check_pass += 1
            print_ok("set supervisor auto start boot success")
        else:
            print_error("set supervisor auto start on boot failed")

    def start_supervisor(self):
        """启动superviord
        >>> 此处启动使用的是mystart的逻辑, 此时cloudsupervisord.service还不存在, 因此此处不能用systemctl start cloudsupervisord
        >>> 当机器重启一次后就会自动依据chkconfig生成cloudsupervisord.service
        """
        output = self.operation_service_server(name="cloudsupervisord", option="status")
        T = 60
        # 确定停止完成
        while self.stop_keyword not in output and T >= 0:
            time.sleep(1)
            output = self.operation_service_server(name="cloudsupervisord", option="status")
            T -= 1
        supervisord = os.path.join(self.root, "packages/python/bin/supervisord")
        supervisord_conf = os.path.join(self.root, "conf/supervisor/supervisord.conf")
        supervisorctl = os.path.join(self.root, "packages/python/bin/supervisorctl")
        # 启动
        try:
            run("%s -c %s" % (supervisord, supervisord_conf))
        except:
            print_error("start supervisor failed")
            sys.exit(1)
        output = run("%s -c %s status" % (supervisorctl, supervisord_conf))
        T = 60
        # 启动后检查是否启动成功
        while "RUNNING" not in output and T >= 0:
            print "\rwaitting for supervisor start up %s" % "." * (60 - T)
            sys.stdout.flush()
            time.sleep(1)
            output = run("%s -c %s status" % (supervisorctl, supervisord_conf))
            T -= 1
        if self.stop_keyword in output:
            print_error("start supervisor failed")
            sys.exit(1)
        else:
            print_ok("start supervisor success")


class QDataSixInstall(QDataBaseInstall):
    """６.6/6.7系统部署
    """

    def __init__(self):
        super(QDataSixInstall, self).__init__()
        self.stop_keyword = "is stopped"
        self.running_keyword = "is running"

    def operation_service_server(self, name, option, null=False):
        """启动/停止系统服务

        :rtype str
        :return 执行输出结果
        """
        if null:
            cmd = "service %s %s > /dev/null" % (name, option)
        else:
            cmd = "service %s %s" % (name, option)
        output = run(cmd)
        return output

    def set_nginx_lib(self):
        """设置niginx链接
        """
        pass

    def start_open_firewall(self):
        """启动防火墙服务
        """
        cmd = "service iptables start"
        try:
            run(cmd)
        except Exception as e:
            logger.exception(e)

    def set_firewall(self):
        """
        设置防火墙，开启端口
        """
        for port in self.port_list:
            try:
                cmd = "/sbin/iptables -I INPUT -p tcp --dport %s -j ACCEPT && /etc/rc.d/init.d/iptables save" % port
                run(cmd)
                self.check_pass += 1
                print_ok("Set firewall,start %s port success" % port)
            except Exception as e:
                self.check_error += 1
                print_error(str(e))


class QDataInstall(object):
    """部署QData Cloud环境
    """

    def __init__(self):
        self.system_version, _ = get_system_version()
        if self.system_version.startswith("7"):
            self.manager = QDataSevenInstall()
        else:
            self.manager = QDataSixInstall()

    def __getattr__(self, item):
        func = getattr(self.manager, item)
        return func


def main():
    help_info = "usage: %s [check|copy|mysql|settings|supervisor|time|system]" % sys.argv[0]
    install = QDataInstall()
    if len(sys.argv) == 1:
        install.do_check()
        install.do_copy()
        install.set_environment()
        install.set_ip_of_product_yaml()
        install.do_mysql()
        install.do_settings()
        install.do_time_zone()
        install.do_system()
        install.do_install_tool()
        install.do_supervisor()
        install.remind_qflame_exporter_update()
    elif len(sys.argv) == 2:
        args = sys.argv[1]
        if args in ["-h", "--help"]:
            print help_info
        else:
            args_func = {"check": install.do_check,
                         "copy": install.do_copy,
                         "mysql": install.do_mysql,
                         "settings": install.do_settings,
                         "supervisor": install.do_supervisor,
                         "time": install.do_time_zone,
                         "system": install.do_system
                         }
            func = args_func.get(args)
            if func:
                func()
                install.remind_qflame_exporter_update()
            else:
                print help_info
    else:
        print help_info


if __name__ == "__main__":
    main()
