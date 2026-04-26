---
title: "VMware ESXi 升级"
doc_id: "eae85fc8-6f84-4f8f-91a3-1cbdd6fa4cb2"
source_file: "C:\Users\huaci\Desktop\VMware\vSphere\VMware ESXi 鍗囩骇.pdf"
file_type: "pdf"
doc_type: "price_list"
cleaned_at: "2026-04-25 00:00:59"
---

# VMware ESXi 升级

## 基本信息

| 字段 | 值 |
|------|-----|
| 文档ID | `eae85fc8-6f84-4f8f-91a3-1cbdd6fa4cb2` |
| 来源文件 | `C:\Users\huaci\Desktop\VMware\vSphere\VMware ESXi 鍗囩骇.pdf` |
| 文件类型 | `pdf` |
| 文档类型 | `price_list` |
| 清洗时间 | `2026-04-25 00:00:59` |

## 清洗警告

- 自动检测 PDF 类型: marketing_whitepaper

## 表格数据

### 表格 1

| 为：protocol://hostname |
| --- |
| ipv4 | '['ipv6']'[:port]。该协议必须 |

### 表格 2

| 筛选器必须用双竖线“ | ”分隔。日志筛 |
| --- | --- |
| 选器的格式为：numLogs | ident |

---

## 正文

[第1页]
VMware ESXi 升级
Update 3
VMware vSphere 7.0
VMware ESXi 7.0
[第2页]
您可以从 VMware 网站下载最新的技术文档：
https://docs.vmware.com/cn/。
VMware, Inc.
3401 Hillview Ave.
Palo Alto, CA 94304
www.vmware.com
威睿信息技术（中国）有
限公司
北京办公室
北京市
朝阳区新源南路 8 号
启皓北京东塔 8 层 801
www.vmware.com/cn
上海办公室
上海市
淮海中路 333 号
瑞安大厦 804-809 室
www.vmware.com/cn
广州办公室
广州市
天河路 385 号
太古汇一座 3502 室
www.vmware.com/cn
版权所有
© 2018-2022 VMware, Inc. 保留所有权利。 版权和商标信息 VMware ESXi 升级 VMware, Inc. 2 [第3页] 目录 1
关于 VMware ESXi 升级
5
2 vCenter Server 升级选项
6
vSphere 升级过程概述
7
ESXi 主机升级过程概览
8
升级虚拟机和 VMware Tools
10
3 升级 ESXi 主机
12
ESXi 要求
13
ESXi 系统存储概述
13
ESXi 硬件要求
16
支持的远程管理服务器型号和固件版本
19
增强 ESXi 性能的建议
19
ESXi 主机的入站和出站防火墙端口
20
系统日志记录所需的可用空间
20
VMware Host Client 系统要求
21
ESXi 密码和帐户锁定
21
升级 ESXi 主机之前
23
升级具有第三方自定义 VIB 的主机
24
在具有 VMware NSX-T™ Data Center 的环境中升级 ESXi 主机 25
创建自定义映像配置文件，以在具有 VMware NSX-T Data Center 的环境中升级 ESXi 主机 25
创建新的 ISO 映像，以在具有 VMware NSX-T Data Center 的环境中升级 ESXi 主机 26
在具有 VMware NSX-T Data Center 的环境中使用 ESXCLI 升级 ESXi 主机 26
引导 ESXi 安装程序的介质选项
27
下载 ESXi 安装程序
33
存储设备名称和标识符
33
以交互方式升级主机
35
通过使用脚本安装或升级主机
36
输入引导选项以启动安装或升级脚本
36
引导选项
37
关于安装和升级脚本
38
使用脚本从 CD 或 DVD 安装或升级 ESXi
48
使用脚本从 USB 闪存驱动器安装或升级 ESXi
49
利用通过网络引导安装程序执行 ESXi 脚本式安装或升级
50
网络引导安装过程概述
51
使用 PXE 和 TFTP 引导 ESXi 安装程序
52
使用 iPXE 和 HTTP 引导 ESXi 安装程序
54
VMware, Inc.
3
[第4页]
使用本机 UEFI HTTP 引导 ESXi 安装程序
57
网络引导背景信息
59
PXELINUX 配置文件
60
示例 DHCP 配置
61
使用 ESXCLI 命令升级主机
64
VIB、映像配置文件和软件库
64
了解 VIB 和主机的接受级别
65
确定更新是否需要主机处于维护模式或重新引导
67
将主机置于维护模式
68
使用各个 VIB 更新主机
70
使用映像配置文件升级或更新主机
71
使用 Zip 文件更新 ESXi 主机
74
从主机中移除 VIB
74
使用 ESXCLI 命令将第三方扩展添加到主机
76
执行 ESXCLI 安装或升级试运行
76
显示将在下一次重新引导主机后激活的已安装 VIB 和配置文件
77
显示主机的映像配置文件和接受程度
77
升级 ESXi 主机之后
78
关于 ESXi 评估和许可模式
78
为升级后的 ESXi 主机提供许可
79
在升级后的 ESXi 主机上运行安全引导验证脚本
79
系统日志记录所需的可用空间
80
在 ESXi 主机上配置 Syslog
80
ESXi Syslog 选项
81
在 ESXi 主机上配置日志筛选
85
4 使用 vSphere Auto Deploy 重新置备主机 86
vSphere Auto Deploy 简介
86
准备 vSphere Auto Deploy
89
为系统准备 vSphere Auto Deploy
89
使用 vSphere Auto Deploy Cmdlet
92
设置批量许可
93
重新置备主机
94
通过简单的重新引导操作重新置备主机
94
使用 PowerCLI 时用新映像配置文件重新置备主机
95
编写规则并给主机分配主机配置文件
96
测试和修复规则合规性
97
5 收集日志以对 ESXi 主机进行故障排除
100
VMware ESXi 升级
VMware, Inc.
4
[第5页]
关于 VMware ESXi 升级
1
《VMware ESXi 升级》介绍了如何将 VMware ESXi™ 升级到当前版本。
VMware 非常重视包容性。为了在我们的客户、合作伙伴和内部社区中促进此原则的实施，我们更新了本
指南，移除了非包容性语言的实例。
目标读者
《VMware ESXi 升级》面向需要从早期版本的 ESXi 进行升级的所有用户。这些主题的目标读者为熟悉虚
拟机技术和数据中心操作且具有丰富经验的 Microsoft Windows 或 Linux 系统管理员。 VMware, Inc. 5 [第6页]
vCenter Server 升级选项
2
vCenter Server7.0 提供了多个用于升级vCenter Server 部署的选项。要成功升级 vCenter Server，必
须了解升级选项、影响升级过程的配置详细信息以及任务顺序。
vSphere 的两个核心组件是 VMware ESXi™ 和 VMware vCenter Server™。ESXi 是用于创建和运行虚拟
机和虚拟设备的虚拟化平台。vCenter Server 是一种服务，充当连接到网络的ESXi 主机的中心管理员。
您使用vCenter Server 系统将多个主机的资源加入池中并管理这些资源。vCenter ServerAppliance 是经
过优化以运行 vCenter Server 的预配置虚拟机。
可以将包含嵌入式或外部 Platform Services Controller 的现有 vCenter Server 部署升级到包含 vCenter
Server Appliance 的部署。
本章讨论了以下主题：
n
vSphere 升级过程概述
VMware, Inc.
6
[第7页]
vSphere 升级过程概述
vSphere 是一款复杂的产品，具有多个要升级的组件。理解所需的任务顺序对于成功升级 vSphere 至关重 要。
图 2-1. vSphere 升级任务概述
开始 vSphere 升级
升级到 vSphere 7.0 完成
备份您的配置
升级 vCenter Server
升级 ESXi 主机
升级虚拟机
升级 vSphere 包含下列任务：
1
阅读 vSphere 发行说明。
2
验证是否已备份配置。
3
如果 vSphere 系统包括 VMware 解决方案或插件，请验证它们是否与要升级到的 vCenter Server
Appliance 版本兼容。请参见《VMware 产品互操作性列表》，网址为 http://www.vmware.com/
resources/compatibility/sim/interop_matrix.php。 4
升级 vCenter Server。
有关详细说明，请参见《vCenter Server 升级》
5
升级 ESXi 主机。请参见ESXi 主机升级过程概览。
6
要确保有足够的磁盘存储来存储日志文件，请考虑设置用于远程日志记录的 syslog 服务器对于本地存
储量有限的主机，在远程主机上设置日志记录尤为重要。
请参见系统日志记录所需的可用空间和在 ESXi 主机上配置 Syslog。 VMware ESXi 升级 VMware, Inc. 7 [第8页] 7
通过手动或使用 vSphere Lifecycle Manager 执行协调升级，升级虚拟机。
请参见升级虚拟机和 VMware Tools
ESXi 主机升级过程概览
VMware 提供了多种方法用于将 ESXi 版本 6.5 和版本 6.7 的主机升级到 ESXi 版本 7.0。
到 ESXi 7.0 的升级支持的详细信息和级别取决于要升级的主机和所使用的升级方法。验证是否支持从
ESXi 的当前版本升级到目标版本的升级途径。有关详细信息，请参见 VMware 产品互操作性列表，网址
为 http://www.vmware.com/resources/compatibility/sim/interop_matrix.php。
您可以从 CD、DVD 或 USB 使用交互式升级、脚本式升级、ESXCLI 或 vSphere Lifecycle Manager 升
级版本 6.5 或 6.7 的 ESXi 主机。将具有自定义 VIB 的 ESXi 6.5 或 6.7 主机升级到版本 7.0 时，将迁移所
有受支持的自定义 VIB。 有关详细信息，请参见升级具有第三方自定义 VIB 的主机。 VMware ESXi 升级 VMware, Inc. 8 [第9页]
图 2-2. ESXi 主机升级过程概览
开始 ESXi 升级
选择升级方法
确认满足要求
准备使用 Auto Deploy 升级 ESXi 主机
准备使用 vSphere Lifecycle Manager
升级 ESXi 主机
准备 ESXi 主机升级
使用 Auto Deploy 升级 ESXi 主机
使用 vSphere Lifecycle Manager
升级 ESXi 主机
使用 GUI、脚本或
CLI 升级 ESXi 主机
执行升级后任务
升级到 ESXi 7.0 已完成
以下简要步骤用于升级 ESXi。
1
验证您的系统是否满足升级要求。请参见ESXi 要求。
2
在升级之前准备环境。请参见 升级 ESXi 主机之前。
3
确定要查找和引导 ESXi 安装程序的位置。请参见引导 ESXi 安装程序的介质选项。如果通过网络引导
安装程序，请验证是否正确设置了网络引导基础架构。请参见#unique_12。 4
升级 ESXi。请参见第 3 章 升级 ESXi 主机
5
升级 ESXi 主机后，必须将主机重新连接到 vCenter Server 并重新应用许可证。请参见升级 ESXi 主 机之后。 VMware ESXi 升级 VMware, Inc. 9 [第10页]
支持使用以下方法直接升级到 ESXi 7.0。
n
从 CD、DVD 或 USB 驱动器使用交互式图形用户界面 (GUI) 安装程序。 n 执行脚本式升级。 n 使用 ESXCLI。 n
请使用 vSphere Auto Deploy。如果 ESXi 主机是使用 vSphere Auto Deploy 进行部署的，则可以使
用 vSphere Auto Deploy 通过 7.0 映像重新置备主机。 n
使用 vSphere Lifecycle Manager。
图形用户界面 (Graphical User Interface, GUI) 安装程序
要以交互方式进行升级，可以使用 CD、DVD 或 USB 闪存上的 ESXi 安装程序 ISO 映像，也可以通过
网络引导安装程序。此方法适用于少数主机的部署。如果在安装过程中选择包含 ESXi 安装的目标磁
盘，则安装程序会将主机升级到 ESXi 版本 7.0。安装程序还将为您提供一个选项，用于迁移一些现有
的主机设置和配置文件以及保留现有 VMFS 数据存储。请参见以交互方式升级主机。 执行脚本式升级
要执行脚本式升级，可以使用 CD、DVD 或 USB 闪存上的 ESXi 7.0 安装程序，也可以通过网络引导
安装程序。此方法是部署多个主机的高效方式。有关详细信息，请参见通过使用脚本安装或升级主机。 ESXCLI
您可以使用 ESXCLI 将 ESXi 6.5 主机或 ESXi 6.7 主机升级到 ESXi 7.0 主机。请参见 使用 ESXCLI 命 令升级主机 。
vSphere Auto Deploy
如果使用 vSphere Auto Deploy 部署 ESXi 主机，可以使用 vSphere Auto Deploy 重新置备主机并
通过新的映像配置文件重新引导该主机。该配置文件包含 ESXi 升级或修补程序、主机配置的配置文件
或者由 VMware 合作伙伴提供的第三方驱动程序或管理代理。可以通过使用 vSphere ESXi Image
Builder CLI 来构建自定义映像。有关详细信息，请参见第 4 章 使用 vSphere Auto Deploy 重新置备 主机 。
vSphere Lifecycle Manager
vSphere Lifecycle Manager 是用于安装、升级和更新 ESXi 主机的 vCenter Server 服务。通过使用
映像和基准，vSphere Lifecycle Manager 可在集群级别为多个 ESXi 主机启用集中式和简化的生命周
期管理。有关执行协调安装、升级和更新的详细信息，请参见《管理主机和集群生命周期》文档。
升级虚拟机和 VMware Tools
升级 ESXi 主机之后，您可以升级主机上的虚拟机，使其能够利用新功能。
您可以使用以下工具升级虚拟机。
vSphere Client
VMware ESXi 升级
VMware, Inc.
10
[第11页]
您可以使用 vSphere Client 逐步升级虚拟机。有关升级虚拟机的详细信息，请参见《《vSphere 虚拟 机管理》》文档。
vSphere Lifecycle Manager
您可以使用 vSphere Lifecycle Manager 升级环境中的虚拟机硬件和 VMware Tools 版本的虚拟机。
vSphere Lifecycle Manager 可自动执行升级过程，并验证步骤是否按正确的顺序进行。有关详细信
息，请参见《管理主机和集群生命周期》文档。
VMware ESXi 升级
VMware, Inc.
11
[第12页]
升级 ESXi 主机
3
升级 vCenter Server 后，升级 ESXi 主机。可以将 ESXi 6.5 和 6.7 主机直接升级到 ESXi 7.0。
要升级主机，可使用ESXi 主机升级过程概览中介绍的工具和方法。
小心 如果升级由 vCenter Server 管理的主机，必须先升级 vCenter Server，然后才能升级 ESXi 主机。
如果不按正确的顺序升级您的环境，则可能会丢失数据且无法访问服务器。 本章讨论了以下主题： n ESXi 要求 n 升级 ESXi 主机之前 n
升级具有第三方自定义 VIB 的主机
n
在具有 VMware NSX-T™ Data Center 的环境中升级 ESXi 主机 n
引导 ESXi 安装程序的介质选项
n
下载 ESXi 安装程序
n
存储设备名称和标识符
n
以交互方式升级主机
n
通过使用脚本安装或升级主机
n
网络引导安装过程概述
n
使用 ESXCLI 命令升级主机
n
升级 ESXi 主机之后
VMware, Inc.
12
[第13页]
ESXi 要求
要安装或升级 ESXi，系统必须满足特定的硬件和软件要求。
ESXi 系统存储概述
ESXi 7.0 引入了一种系统存储布局，可对大型模块和第三方组件进行灵活的分区管理和支持，同时简化了 调试操作。
ESXi 7.0 系统存储更改
在 ESXi 7.0 之前，分区大小固定不变，除 /scratch 分区和可选 VMFS 数据存储之外，且分区号是静态
的，这些限制了分区管理。在 ESXi 7.0 中，分区整合为更少且更大的可扩展分区，具体取决于所使用的引 导介质及其容量。
ESXi 7.0 系统存储布局包含四个分区：
表 3-1. ESXi 7.0 系统存储分区：
分区
适用情况
类型
系统引导
存储引导加载程序和 EFI 模块。
FAT16
引导槽 0
用于存储 ESXi 引导模块的系统空间。
FAT16
引导槽 1
用于存储 ESXi 引导模块的系统空间。
FAT16
ESX-OSData
作为存储其他模块的统一位置。
不用于引导和虚拟机。
整合旧版 /scratch 分区、VMware Tools 的 locker 分区和核心转储目标。
小心 始终在未在 ESXi 主机之间共享的持久存储设备上创建 ESX-OSData 分区。仅对引导
槽分区使用 USB、SD 和非 USB 闪存介质设备。
VMFS-L
ESX-OSData 卷大概分为两类数据：永久数据和非永久数据。永久数据包含不经常写入的数据，例如
VMware Tools ISO、配置和核心转储。
非永久数据包含频繁写入的数据，例如日志、VMFS 全局跟踪、vSAN 条目持久性守护进程 (EPD) 数据、 vSAN 跟踪和实时数据库。 VMware ESXi 升级 VMware, Inc. 13 [第14页]
图 3-1. ESXi 7.0 及更高版本中整合的系统存储
引导槽 0
系统引导
引导槽 1
小型核心转储
暂存
VMFS 数据存储
引导槽 0
系统引导
引导槽 1
VMFS 数据存储
ESX-OSData
ROM 数据
RAM 数据
4 MB
250 MB
250 MB
110 MB
286 MB
2.5 GB
4 GB
（介质 > 8.5 GB 时创建
不在 USB 闪存上创建）
locker
大型核心转储
（介质 > 3.4 GB 时创建）
ESXi 6.x
系统存储布局
ESXi 7.0
系统存储布局
100 MB
500 MB 到 4 GB，
（具体取决于
所使用的
引导介质的大小）
500 MB 到 4 GB，
（具体取决于
所使用的
引导介质的大小）
剩余空间，
最多 138 GB
剩余空间，
（介质大小 > 142 GB）
VMware ESXi 升级
VMware, Inc.
14
[第15页]
ESXi 7.0 系统存储大小
分区大小（系统引导分区除外）可能会因所用引导介质的大小而异。如果引导介质具有高耐用性且容量大
于 142 GB，则会自动创建 VMFS 数据存储以存储虚拟机数据。
可以通过使用 vSphere Client 并导航到分区详细信息视图，查看 ESXi 安装程序配置的引导介质容量和自
动大小。或者，也可以使用 ESXCLI，例如 esxcli storage filesystem list 命令。
表 3-2. ESXi 7.0 系统存储大小，具体取决于所使用的引导介质及其容量。 引导介质大小 4-10 GB 10-32 GB 32-128 GB 大于 128 GB 系统引导 100 MB 100 MB 100 MB 100 MB 引导槽 0 500 MB 1 GB 4 GB 4 GB 引导槽 1 500 MB 1 GB 4 GB 4 GB ESX-OSData 剩余空间 剩余空间 剩余空间 最多 128 GB VMFS 数据存储
介质大小 > 142 GB 时
的剩余空间
从 vSphere 7.0 Update 1c 开始，可以使用 ESXi 安装程序引导选项 systemMediaSize 限制引导介质上的
系统存储分区大小。如果您的系统占用空间较小，不需要 128 GB 的最大系统存储大小，则可以将其限制
为最小值 32 GB。systemMediaSize 参数接受以下值： n
min（32 GB，适用于单个磁盘或嵌入式服务器）
n
small（64 GB，适用于至少具有 512 GB RAM 的服务器） n
default (128 GB)
n
max（多余多 TB 服务器，使用所有可用空间）
注 GB 单位为 2^30 字节或 1024*1024*1024 字节的倍数。
所选值必须符合您的系统用途。例如，具有 1 TB 内存的系统必须至少将 64 GB 内存用于系统存储。要在
安装时设置引导选项，例如 systemMediaSize=small，请参阅输入引导选项以启动安装或升级脚本。有关
详细信息，请参见知识库文章 81166。
ESXi 7.0 系统存储链接
需要访问 ESXi 分区的子系统可使用以下符号链接访问这些分区：
表 3-3. ESXi 7.0 系统存储符号链接。
系统存储卷
符号链接
引导槽 0
/bootbank
引导槽 1
/altbootbank
VMware ESXi 升级
VMware, Inc.
15
[第16页]
表 3-3. ESXi 7.0 系统存储符号链接。 （续）
系统存储卷
符号链接
永久数据
/productLocker
/locker
/var/core
/usr/lib/vmware/isoimages
/usr/lib/vmware/floppies
非永久数据
/var/run
/var/log
/var/vmware
/var/tmp
/scratch
ESXi 硬件要求
确保主机符合 ESXi 7.0 支持的最低硬件配置。
硬件和系统资源
要安装或升级 ESXi，您的硬件和系统资源必须满足下列要求：
n
支持的服务器平台。有关支持的平台的列表，请参见《VMware 兼容性指南》，网址为 http://
www.vmware.com/resources/compatibility。 n
ESXi 7.0 要求主机至少具有两个 CPU 内核。
n
ESXi 7.0 支持广泛的多核 64 位 x86 处理器。有关受支持处理器的完整列表，请参见《VMware 兼容
性指南》，网址为 http://www.vmware.com/resources/compatibility。 n
ESXi7.0 需要在 BIOS 中针对 CPU 启用 NX/XD 位。 n
ESXi7.0 需要至少 4 GB 的物理 RAM。至少提供 8 GB 的 RAM，以便能够在典型生产环境中运行虚拟 机。 n
要支持 64 位虚拟机，x64 CPU 必须能够支持硬件虚拟化（Intel VT-x 或 AMD RVI）。 n
一个或多个千兆或更快以太网控制器。有关支持的网络适配器型号的列表，请参见《VMware 兼容性
指南》，网址为 http://www.vmware.com/resources/compatibility。 n
ESXi 7.0 需要至少具有 32 GB 永久存储（如 HDD、SSD 或 NVMe）的引导磁盘。仅对 ESXi 引导槽
分区使用 USB、SD 和非 USB 闪存介质设备。引导设备不得在 ESXi 主机之间共享。 n
SCSI 磁盘或包含未分区空间用于虚拟机的本地（非网络）RAID LUN。 n
对于串行 ATA (SATA)，有一个通过支持的 SAS 控制器或支持的板载 SATA 控制器连接的磁盘。
SATA 磁盘被视为远程、非本地磁盘。默认情况下，这些磁盘用作暂存分区，因为它们被视为远程磁 盘。
注 不能将 SATA CD-ROM 设备连接到 ESXi 主机上的虚拟机。要使用 SATA CD-ROM 设备，必须 使用 IDE 模拟模式。 VMware ESXi 升级 VMware, Inc. 16 [第17页] 存储系统
有关支持的存储系统的列表，请参见《VMware 兼容性指南》，网址为 http://www.vmware.com/
resources/compatibility。有关软件以太网光纤通道 (FCoE)，请参见使用软件 FCoE 安装并引导 ESXi。 ESXi 引导要求
vSphere 7.0 支持从统一可扩展固件接口 (Unified Extensible Firmware Interface, UEFI) 引导 ESXi 主
机。可以使用 UEFI 从硬盘驱动器、CD-ROM 驱动器或 USB 介质引导系统。
vSphere Auto Deploy 支持使用 UEFI 进行 ESXi 主机的网络引导和置备。
如您正在使用的系统固件和任何附加卡上的固件均支持大于 2 TB 的磁盘，则 ESXi 可以从该磁盘进行引 导，。请参见供应商文档。
ESXi7.0 安装或升级的存储要求
为确保 ESXi 7.0 安装实现最佳性能，请对引导设备使用最小为 32 GB 的持久存储设备。要升级到 ESXi
7.0，引导设备至少需要为 4 GB。从本地磁盘、SAN 或 iSCSI LUN 引导时，要求至少具有 32 GB 磁盘以
便能够创建系统存储卷，其中包括引导分区、引导槽和基于 VMFS-L 的 ESX-OSData 卷。ESX-OSData
卷承担旧版 /scratch 分区、VMware Tools 的 locker 分区以及核心转储目标的角色。
有助于 ESXi 7.0 安装实现最佳性能的其他选项如下所示： n
本地磁盘为 128 GB 或更大，以获得 ESX-OSData 的最佳支持。磁盘包含引导分区、ESX-OSData 卷 和 VMFS 数据存储。 n
最少支持 128 写入兆兆字节 (TBW) 的设备。
n
提供至少 100 MB/s 顺序写入速度的设备。
n
为了在设备出现故障时具有弹性，建议使用 RAID 1 镜像设备。
注 GB 单位为 2^30 字节或 1024*1024*1024 字节的倍数。
支持旧版 SD 和 USB 设备，但存在以下限制：
n
对引导槽分区支持使用 SD 和 USB 设备。为确保最佳性能，还要提供最小为 32 GB 的单独持久本地设
备，用于存储 ESX-OSData 卷的 /scratch 和 VMware Tools 分区。持久本地设备的最佳容量为
128 GB。使用 SD 和 USB 设备存储 ESX-OSData 分区的做法即将弃用。 n
从 ESXi 7.0 Update 3 开始，如果引导设备是没有本地持久存储的 USB 或 SD 卡（如 HDD、SSD 或
NVMe 设备），会在 RAM 磁盘上自动创建 VMware Tools 分区。有关详细信息，请参见知识库文章 83376。 n
如果将 /scratch 分区分配给没有本地持久存储的 USB 或 SD 卡，您会看到警告，阻止您在闪存介质
设备上创建或配置引导槽分区以外的分区。为实现最佳性能，请在 RAM 磁盘上设置 /scratch 分
区。您还可以配置 /scratch 分区并将其移至 SAN 或 NFS。有关详细信息，请参见知识库文章 1033696。 n
对于要在 SD 闪存存储设备上安装 ESXi 的特定服务器型号，必须使用服务器供应商批准的 SD 闪存设
备。可以在 partnerweb.vmware.com 上找到经过验证的设备列表。 VMware ESXi 升级 VMware, Inc. 17 [第18页] n
有关基于 SD 卡或基于 USB 的环境的更新指导，请参见知识库文章 85685。 n
要选择合适的 SD 或 USB 引导设备，请参见知识库文章 82515。
小心 如果找不到本地磁盘，或引导介质为 USB 或 SD 设备，而无用于持久数据的额外高耐用性存储，
则 /scratch 分区位于 RAM 磁盘上，链接到 /tmp，并且 ESXi 7.0 在降级模式下运行。
在降级模式下，您会看到系统警示，如：警示：系统日志和数据无持久存储可用。ESX 在运行时具有有限
系统存储空间，日志和系统数据将在重新引导时丢失。
当 ESXi 7.0 在降级模式下运行时，日志的 RAM 消耗可能会对临时数据导致非持久日志，可能无法记录或
内存不足。由于重新构建磁盘状态所花费的时间，因此引导速度可能会变慢。
使用具有足够大小的持久存储以防止降级模式。您可以重新配置 /scratch 以使用单独的磁盘或 LUN。
升级到 ESXi 7.0 的过程会对引导设备重新进行分区，将原始核心转储、locker 和暂存分区整合到 ESX- OSData 卷中。
在重新分区过程中会发生以下事件：
n
如果未配置自定义核心转储目标，则默认核心转储位置为 ESX-OSData 卷中的一个文件。 n
如果将 syslog 服务配置为在 4 GB VFAT 暂存分区上存储日志文件，var/run/log 中的日志文件将
迁移到 ESX-OSData 卷。
n
VMware Tools 将从 locker 分区进行迁移，并擦除该分区。 n
擦除核心转储分区。删除在暂存分区上存储的应用程序核心转储文件。
注 由于引导设备的重新分区过程，无法回滚到早期版本的 ESXi。要在升级到版本 7.0 后使用较低版本的
ESXi，必须在升级之前创建引导设备的备份，然后从备份还原 ESXi 引导设备。
如果使用 USB 或 SD 设备执行升级，安装程序会尝试在可用的本地磁盘上分配ESX-OSData 区域。如果
没有可用空间，则数据存储用于 /scratch。如果未找到本地磁盘或数据存储，则 /scratch 将放置在
RAM 磁盘上。升级后，请重新配置 /scratch 以使用持久性数据存储，或为系统存储卷添加新磁盘。
有关重新配置 /scratch 分区的详细信息，请参见《vCenter Server 安装和设置》文档。
升级到 ESXi 7.0 后，可以添加新的本地磁盘，并启用设置 autoPartition=TRUE。重新引导后，将对引导
磁盘进行分区。有关配置 ESXi 系统分区大小的引导选项的详细信息，请参见知识库文章 https://
kb.vmware.com/s/article/81166。
在 Auto Deploy 安装情形下，安装程序将尝试在可用的本地磁盘或数据存储上分配暂存区域。如果未找到
本地磁盘或数据存储，则 /scratch 分区将放置在 RAM 磁盘上。请在安装之后重新配置 /scratch 以使 用持久性数据存储。
对于从 SAN 引导或使用 Auto Deploy 的环境，必须在单独的 SAN LUN 上设置每个 ESXi 主机的 ESX-
OSData 卷。但是，如果 /scratch 配置为不使用 ESX-OSData，则无需为每个主机的 /scratch 分配
单独的 LUN。可以将多个 ESXi 主机的暂存区域同时放置在一个 LUN 上。分配给任一 LUN 的主机数量应
根据 LUN 的大小以及虚拟机的 I/O 行为来权衡。
VMware ESXi 升级
VMware, Inc.
18
[第19页]
支持的远程管理服务器型号和固件版本
远程管理应用程序可用于安装或升级 ESXi 或者远程管理主机。
表 3-4. 受支持的远程管理服务器型号和最低固件版本
远程管理服务器型号
固件版本
Java
Dell DRAC 7
1.30.30（内部版本 43）
1.7.0_60-b19
Dell DRAC 6
1.54（内部版本 15）、1.70（内部版本 21）
1.6.0_24
Dell DRAC 5
1.0, 1.45, 1.51
1.6.0_20,1.6.0_203
Dell DRAC 4
1.75
1.6.0_23
HP ILO
1.81, 1.92
1.6.0_22, 1.6.0_23
HP ILO 2
1.8, 1.81
1.6.0_20, 1.6.0_23
HP ILO 3
1.28
1.7.0_60-b19
HP ILO 4
1.13
1.7.0_60-b19
IBM RSA 2
1.03, 1.2
1.6.0_22
增强 ESXi 性能的建议
要增强性能，请在内存超过最低要求数量并且具有多个物理磁盘的强大系统上安装或升级 ESXi。
有关 ESXi 系统要求，请参见ESXi 硬件要求。
表 3-5. 增强性能的建议
系统元件
建议
内存
ESXi 主机比普通服务器需要更多的内存。至少提供 8 GB 的
RAM，以便能够充分利用 ESXi 的功能，并在典型生产环境下
运行虚拟机。 ESXi 主机必须具有足够的内存才能同时运行多台
虚拟机。以下示例可帮助您计算在 ESXi 主机上运行的虚拟机所 需的内存。
使用 Red Hat Enterprise Linux 或 Windows XP 运行四台虚拟
机，至少需要配备 3 GB 的内存才能达到基准性能。此数字中有
1024 MB 用于虚拟机，供应商建议每个操作系统至少应为 256 MB。
如果要运行这四个具有 512 MB RAM 的虚拟机，则 ESXi 主机
必须具有 4 GB RAM，其中 2048 MB 供虚拟机使用。
这些计算不包括每个虚拟机使用可变开销内存而可能节省的内存
量。请参见《vSphere 资源管理》。
虚拟机专用的快速以太网适配器
将管理网络和虚拟机网络置于不同的物理网卡上。虚拟机的专用
千兆位以太网卡，如 Intel PRO 1000 适配器，可以通过大网络 流量来提高虚拟机的吞吐量。 VMware ESXi 升级 VMware, Inc. 19 [第20页]
表 3-5. 增强性能的建议 （续）
系统元件
建议
磁盘位置
将虚拟机使用的所有数据置于专为虚拟机分配的物理磁盘上。如
果不将虚拟机置于包含 ESXi 引导映像的磁盘上，可获得更优异
的性能。所使用的物理磁盘应该有足够大的空间来容纳所有虚拟
机使用的磁盘映像。
VMFS6 分区
ESXi 安装程序将在找到的第一个空白本地磁盘上创建初始
VMFS 卷。要添加磁盘或修改原始配置，请使用 vSphere
Client。这种做法可确保分区的起始扇区为 64 K 的整数倍，这 可以提高存储的性能。
注 对于仅适用于 SAS 的环境，安装程序可能不会格式化磁
盘。对于某些 SAS 磁盘，可能无法识别是本地磁盘还是远程磁
盘。安装后，您可以使用 vSphere Client 设置 VMFS。 处理器
更快的处理器可以提高 ESXi 性能。对于某些工作负载，更大的
高速缓存可提高 ESXi 的性能。
硬件兼容性
在服务器中使用 ESXi 7.0 驱动程序支持的设备。请参见《硬件
兼容性指南》，网址为 http://www.vmware.com/resources/ compatibility。
ESXi 主机的入站和出站防火墙端口
通过 vSphere Client 和 VMware Host Client，您可以打开和关闭每个服务的防火墙端口或允许来自选定 IP 地址的流量。
ESXi 包括默认启用的防火墙。安装时，会配置 ESXi 防火墙以阻止除主机安全配置文件中启用的服务相关
的流量之外的所有入站和出站流量。有关 ESXi 防火墙中受支持端口和协议的列表，请参见 https://
ports.vmware.com/ 中的 VMware Ports and Protocols Tool™。
VMware Ports and Protocols Tool 将列出默认安装的服务的端口信息。如果在主机上安装其他 VIB，则
可能还会配置其他服务和防火墙端口。这些信息主要用于 vSphere Client 中显示的服务，但是 VMware
Ports and Protocols Tool 还包括其他某些端口。 系统日志记录所需的可用空间
如果使用 Auto Deploy 安装了 ESXi7.0 主机，或如果独立于 VMFS 卷上暂存目录中的默认位置设置日志
目录，则可能需要更改当前日志大小和轮换设置以确保存在足够的空间用于系统日志记录。
所有 vSphere 组件都使用此基础架构。此基础架构中的日志容量的默认值有所不同，具体取决于可用的存
储量和系统日志记录的配置方式。使用 Auto Deploy 部署的主机将日志存储在内存磁盘上，这意味着日志 的可用空间量较小。
如果使用 Auto Deploy 配置主机，则通过以下方式之一重新配置日志存储： n
通过网络将日志重定向至远程收集器。
n
将日志重定向至 NAS 或 NFS 存储。
如果将日志重定向至非默认存储，例如 NAS 或 NFS 存储，可能还要为安装到磁盘的主机重新配置日志大 小和轮换。 VMware ESXi 升级 VMware, Inc. 20 [第21页]
无需为使用默认配置的 ESXi 主机重新配置日志存储，这些主机会将日志存储在 VMFS 卷上的暂存目录
中。对于这些主机，ESXi7.0 会配置最适合安装的日志，并会提供足够的空间来容纳日志消息。
表 3-6. 建议的 hostd、vpxa 和 fdm 日志的最小大小和轮换配置 日志 最大日志文件大小 要保留的轮换数 所需最小磁盘空间 管理代理 (hostd) 10 MB 10 100 MB
VirtualCenter 代理 (vpxa)
5 MB
10
50 MB
vSphere HA 代理（故障域
管理器，fdm）
5 MB
10
50 MB
有关设置和配置 syslog 和 syslog 服务器以及安装 vSphere Syslog Collector 的信息，请参见
《《vCenter Server 安装和设置》》文档。
VMware Host Client 系统要求
确保您的浏览器支持 VMware Host Client。
VMware Host Client 支持以下客户机操作系统和 Web 浏览器版本。 支持的浏览器 Mac OS
Windows 32 位和 64 位版本
Linux
Google Chrome
89+
89+
75+
Mozilla Firefox
80+
80+
60+
Microsoft Edge
90+
90+
不适用
Safari
9.0+
不适用
不适用
ESXi 密码和帐户锁定
对于 ESXi 主机，必须使用符合预定义要求的密码。您可以使用Security.PasswordQualityControl 高
级选项更改所需长度和字符类别要求或允许密码短语。您还可以使用 Security.PasswordHistory 高级选
项设置每个用户要记住的密码数。
注 ESXi 密码的默认要求因版本而异。可以使用 Security.PasswordQualityControl 高级选项检查并更 改默认密码限制。 ESXi 密码
ESXi 对从直接控制台用户界面、ESXi Shell、SSH 或 VMware Host Client 进行的访问强制执行密码要 求。 n
默认情况下，在创建密码时，必须至少包括以下四类字符中三类字符的组合：小写字母、大写字母、数
字和特殊字符（如下划线或短划线）。
n
默认情况下，密码长度至少为 7 个字符，且小于 40 个字符。 n
密码不得包含字典单词或部分字典单词。
VMware ESXi 升级
VMware, Inc.
21
[第22页]
n
密码不得包含用户名或部分用户名。
注 密码开头的大写字母不算入使用的字符类别数。密码结尾的数字不算入使用的字符类别数。密码内使用 的字典词可降低整体密码强度。 ESXi 密码示例
以下候选密码说明选项设置如下时可以使用的密码。
retry=3 min=disabled,disabled,disabled,7,7
使用此设置时，如果新密码不够强或者两次未正确输入密码，则系统最多会提示用户输入三次 (retry=3)。
不允许使用包含一种或两种类别字符的密码，也不允许使用密码短语，因为前三项已禁用。使用三种和四
种类别字符的密码需要 7 个字符。有关其他选项（例如，max、passphrase 等）的详细信息，请参见
pam_passwdqc 手册页。
使用这些设置时，允许使用以下密码。
n
xQaTEhb! ：包含由三类字符组成的八个字符。
n
xQaT3#A：包含由四类字符组成的七个字符。
下列候选密码不符合要求。
n
Xqat3hi：以大写字符开头，将有效字符类别数减少为两种。需要的最少字符类别数为三种。 n
xQaTEh2：以数字结尾，将有效字符种类数减少到两种。需要的最少字符类别数为三种。 ESXi 密码短语
您还可以使用密码短语代替密码，但是，默认情况下，密码短语处于禁用状态。您可以在 vSphere Client
中使用 Security.PasswordQualityControl 高级选项更改默认设置和其他设置。
例如，您可以将该选项更改为以下值。
retry=3 min=disabled,disabled,16,7,7
此示例允许密码短语的长度至少为 16 个字符，且至少包含 3 个单词。
对于旧版主机，仍然支持更改 /etc/pam.d/passwd 文件，但在将来的版本中将不再支持更改此文件。将
来的版本将改用 Security.PasswordQualityControl 高级选项。 更改默认密码限制
您可以使用 ESXi 主机的Security.PasswordQualityControl 高级选项更改密码或密码短语的默认限
制。有关设置 ESXi 高级选项的信息，请参见《vCenter Server 和主机管理》文档。
例如，您可以更改默认设置，要求包含最少 15 个字符和最少 4 个词 (passphrase=4)，如下所示：
retry=3 min=disabled,disabled,15,7,7 passphrase=4 VMware ESXi 升级 VMware, Inc. 22 [第23页]
有关详细信息，请参见 pam_passwdqc 的手册页。
注 并非所有可能的密码组合选项都已经过测试。更改默认密码设置后执行测试。
以下示例设置了密码复杂性要求，要求使用四类字符中的 8 个字符并实现显著的密码差异、记住五个密码
的历史记录以及 90 天轮换策略：
min=disabled,disabled,disabled,disabled,8 similar=deny
将 Security.PasswordHistory 选项设置为 5，并将 Security.PasswordMaxDays 选项设置为 90。 ESXi 帐户锁定行为
对于通过 SSH 和通过 vSphere Web Services SDK 进行的访问，支持帐户锁定。直接控制台界面 (DCUI)
和 ESXi Shell 不支持帐户锁定。默认情况下，最多允许 5 次尝试，当这些尝试均失败后，便会锁定帐户。
默认情况下，帐户将在 15 分钟后解锁。
配置登录行为
可以使用以下高级选项配置 ESXi 主机的登录行为：
n
Security.AccountLockFailures。在锁定用户帐户之前允许的最多失败登录尝试次数。零表示取消 激活帐户锁定。 n
Security.AccountUnlockTime.用户被锁定的秒数。 n
Security.PasswordHistory.要为每个用户记住的密码数。零表示取消激活密码历史记录。
有关设置 ESXi 高级选项的信息，请参见《vCenter Server 和主机管理》文档。 升级 ESXi 主机之前
为成功升级 ESXi 主机，需要了解相关更改并做好准备。
为实现 ESXi 成功升级，请遵循以下最佳做法：
1
请确保了解 ESXi 升级过程、该过程对现有部署的影响以及升级所需的准备。 n
如果 vSphere 系统包括 VMware 解决方案或插件，请确保它们与要升级到的 vCenter Server 版
本兼容。请参见 http://www.vmware.com/resources/compatibility/sim/interop_matrix.php
上的 VMware 产品互操作性列表。
n
请阅读ESXi 主机升级过程概览，了解支持的升级方案以及可用于执行升级的选项和工具。 n
有关已知的安装问题，请阅读《VMware vSphere 发行说明》。 2 准备系统以进行升级。 n
请确保升级操作支持当前的 ESXi 版本。请参见ESXi 主机升级过程概览。 n
请确保系统硬件符合 ESXi 要求。请参见ESXi 要求和《VMware 兼容性指南》（网址为 http://
www.vmware.com/resources/compatibility/search.php）。请查看系统兼容性、I/O 与网络和
主机总线适配器 (HBA) 卡的兼容性、存储兼容性和备份软件兼容性。 VMware ESXi 升级 VMware, Inc. 23 [第24页] n
确保主机上有足够的磁盘空间用于升级。
n
如果 SAN 已连接到主机，请先分离光纤通道系统然后继续升级。请勿在 BIOS 中停用 HBA 卡。 3
请在执行升级之前备份您的主机。如果升级失败，则可以还原主机。
4
如果要使用 Auto Deploy 置备主机，运行该过程的用户必须在所置备的 ESXi 主机上拥有本地管理员
特权。默认情况下，安装过程具有这些特权且证书置备会按预期进行。但如果您使用安装程序以外的其
他方法，则必须以具有本地管理员特权的用户身份运行该过程。
5
根据所选升级选项，可能需要迁移该主机上的所有虚拟机或关闭这些虚拟机的电源。升级方法请参见说 明。 n
从 CD、DVD 或 USB 驱动器进行交互式升级：请参见以交互方式升级主机。 n
脚本式升级：请参见通过使用脚本安装或升级主机。
n
使用 vSphere Auto Deploy：请参见第 4 章 使用 vSphere Auto Deploy 重新置备主机 。如果
ESXi 6.5 x 或 6.7.x 主机是使用 vSphere Auto Deploy 进行部署的，则您可以使用 vSphere
Auto Deploy 通过 7.0 映像重新置备主机。
n
esxcli 命令方法：请参见 使用 ESXCLI 命令升级主机 。 6
计划必须在 ESXi 主机升级后执行的任务：
n
测试系统以确保已成功完成升级。
n
应用主机的许可证。请参见为升级后的 ESXi 主机提供许可。
n
考虑设置用于远程日志记录的 syslog 服务器，以确保具有足够的磁盘存储来存储日志文件。对于
本地存储有限的主机，在远程主机上设置日志记录尤为重要。vSphere Syslog Collector 作为一项
服务包含在 vCenter Server 6.0 中，可用于从所有主机收集日志。请参见系统日志记录所需的可
用空间。有关设置和配置 syslog 和 syslog 服务器、从主机配置文件界面设置 syslog 以及安装
vSphere Syslog Collector 的信息，请参见《vCenter Server 安装和设置》文档。 7
如果升级失败，且已备份主机，则可以还原主机。
升级具有第三方自定义 VIB 的主机
主机可以安装自定义 vSphere 安装包 (VIB)，例如第三方驱动程序或管理代理。将 ESXi 主机升级到 7.0
时，系统将迁移所有受支持的自定义 VIB，不管安装程序 ISO 中是否包含这些 VIB。
如果主机或安装程序 ISO 映像包含的 VIB 会引发冲突和阻止升级，则错误消息会指出引发冲突的 VIB。要
升级主机，请执行以下操作之一：
n
从 ESXi 主机中移除引发冲突的 VIB 并重试升级。您可以使用 esxcli 命令从主机中移除 VIB。有关
详细信息，请参见 从主机中移除 VIB 。
n
使用 vSphere ESXi Image Builder CLI 创建可解决冲突的自定义安装程序 ISO 映像。有关 vSphere
ESXi Image Builder CLI 的详细信息，请参见《《vCenter Server 安装和设置》》文档。 VMware ESXi 升级 VMware, Inc. 24 [第25页]
在具有 VMware NSX-T™ Data Center 的环境中升级 ESXi 主机
如果 vSphere 系统包含 NSX-T Data Center，则在开始升级 ESXi 主机前，必须确保 NSX 内核模块是用
于升级的所需软件规范或基准的一部分。
将 ESXi 主机升级到 7.0 或更高版本时，系统将迁移所有受支持的自定义 VIB，而无论安装程序 ISO 中是
否包含这些 VIB。但是，NSX 内核模块不会自动迁移到安装程序 ISO 映像。在继续执行升级操作之前，必 须执行以下操作之一： n
创建具有新上载 NSX 内核模块的扩展基准。有关详细信息，请参见管理主机和集群生命周期。 n
使用 NSX 内核模块创建自定义映像配置文件。有关详细信息，请参见创建自定义映像配置文件，以在
具有 VMware NSX-T Data Center 的环境中升级 ESXi 主机。 n
使用 PowerCLI 创建新的 ISO 映像。有关详细信息，请参见创建新的 ISO 映像，以在具有 VMware
NSX-T Data Center 的环境中升级 ESXi 主机。 n
使用 ESXCLI。有关详细信息，请参见在具有 VMware NSX-T Data Center 的环境中使用 ESXCLI 升 级 ESXi 主机。
创建自定义映像配置文件，以在具有 VMware NSX-T Data Center 的环境 中升级 ESXi 主机
如果 vSphere 系统包含 NSX-T Data Center，则在开始将 ESXi 主机从早期版本的 ESXi 升级到 7.0 及更
高版本之前，必须确保 NSX 内核模块是用于升级的基准的一部分。为此，您可以使用 ESXi 基础映像和新
上载的 NSX 内核模块创建自定义映像配置文件。
前提条件
n
从 VMware Customer Connect 下载适用于您环境中部署的 NSX-T Data Center 版本的 NSX
Kernel Module for VMware ESXi 7.0 zip 文件。例如，适用于 VMware NSX-T Data Center
3.0.0 的 nsx-lcp-3.0.0.0.0.15945993-esx70.zip。 n
确保已在vCenter Server 系统中启用 Auto Deploy 和 Image Builder。 步骤 1
登录到 vCenter Server 7.0.x 系统。
2
导航到主页 > Autodeploy > 软件库，向 vSphere ESXi Image Builder 清单中导入 ESXi 7.0.x 基础
映像，如果它尚不可用，则导入 NSX 内核模块对应的 ZIP 文件。 3
创建一个映像配置文件，将 NSX-T Data Center NSX 内核模块与 ESX 7.0.x 的基础映像合并在一
起。有关详细步骤，请参见创建映像配置文件。
4
将自定义映像配置文件导出为 ISO 映像。
5
将 ISO 映像导入 vSphere Lifecycle Manager 库。
现在，您可以使用vSphere Lifecycle Manager 基于导入的 ISO 映像创建升级基准。有关 vSphere
Lifecycle Manager 升级工作流（使用基准）的详细信息，请参见《管理主机和集群生命周期》指南。 VMware ESXi 升级 VMware, Inc. 25 [第26页]
创建新的 ISO 映像，以在具有 VMware NSX-T Data Center 的环境中升级 ESXi 主机
如果 vSphere 系统包含 NSX-T Data Center，则在开始将 ESXi 主机从早期版本的 ESXi 升级到 7.0 及更
高版本之前，必须确保 NSX 内核模块是用于升级的软件规范或基准的一部分。为此，可以使用 New-
IsoImage PowerCLI cmdlet 创建新的 ISO 映像，并按照您喜欢的方式执行 ESXi 升级。 前提条件 n
从 VMware Customer Connect 下载适用于您环境中部署的 NSX-T Data Center 版本的 NSX
Kernel Module for VMware ESXi 7.0 zip 文件。例如，适用于 VMware NSX-T Data Center
3.0.0 的 nsx-lcp-3.0.0.0.0.15945993-esx70.zip。 n
安装 PowerCLI 和所有必备软件。请参见 vSphere ESXi Image Builder 安装和用法。 n
确认您有权访问包含要使用的软件规范的软件库。
步骤
u
在 PowerCLI 会话中，运行 New-IsoImage cmdlet 并传递参数 Depots、Destination 和
SoftwareSpec，以生成 ISO 映像。例如 PS C:\Users\Administrator> New-IsoImage -Depots
"C:\VMware-ESXi-7.0U1-16850804-depot.zip","C:\nsx-lcp-3.0.0.0.0.15945993-
esx70.zip", -Destination C:\<your new ISO image name>.iso -SoftwareSpec C:\<your
file name>.json。此命令通过使用 ESXi 基础映像、NSX 内核 zip 文件以及 JSON 文件中所需映像
的软件规范创建新的 ISO 映像。可以使用任意数量的软件库，也可以组合使用脱机和联机软件库。为
了升级到 ESXi 7.0，New-IsoImage cmdlet 会保留 vSphere Lifecycle Manager 所需的 ESXi 7.0.x 的其他元数据。 后续步骤
使用新的 ISO 映像按照您喜欢的方式完成 ESXi 升级。有关vSphere Lifecycle Manager 升级工作流的详
细信息，请参见《管理主机和集群生命周期》指南。
在具有 VMware NSX-T Data Center 的环境中使用 ESXCLI 升级 ESXi 主 机
如果 vSphere 系统包含 NSX-T Data Center，则在开始将 ESXi 主机从早期版本的 ESXi 升级到 7.0 及更
高版本之前，必须确保 NSX 内核模块是用于升级的软件规范或基准的一部分。您可以使用 ESXCLI 命令升
级 ESXi 主机，然后重新安装 NSX 内核模块。
要在包含 NSX-T Data Center 的 vSphere 系统中使用 ESXCLI 升级 ESXi 主机，必须按照使用 ESXCLI
命令升级主机中所述的步骤操作：
前提条件
n
从 VMware Customer Connect 下载适用于您环境中部署的 NSX-T Data Center 版本的 NSX
Kernel Module for VMware ESXi 7.0 zip 文件。例如，适用于 VMware NSX-T Data Center
3.0.0 的 nsx-lcp-3.0.0.0.0.15945993-esx70.zip。 VMware ESXi 升级 VMware, Inc. 26 [第27页] 步骤 1
将 ESXi 主机置于维护模式。有关详细信息，请参见将主机置于维护模式。 2
下载软件库中的 ESXi 7.0.x 映像配置文件，该软件库可以通过 URL 进行访问或在脱机 ZIP 库中获 取。 3
运行 ESXCLI 命令 esxcli software profile update --depot <path-to-depot-file> -p
ESXi-X.X.X-XXXXXX-standard --allow-downgrades --no-sig-check。例如：esxcli software
profile update --depot /vmfs/volumes/5e8fd197-68bce4dc-f8f1-005056af93cf/VMware-
ESXi-7.0.0-15843807-depot.zip -p ESXi-7.0.0-15843807-standard --allow-downgrades --
no-sig-check。有关详细信息，请参见使用映像配置文件升级或更新主机。 4
使用 ESXCLI 命令 esxcli software vib install -d <path_to_kernel_module_file> --no-
sig-check 安装 NSX 内核模块。例如：esxcli software vib install -d /tmp/nsx-
lcp-3.0.0.0.0.15945993-esx70.zip 5 重新引导 ESXi 主机。 6
将ESXi 主机退出维护模式。
引导 ESXi 安装程序的介质选项
要安装 ESXi 的系统必须可以访问 ESXi 安装程序。
ESXi 安装程序支持以下引导介质：
n
从 CD/DVD 引导。请参见将 ESXi 安装程序 ISO 映像下载并刻录至 CD or DVD 。 n
从 USB 闪存驱动器引导。请参见格式化 USB 闪存驱动器以引导 ESXi 安装或升级。 n
从网络引导。#unique_12
n
使用远程管理应用程序从远程位置引导。请参见#unique_34
将 ESXi 安装程序 ISO 映像下载并刻录至 CD or DVD
如果没有 ESXi 安装 CD/DVD，则可以创建一个。
您也可以创建包含自定义安装脚本的安装程序 ISO 映像。请参见 使用自定义安装或升级脚本创建安装程序 ISO 映像。 步骤 1
请按照 下载 ESXi 安装程序 中的过程操作。
2
将 ISO 映像刻录至 CD 或 DVD。
VMware ESXi 升级
VMware, Inc.
27
[第28页]
格式化 USB 闪存驱动器以引导 ESXi 安装或升级
您可以格式化 USB 闪存驱动器以引导 ESXi 安装或升级。
此过程中的说明假设 USB 闪存驱动器被检测为 /dev/sdb。
注 包含安装脚本的 ks.cfg 文件不能位于引导安装或升级所使用的同一个 USB 闪存驱动器上。 前提条件 n
超级用户可以访问的 Linux 计算机
n
Linux 计算机可以检测到的 USB 闪存驱动器
n
ESXi ISO 映像 VMware-VMvisor-Installer-version_number-
build_number.x86_64.iso，其中包括 isolinux.cfg 文件 n
Syslinux 3.86 软件包。其他版本可能与 ESXi 不兼容。 步骤 1
使用 su 或 sudo root 命令引导 Linux，登录并进入超级用户模式。 2
如果您的 USB 闪存驱动器未检测为 /dev/sdb，或者您不确定 USB 闪存驱动器是如何检测到的，请
先确定该闪存驱动器的检测方式。
a
插入 USB 闪存驱动器。
b
在命令行中，运行以下命令以显示当前日志消息。
tail -f /var/log/messages
可以看到以类似以下消息格式显示的标识 USB 闪存驱动器的若干条消息。
Oct 25 13:25:23 ubuntu kernel: [ 712.447080] sd 3:0:0:0: [sdb] Attached SCSI removable disk
在此示例中，sdb 用于标识 USB 设备。如果您设备的标识方式与此不同，请使用该标识替换 sdb。 3
在 USB 闪存驱动器上创建分区表。
/sbin/fdisk /dev/sdb
或者，输入 o 以创建新的空 DOS 分区表。
a
输入 d 删除分区，直至删除所有分区。
b
输入 n 创建遍及整个磁盘的主分区 1。
c
输入 t 将 FAT32 文件系统的类型设置为适当的设置，如 c。 d
输入 a 在分区 1 上设置活动标记。
VMware ESXi 升级
VMware, Inc.
28
[第29页]
e
输入 p 打印分区表。
结果应类似于以下消息。
Disk /dev/sdb: 2004 MB, 2004877312 bytes 255 heads, 63 sectors/track, 243 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes Device Boot Start End Blocks Id
System /dev/sdb1 1 243 1951866 c W95 FAT32 (LBA) f
输入 w 写入分区表并退出程序。
4
使用 FAT32 文件系统格式化 USB 闪存驱动器。
/sbin/mkfs.vfat -F 32 -n USB /dev/sdb1 5
在 USB 闪存驱动器上安装 Syslinux 引导加载程序。
Syslinux 可执行文件和 mbr.bin 文件的位置可能因 Syslinux 版本而异。默认使用以下命令。
/usr/bin/syslinux /dev/sdb1
cat /usr/lib/syslinux/mbr/mbr.bin > /dev/sdb
例如，您可以下载 syslinux-3.86.zip 的副本，解压缩存档，按照其说明编译 syslinux 源代码，
随后如果从下载的目录中运行 syslinux 安装，则可以使用以下命令：
cd ~/Downloads/syslinux-3.86
.mtools/syslinux /dev/sdb1
cat mbr/mbr.bin > /dev/sdb
6
创建一个目标目录并向其挂载 USB 闪存驱动器。
mkdir /usbdisk
mount /dev/sdb1 /usbdisk
7
创建一个源目录并向其挂载 ESXi 安装程序 ISO 映像。
mkdir /esxi_cdrom
mount -o loop VMware-VMvisor-Installer-version_number-build_number.x86_64.iso /esxi_cdrom 8
将 ISO 映像的内容复制到 USB 闪存驱动器。
cp -r /esxi_cdrom/* /usbdisk
9
将 isolinux.cfg 文件重命名为 syslinux.cfg。
mv /usbdisk/isolinux.cfg /usbdisk/syslinux.cfg
10 在 usbdisk/syslinux.cfg 文件中，将 APPEND -c boot.cfg 行编辑为 APPEND -c boot.cfg -p
1 以确保引导加载程序从您在步骤 3 中创建的第一个分区读取文件。分区号可能不同，具体取决于 USB 设备的布局。 VMware ESXi 升级 VMware, Inc. 29 [第30页] 11 卸载 USB 闪存驱动器。
umount /usbdisk
12 卸载安装程序 ISO 映像。
umount /esxi_cdrom
结果
您可以使用 USB 闪存驱动器引导 ESXi 安装程序。
创建 USB 闪存驱动器以存储 ESXi 安装脚本或升级脚本
您可以使用 USB 闪存驱动器存储在 ESXi 的脚本式安装或升级期间使用的 ESXi 安装脚本或升级脚本。
如果安装计算机上有多个 USB 闪存驱动器，则安装软件会在所有已连接的 USB 闪存驱动器上搜索安装或 升级脚本。
此过程中的说明假设 USB 闪存驱动器被检测为 /dev/sdb。
注 请勿将包含安装或升级脚本的 ks 文件存储在引导安装或升级时使用的同一个 USB 闪存驱动器上。 前提条件 n Linux 计算机 n
ESXi 安装或升级脚本 ks.cfg kickstart 文件 n USB 闪存驱动器 步骤 1
将 USB 闪存驱动器附加到可以访问安装或升级脚本的 Linux 计算机。 2 创建分区表。
/sbin/fdisk /dev/sdb
a
键入 d 删除分区，直至将其全部删除。
b
键入 n 创建遍及整个磁盘的主分区 1。
c
键入 t 将 FAT32 文件系统的类型设置为适当的设置，如 c。 VMware ESXi 升级 VMware, Inc. 30 [第31页] d 键入 p 打印分区表。 结果应类似于以下文本：
Disk /dev/sdb: 2004 MB, 2004877312 bytes
255 heads, 63 sectors/track, 243 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Device Boot Start End Blocks Id System
/dev/sdb1 1 243 1951866 c W95 FAT32 (LBA) e 键入 w 写入分区表并退出。 3
使用 FAT32 文件系统格式化 USB 闪存驱动器。
/sbin/mkfs.vfat -F 32 -n USB /dev/sdb1 4
创建一个目标目录并向其挂载 USB 闪存驱动器。
mkdir -p /usbdisk
mount /dev/sdb1 /usbdisk
5
将 ESXi 安装脚本复制到 USB 闪存驱动器。
cp ks.cfg /usbdisk
6
卸载 USB 闪存驱动器。
umount /usbdisk
结果
USB 闪存驱动器中包含 ESXi 的安装或升级脚本。
后续步骤
引导 ESXi 安装程序时，指向安装或升级脚本的 USB 闪存驱动器的位置。请参见 输入引导选项以启动安装
或升级脚本和PXELINUX 配置文件。
使用自定义安装或升级脚本创建安装程序 ISO 映像
您可以使用自身的安装或升级脚本自定义标准的 ESXi 安装程序 ISO 映像。当您引导生成的安装程序 ISO
映像时，此自定义可用于执行无需人工干预的脚本式安装或升级。
另请参见关于安装和升级脚本和 关于 boot.cfg 文件 。 前提条件 n Linux 计算机 n
ESXi ISO 映像 VMware-VMvisor-Installer-7.x.x-XXXXXX.x86_64.iso，其中 7.x.x 表示
要安装的 ESXi 的版本， XXXXXX 表示安装程序 ISO 映像的内部版本号 n
您的自定义安装或升级脚本 KS_CUST.CFG kickstart 文件 VMware ESXi 升级 VMware, Inc. 31 [第32页] 步骤 1
从 VMware 网站下载 ESXi ISO 映像。
2
将 ISO 映像挂载到文件夹中：
mount -o loop VMware-VMvisor-Installer-7.x.x-XXXXXX.x86_64.iso /
esxi_cdrom_mount
XXXXXX 是要安装或升级到的版本的 ESXi 内部版本号。 3
将 esxi_cdrom 的内容复制到另一个文件夹：
cp -r /esxi_cdrom_mount/* /esxi_cdrom 4
将 kickstart 文件复制到 /esxi_cdrom。
cp KS_CUST.CFG /esxi_cdrom
5
（可选） 修改 boot.cfg 文件，以便使用 kernelopt 选项指定安装或升级脚本的位置。
必须使用大写字符提供脚本路径，例如，
kernelopt=runweasel ks=cdrom:/KS_CUST.CFG
要进行 UEFI 引导，您必须修改位于 /efi/boot/ 的 boot.cfg 文件。
安装或升级将变为完全自动的，无需在安装或升级过程中指定 kickstart 文件。 6
使用 mkisofs 或 genisoimage 命令重新创建 ISO 映像。 命令 语法 mkisofs
mkisofs -relaxed-filenames -J -R -o custom_esxi.iso -b
ISOLINUX.BIN -c BOOT.CAT -no-emul-boot -boot-load-size 4
-boot-info-table -eltorito-alt-boot -eltorito-platform efi -b
EFIBOOT.IMG -no-emul-boot /esxi_cdrom genisoimage
genisoimage -relaxed-filenames -J -R -o custom_esxi.iso -b
ISOLINUX.BIN -c BOOT.CAT -no-emul-boot -boot-load-size 4
-boot-info-table -eltorito-alt-boot -e EFIBOOT.IMG -no-emul-
boot /esxi_cdrom
您可以使用此 ISO 安装程序映像进行常规引导或 UEFI 安全引导。但是，vSphere Lifecycle
Manager 无法验证此类 ISO 映像的校验和，因此无法使用 vSphere Lifecycle Manager 工作流将其 用于升级。 结果
ISO 映像包括您的自定义安装或升级脚本。
后续步骤
从 ISO 映像安装 ESXi。
VMware ESXi 升级
VMware, Inc.
32
[第33页]
下载 ESXi 安装程序
下载适用于 ESXi 的安装程序。您可以从 OEM 或 VMware 下载门户获取软件，网址为 https://
my.vmware.com/。
前提条件
在 https://my.vmware.com/web/vmware/ 上创建一个 VMware Customer Connect 帐户。 步骤 1
登录到 VMware Customer Connect。
2
导航到产品和帐户 > 所有产品。
3
找到 VMware vSphere，然后单击下载产品。
4
从选择版本下拉菜单中选择 VMware vSphere 版本。 5
选择 VMware vSphere Hypervisor (ESXi) 的一个版本，然后单击转到下载。 6
下载 ESXi ISO 映像。
有关 ESXi 的评估副本，请转到 https://my.vmware.com/en/group/vmware/evalcenter?p=free- esxi7。
有关 ESXi 的产品修补程序，请参见 VMware 知识库文章 1021623 或转到 https://my.vmware.com/
group/vmware/patch。
7
确认校验和
存储设备名称和标识符
在 ESXi 环境中，每个存储设备由多个名称进行标识。
设备标识符
ESXi 主机使用不同的算法和约定为每个存储设备生成标识符，具体取决于存储类型。 存储提供的标识符
ESXi 主机查询目标存储设备的设备名称。主机从返回的元数据中提取或生成设备的唯一标识符。该标
识符基于特定存储标准，在所有主机之间具有唯一和持久性，且采用以下格式之一： n naa.xxx n eui.xxx n t10.xxx 基于路径的标识符
如果设备未提供标识符，主机将生成 mpx.path 名称，其中 path 代表设备的第一个路径，例如
mpx.vmhba1:C0:T1:L3。此标识符的使用方法可以与存储提供的标识符相同。 VMware ESXi 升级 VMware, Inc. 33 [第34页]
假设本地设备的路径名称唯一时，才会为其创建 mpx. path 标识符。但是，此标识符不是唯一的也不
是永久的，并且每次系统重新启动后都会发生变化。
设备路径通常采用以下格式：
vmhbaAdapter:CChannel:TTarget:LLUN n
vmhbaAdapter 是存储适配器的名称。此名称指的是主机上的物理适配器，而不是由虚拟机使用 的 SCSI 控制器。 n
CChannel 是存储通道号。
软件 iSCSI 适配器和从属硬件适配器使用通道号来显示到同一目标的多个路径。 n
TTarget 为目标号。目标编号由主机确定，对主机可见的目标的映射更改时，编号也可能更改。由
不同主机共享的目标可能没有相同的目标号。
n
LLUN 是显示目标中 LUN 位置的 LUN 号。LUN 号由存储系统提供。如果目标只有一个 LUN，
则 LUN 号始终为零 (0)。
例如，vmhba1:C0:T3:L1 表示通过存储适配器 vmhba1 和通道 0 访问的目标 3 上的 LUN 1。 旧标识符
除了设备提供的标识符或 mpx.Path 标识符，ESXi 还会为每个设备生成一个备用的旧名称。标识符具 有以下格式： vml.number
旧标识符包含一系列对于设备唯一的数字。可以从通过 SCSI INQUIRY 命令获取的元数据部分派生出
标识符。对于未提供 SCSI INQUIRY 标识符的非本地设备，使用 vml.number 标识符作为唯一可用的 标识符。
示例： 在 vSphere CLI 中显示设备名称
您可以在 vSphere CLI 中使用 esxcli storage core device list 命令显示所有设备名称。输出与 下例类似：
# esxcli storage core device list
naa.XXX
Display Name: DGC Fibre Channel Disk(naa.XXX) ...
Other UIDs: vml.000XXX
mpx.vmhba1:C0:T0:L0
Display Name: Local VMware Disk (mpx.vmhba1:C0:T0:L0) ...
Other UIDs: vml.0000000000XYZ
VMware ESXi 升级
VMware, Inc.
34
[第35页]
以交互方式升级主机
要将 ESXi 6.5 主机或 ESXi 6.7 主机升级到 ESXi 7.0，可从 CD、DVD 或 USB 闪存驱动器引导 ESXi 安 装程序。
在升级之前，请考虑断开网络存储的连接。此操作可缩短安装程序搜索可用磁盘驱动器的时间。断开网络
存储时，断开连接的磁盘上的任何文件在安装时都不可用。请勿断开包含现有 ESXi 安装的 LUN。 前提条件 n
验证 ESXi 安装程序 ISO 是否位于以下其中一个位置。
n
CD 或 DVD 上。如果没有安装 CD 或 DVD，则可以创建一个 CD 或 DVD。请参见将 ESXi 安装
程序 ISO 映像下载并刻录至 CD or DVD
n
USB 闪存驱动器上。请参见格式化 USB 闪存驱动器以引导 ESXi 安装或升级
注 也可使用 PXE 引导 ESXi 安装程序以运行交互式安装或脚本式安装。请参见网络引导安装过程概 述。 n
验证服务器硬件时钟已设置为 UTC。此设置位于系统 BIOS 中。 n
ESXi Embedded 不得位于主机上。ESXi Installable 和 ESXi Embedded 不能存在于同一主机上。 n
如果要升级 ESXi 主机，则将迁移未包含在 ESXi 安装程序 ISO 中的受支持自定义 VIB。请参见升级具
有第三方自定义 VIB 的主机
n
有关更改引导顺序的信息，请参见硬件供应商文档。
步骤
1
将 ESXi 安装程序 CD 或 DVD 插入 CD-ROM 或 DVD-ROM 驱动器，或连接安装程序 USB 闪存驱动 器并重新启动计算机。 2
将 BIOS 设置为从 CD-ROM 设备或 USB 闪存驱动器引导。 3
在“选择磁盘”面板中，选择要在其上安装或升级 ESXi 的驱动器，然后按 Enter。
按 F1 可获取所选磁盘的相关信息。
注 选择磁盘时，请勿依赖于列表中的磁盘顺序。磁盘顺序由 BIOS 决定。在连续添加和移除驱动器的 系统中，磁盘顺序可能不当。 4
如果安装程序找到现有 ESXi 安装和 VMFS 数据存储，请升级或安装 ESXi。
如果无法保留现有的 VMFS 数据存储，则只能选择安装 ESXi 并覆盖现有 VMFS 数据存储，或者取消
安装。如果选择覆盖现有的 VMFS 数据存储，请首先备份该数据存储。 5 按 F11 确认并开始升级。 6
升级完成后，取出安装 CD、DVD 或 USB 闪存驱动器。
7
按 Enter 重新引导主机。
8
将第一引导设备设置为之前升级 ESXi 所选的驱动器。
VMware ESXi 升级
VMware, Inc.
35
[第36页]
通过使用脚本安装或升级主机
通过使用无需人工干预的脚本式安装或升级快速部署 ESXi 主机。脚本式安装或升级可提供高效的多主机部 署方式。
安装或升级脚本包含 ESXi 的安装设置。可以将该脚本应用到您希望拥有相似配置的所有主机上。
对于脚本式安装或升级，必须使用支持的命令创建脚本。可以编辑脚本，以更改每台主机独有的设置。
安装或升级脚本可驻留在以下位置之一：
n
FTP 服务器
n
HTTP/HTTPS 服务器
n
NFS 服务器
n
USB 闪存驱动器
n
CD-ROM 驱动器
输入引导选项以启动安装或升级脚本
通过在 ESXi 安装程序引导命令行中键入引导选项，可以启动安装或升级脚本。
在引导时，可能需要指定访问 kickstart 文件的选项。可通过在引导加载程序中按 Shift+O 来输入引导选
项。对于 PXE 引导安装，可以通过 boot.cfg 文件的 kernelopts 行来传递选项。请参见 关于 boot.cfg
文件 和#unique_12。
要指定安装脚本的位置，请设置 ks=filepath 选项，其中 filepath 指示 kickstart 文件的位置。否则，不
会启动脚本式安装或升级。如果省略 ks=filepath，将运行文本安装程序。
引导选项 中列出了受支持的引导选项。
步骤
1
启动主机。
2
出现 ESXi 安装程序窗口时，请按 Shift+O 编辑引导选项。 3
在 runweasel 命令提示符处，键入
ks=location of installation script plus boot command-line options。 VMware ESXi 升级 VMware, Inc. 36 [第37页] 示例： 引导选项 请键入以下引导选项：
ks=http://00.00.00.00/kickstart/ks-osdc-pdp101.cfg nameserver=00.00.0.0 ip=00.00.00.000
netmask=255.255.255.0 gateway=00.00.00.000 引导选项
在执行脚本式安装时，可能需要在引导时指定访问 kickstart 文件的选项。 支持的引导选项
表 3-7. 适用于 ESXi 安装的引导选项
引导选项
描述
BOOTIF=hwtype-MAC address
类似于 netdevice 选项，syslinux.org 站点中 SYSLINUX
下的 IPAPPEND 选项中所述的 PXELINUX 格式除外。
gateway=ip address
将此网关设为用于下载安装脚本和安装介质的默认网关。
ip=ip address
设置要用于下载安装脚本和安装介质的静态 IP 地址。注意：该
选项的 PXELINUX 格式也受支持。请参见 syslinux.org 站
点中 SYSLINUX 下的 IPAPPEND 选项。
ks=cdrom:/path
使用位于 CD-ROM 驱动器中的 CD 的 path 下的脚本执行脚本
式安装。在找到与路径匹配的文件之前，会挂载并检查每个
CDROM。
重要说明 如果您已通过自定义安装或升级脚本创建安装程序
ISO 映像，则必须使用大写字符提供脚本路径，例如
ks=cdrom:/KS_CUST.CFG。
ks=file://path
使用 path 下的脚本执行脚本式安装。
ks=protocol://serverpath
使用位于给定 URL 的网络上的脚本执行脚本式安装。protocol
可以是 http、https、ftp 或 nfs。下面是使用 NFS 协议的一
个示例：ks=nfs://host/porturl-path。在 RFC 2224 中指定 NFS URL 的格式。 ks=usb
通过从附加的 USB 驱动器访问脚本来执行脚本式安装。搜索名
为 ks.cfg 的文件。此文件必须位于驱动器的 root 目录中。如
果附加了多个 USB 闪存驱动器，则在找到 ks.cfg 文件之前会
搜索这些驱动器。仅支持 FAT16 和 FAT32 文件系统。 ks=usb:/path
使用位于 USB 上的指定路径下的脚本文件执行脚本式安装。
ksdevice=device
查找安装脚本和安装介质时尝试使用网络适配器 device。指定为
MAC 地址（如 00:50:56:C0:00:01）。此位置也可以是
vmnicNN 名称。如果未进行指定并且需要通过网络检索文件，
则安装程序会默认使用最先发现的插入的网络适配器。
nameserver=ip address
指定要用于下载安装脚本和安装介质的域名服务器。
VMware ESXi 升级
VMware, Inc.
37
[第38页]
表 3-7. 适用于 ESXi 安装的引导选项 （续）
引导选项
描述
netdevice=device
查找安装脚本和安装介质时尝试使用网络适配器 device。指定为
MAC 地址（如 00:50:56:C0:00:01）。此位置也可以是
vmnicNN 名称。如果未进行指定并且需要通过网络检索文件，
则安装程序会默认使用最先发现的插入的网络适配器。
netmask=subnet mask
指定用于下载安装脚本和安装介质的网络接口的子网掩码。
vlanid=vlanid
配置位于指定 VLAN 上的网卡。
systemMediaSize=small
限制引导介质上系统存储分区的大小。所选值必须符合您的系统
用途。可以从以下值中进行选择：
n
min（32 GB，适用于单个磁盘或嵌入式服务器）
n
small（64 GB，适用于至少具有 512 GB RAM 的服务器） n
default (128 GB)
n
max（适用于多 TB 服务器，使用所有可用空间）
注 GB 单位为 2^30 字节或 1024*1024*1024 字节的倍数。
有关安装后 ESXi 引导选项的详细信息，请参见 VMware 知识库文章 77009。 关于安装和升级脚本
安装/升级脚本是一个包含支持命令的文本文件，例如 ks.cfg。
此脚本的命令部分包含 ESXi 安装选项。该部分必不可少，且必须位于脚本的开头。 安装脚本或升级脚本支持的位置
在脚本式安装和升级中，ESXi 安装程序可从多个位置访问安装或升级脚本（也称为 kickstart 文件）。 安装或升级脚本支持以下位置： n
CD/DVD。请参见 使用自定义安装或升级脚本创建安装程序 ISO 映像。 n
USB 闪存驱动器。请参见创建 USB 闪存驱动器以存储 ESXi 安装脚本或升级脚本。 n
可通过以下协议访问的网络位置：NFS、HTTP、HTTPS、FTP 安装或升级脚本的路径
可以指定安装或升级脚本的路径。
ks=http://XXX.XXX.XXX.XXX/kickstart/KS.CFG 为 ESXi 安装脚本的路径，其中
XXX.XXX.XXX.XXX 是脚本所驻留的计算机的 IP 地址。请参见关于安装和升级脚本。
要在交互式安装中启动安装脚本，需要手动输入 ks= 选项。请参见 输入引导选项以启动安装或升级脚本。 VMware ESXi 升级 VMware, Inc. 38 [第39页] 安装和升级脚本命令
要修改默认安装或升级脚本或者创建自己的脚本，请使用支持的命令。使用安装脚本中支持的命令，这些
命令是在引导安装程序时使用引导命令指定的。
要确定要安装或升级 ESXi 的磁盘，安装脚本需要以下命令之一：install、upgrade 或
installorupgrade。install 命令创建默认分区，包括在创建其他分区后占据所有可用空间的 VMFS 数据存储。
accepteula 或 vmaccepteula（必需）
接受 ESXi 许可协议。
clearpart（可选）
清除磁盘上现有的任何分区。需要指定 install 命令。请小心编辑现有脚本中的 clearpart 命令。 --drives= 移除指定驱动器上的分区。 --alldrives
忽略 --drives= 要求，并允许在每个驱动器上清除分区。
--ignoredrives=
在除指定驱动器以外的所有驱动器上移除分区。除非指定了 --drives= 或
--alldrives 标记，否则需要使用此命令。
--overwritevmfs
允许覆盖指定驱动器上的 VMFS 分区。默认情况下，不允许覆盖 VMFS 分 区。 --firstdisk= disk-type1
[disk-type2,...]
对最先找到的合格磁盘进行分区。默认情况下，合格磁盘按以下顺序排列： 1
本地连接的存储 (local)
2
网络存储 (remote)
3
USB 磁盘 (usb)
可以使用附加到参数的逗号分隔列表更改磁盘的顺序。如果提供筛选列表，
则会覆盖默认设置。可组合筛选器以指定特定磁盘，包括安装有 ESXi 的第
一个磁盘的 esx、型号和供应商信息，或 VMkernel 设备驱动程序的名称。
例如，要首选使用型号名称为 ST3120814A 的磁盘，及使用 mptsas 驱动程
序的任何磁盘，而非普通本地磁盘，参数为
--firstdisk=ST3120814A,mptsas,local。可以对包含 ESXi 映像的本地
存储使用 localesx，或对包含 ESXi 映像的远程存储使用 remoteesx。 dryrun（可选）
解析并检查安装脚本。不执行安装。
VMware ESXi 升级
VMware, Inc.
39
[第40页]
安装
指定这是全新安装。需要 install、upgrade 或 installorupgrade 命令来确定要在其上安装或升级 ESXi 的磁盘。
--disk= or --drive=
指定要分区的磁盘。在命令 --disk=diskname 中，diskname 可以是磁盘
名称，也可以是 ESXi 中的完整磁盘文件系统路径，例如：
n
磁盘名称：--disk=naa.6d09466044143600247aee55ca2a6405 或 n
设备路径：--disk=/vmfs/devices/disks/mpx.vmhba1:C0:T0:L0
有关可接受的磁盘名称格式，请参见磁盘设备名称。
--firstdisk=
disk-type1,
[disk-type2,...]
对最先找到的合格磁盘进行分区。默认情况下，合格磁盘按以下顺序排列： 1
本地连接的存储 (local)
2
网络存储 (remote)
3
USB 磁盘 (usb)
可以使用附加到参数的逗号分隔列表更改磁盘的顺序。如果提供筛选列表，
则会覆盖默认设置。可组合使用筛选器以指定特定磁盘，包括安装有 ESX 的
第一个磁盘的 esx、型号和供应商信息，或 VMkernel 设备驱动程序的名
称。例如，要首选使用型号名称为 ST3120814A 的磁盘，及使用 mptsas 驱
动程序的任何磁盘，而非普通本地磁盘，参数为
--firstdisk=ST3120814A,mptsas,local。可以对包含 ESXi 映像的本地
存储使用 localesx，或对包含 ESXi 映像的远程存储使用 remoteesx。 --ignoressd
从有资格进行分区的磁盘中排除固态磁盘。此选项可与 install 命令和
--firstdisk 选项配合使用。此选项优先于 --firstdisk 选项。此选项与
--drive 或 --disk 选项以及 upgrade 和 installorupgrade 命令一起
使用时无效。有关防止在自动分区期间进行 SSD 格式化的详细信息，请参
见 《vSphere 存储》文档。
--overwritevsan
在 vSAN 磁盘组中的 SSD 或 HDD（磁性）磁盘上安装 ESXi 时，必须使用
--overwritevsan 选项。如果使用此选项，但选定磁盘上不存在 vSAN 分
区，安装将失败。在 vSAN 磁盘组中的磁盘上安装 ESXi 时，结果取决于选 择的磁盘： n
如果选择 SSD，则同一磁盘组中的 SSD 和所有底层 HDD 会被擦除。 n
如果选择的是 HDD，并且磁盘组有两个以上磁盘，则只有选定的 HDD 才会被清除。 n
如果选择的是 HDD 磁盘，并且磁盘组的磁盘不超过两个，则 SSD 和选 定的 HDD 会被清除。
有关管理 vSAN 磁盘组的详细信息，请参见《《vSphere 存储》》文档。
--overwritevmfs
安装前要覆盖磁盘上的现有 VMFS 数据存储时需要。
VMware ESXi 升级
VMware, Inc.
40
[第41页]
--preservevmfs
安装期间保留磁盘上的现有 VMFS 数据存储。
--novmfsondisk
防止在该磁盘上创建 VMFS 分区。如果磁盘上存在 VMFS 分区，则必须与
--overwritevmfs 一起使用。
installorupgrade
需要 install、upgrade 或 installorupgrade 命令来确定要在其上安装或升级 ESXi 的磁盘。
--disk= or --drive=
指定要分区的磁盘。在命令 --disk=diskname 中，diskname 可以是磁盘
名称，也可以是 ESXi 中的完整磁盘文件系统路径，例如：
n
磁盘名称：--disk=naa.6d09466044143600247aee55ca2a6405 或 n
设备路径：--disk=/vmfs/devices/disks/mpx.vmhba1:C0:T0:L0
有关可接受的磁盘名称格式，请参见磁盘设备名称。
--firstdisk=
disk-type1,
[disk-type2,...]
对最先找到的合格磁盘进行分区。默认情况下，合格磁盘按以下顺序排列： 1
本地连接的存储 (local)
2
网络存储 (remote)
3
USB 磁盘 (usb)
可以使用附加到参数的逗号分隔列表更改磁盘的顺序。如果提供筛选列表，
则会覆盖默认设置。可组合使用筛选器以指定特定磁盘，包括安装有 ESX 的
第一个磁盘的 esx、型号和供应商信息，或 VMkernel 设备驱动程序的名
称。例如，要首选使用型号名称为 ST3120814A 的磁盘，及使用 mptsas 驱
动程序的任何磁盘，而非普通本地磁盘，参数为
--firstdisk=ST3120814A,mptsas,local。可以对包含 ESXi 映像的本地
存储使用 localesx，或对包含 ESXi 映像的远程存储使用 remoteesx。
--overwritevsan
在 vSAN 磁盘组中的 SSD 或 HDD（磁性）磁盘上安装 ESXi 时，必须使用
--overwritevsan 选项。如果使用此选项，但选定磁盘上不存在 vSAN 分
区，安装将失败。在 vSAN 磁盘组中的磁盘上安装 ESXi 时，结果取决于选 择的磁盘： n
如果选择 SSD，则同一磁盘组中的 SSD 和所有底层 HDD 会被擦除。 n
如果选择的是 HDD，并且磁盘组有两个以上磁盘，则只有选定的 HDD 才会被清除。 n
如果选择的是 HDD 磁盘，并且磁盘组的磁盘不超过两个，则 SSD 和选 定的 HDD 会被清除。
有关管理 vSAN 磁盘组的详细信息，请参见《《vSphere 存储》》文档。
--overwritevmfs
安装 ESXi（如果磁盘上存在 VMFS 分区，但不存在 ESX 或 ESXi 安装）。
除非存在该选项，否则当磁盘上存在 VMFS 分区但 ESX 或 ESXi 安装缺失 时，安装程序会失败。 VMware ESXi 升级 VMware, Inc. 41 [第42页] keyboard（可选） 设置系统的键盘类型。 keyboardType
指定所选键盘类型的键盘映射。keyboardType 必须是下列类型之一。 n 比利时语 n 葡萄牙语 (巴西) n 克罗地亚语 n 捷克斯洛伐克语 n 丹麦语 n 爱沙尼亚语 n 芬兰语 n 法语 n 德语 n 希腊语 n 冰岛语 n 意大利语 n 日语 n 拉丁美洲语 n 挪威语 n 波兰语 n 葡萄牙语 n 俄语 n 斯洛文尼亚语 n 西班牙语 n 瑞典语 n 瑞士法语 n 瑞士德语 n 土耳其语 n 乌克兰语 n 英式英语 n 美式英语 (默认) n 美式英语 Dvorak VMware ESXi 升级 VMware, Inc. 42 [第43页]
serialnum 或 vmserialnum（可选）
ESXi 版本 5.1 及更高版本支持该命令。配置许可。如果不包括此命令，ESXi 将以评估模式安装。
--esx=<license-key>
指定要使用的 vSphere 许可证密钥。格式为 5 个组，每个组包含五个字符
(XXXXX-XXXXX-XXXXX-XXXXX-XXXXX)。 network（可选） 指定系统的网络地址。
--bootproto=[dhcp|
static]
指定是从 DHCP 获得网络设置还是手动对其进行设置。
--device=
以 vmnicNN 形式（如 vmnic0）指定网卡的 MAC 地址或设备名称。该选项
指的是虚拟交换机的上行链路设备。
--ip=
以 xxx.xxx.xxx.xxx 形式为要安装的计算机设置 IP 地址。需要与
--bootproto=static 选项配合使用，否则将被忽略。 --gateway=
以 xxx.xxx.xxx.xxx 形式将默认网关指定为 IP 地址。与
--bootproto=static 选项配合使用。
--nameserver=
将主名称服务器指定为 IP 地址。与 --bootproto=static 选项配合使用。
如果不打算使用 DNS，请忽略此选项。
--nameserver 选项可以接受两个 IP 地址。例如：--
nameserver="10.126.87.104[,10.126.87.120]" --netmask=
以 255.xxx.xxx.xxx 形式指定所安装系统的子网掩码。与 --
bootproto=static 选项配合使用。
--hostname=
指定所安装系统的主机名。
--vlanid= vlanid
指定系统所处的 VLAN。与 --bootproto=dhcp 或 --bootproto=static
选项配合使用。设置为 1 到 4096 的一个整数。
--addvmportgroup=(0|1)
指定是否添加虚拟机使用的虚拟机网络端口组。默认值为 1。
paranoid（可选）
引发警告消息从而中断安装。如果省略此命令，则系统会记录警告消息。 VMware ESXi 升级 VMware, Inc. 43 [第44页]
part 或 partition（可选）
在系统上创建额外的 VMFS 数据存储。每个磁盘只能创建一个数据存储。不能与 install 命令在同一个
磁盘上使用。一个磁盘只能指定一个分区，并且只能是 VMFS 分区。 datastore name 指定分区的挂载位置。
--ondisk= or --ondrive=
指定创建分区的磁盘或驱动器。
--firstdisk=
disk-type1,
[disk-type2,...]
对最先找到的合格磁盘进行分区。默认情况下，合格磁盘按以下顺序排列： 1
本地连接的存储 (local)
2
网络存储 (remote)
3
USB 磁盘 (usb)
可以使用附加到参数的逗号分隔列表更改磁盘的顺序。如果提供筛选列表，
则会覆盖默认设置。可组合使用筛选器以指定特定磁盘，包括安装有 ESX 的
第一个磁盘的 esx、型号和供应商信息，或 VMkernel 设备驱动程序的名
称。例如，要首选使用型号名称为 ST3120814A 的磁盘，及使用 mptsas 驱
动程序的任何磁盘，而非普通本地磁盘，参数为
--firstdisk=ST3120814A,mptsas,local。可以对包含 ESXi 映像的本地
存储使用 localesx，或对包含 ESXi 映像的远程存储使用 remoteesx。 reboot（可选）
脚本式安装完成后重新引导计算机。
<--noeject>
安装完成后不弹出 CD。
rootpw（必需）
设置系统的 root 密码。
--iscrypted
指定加密该密码。
password
指定密码值。
升级
需要 install、upgrade 或 installorupgrade 命令来确定要在其上安装或升级 ESXi 的磁盘。
--disk= or --drive=
指定要分区的磁盘。在命令 --disk=diskname 中，diskname 可以是磁盘
名称，也可以是 ESXi 中的完整磁盘文件系统路径，例如：
n
磁盘名称：--disk=naa.6d09466044143600247aee55ca2a6405 或 n
设备路径：--disk=/vmfs/devices/disks/mpx.vmhba1:C0:T0:L0 VMware ESXi 升级 VMware, Inc. 44 [第45页]
有关可接受的磁盘名称格式，请参见磁盘设备名称。
--firstdisk=
disk-type1,
[disk-type2,...]
对最先找到的合格磁盘进行分区。默认情况下，合格磁盘按以下顺序排列： 1
本地连接的存储 (local)
2
网络存储 (remote)
3
USB 磁盘 (usb)
可以使用附加到参数的逗号分隔列表更改磁盘的顺序。如果提供筛选列表，
则会覆盖默认设置。可组合使用筛选器以指定特定磁盘，包括安装有 ESX 的
第一个磁盘的 esx、型号和供应商信息，或 VMkernel 设备驱动程序的名
称。例如，要首选使用型号名称为 ST3120814A 的磁盘，及使用 mptsas 驱
动程序的任何磁盘，而非普通本地磁盘，参数为
--firstdisk=ST3120814A,mptsas,local。可以对包含 ESXi 映像的本地
存储使用 localesx，或对包含 ESXi 映像的远程存储使用 remoteesx。
%include 或 include（可选）
指定要解析的另一个安装脚本。该命令的处理方式类似于多行命令，但仅使用一个参数。 filename
例如：%include part.cfg
%pre（可选）
指定在评估 kickstart 配置之前要运行的脚本。例如，可使用其生成 kickstart 文件要包含的文件。 --interpreter
=[python|busybox]
指定要使用的解释程序。默认为 busybox。
%post（可选）
软件包安装完成后，运行指定的脚本。如果指定多个 %post 部分，则它们将按照在安装脚本中显示的顺序 依次运行。 --interpreter
=[python|busybox]
指定要使用的解释程序。默认为 busybox。
--timeout=secs
指定用于运行脚本的超时时间。如果超时时间到达后脚本仍未完成，则会强 制停止脚本。
--ignorefailure
=[true|false]
如果值为 true，则即使 %post 脚本停止并显示错误，安装仍将视为成功。 VMware ESXi 升级 VMware, Inc. 45 [第46页] %firstboot
创建仅在首次引导期间运行的 init 脚本。该脚本不会对后续引导造成影响。如果指定多个 %firstboot
部分，则它们将按照在 kickstart 文件中显示的顺序依次运行。
注 在系统首次引导之前，无法检查 %firstboot 脚本的语义。安装完成之前，%firstboot 脚本可能包 含未公开的潜在灾难性错误。
重要说明 如果在 ESXi 主机上启用安全引导，%firstboot 脚本不会运行。 --interpreter
=[python|busybox]
指定要使用的解释程序。默认为 busybox。
注 在系统首次引导之前，无法检查 %firstboot 脚本的语义。如果该脚本包含错误，则直到安装完成才 会显示这些错误。 磁盘设备名称
install、upgrade 和 installorupgrade 安装脚本命令需要使用磁盘设备名称。 表 3-8. 磁盘设备名称 格式 示例 描述 NAA
naa.6d09466044143600247aee55ca2a6405
SCSI INQUIRY 标识符
EUI
eui.3966623838646463
SCSI INQUIRY 标识符
T10
t10.SanDisk00Cruzer_Blade000000004C5300 01171118101244
SCSI INQUIRY 标识符
VML
vml.00025261
旧版 VMkernel 标识符
MPX
mpx.vmhba0:C0:T0:L0
基于路径的标识符
有关存储设备名称的详细信息，请参见《vSphere 存储》文档中的存储设备名称和标识符。 存储设备名称和标识符
在 ESXi 环境中，每个存储设备由多个名称进行标识。
设备标识符
ESXi 主机使用不同的算法和约定为每个存储设备生成标识符，具体取决于存储类型。 存储提供的标识符
ESXi 主机查询目标存储设备的设备名称。主机从返回的元数据中提取或生成设备的唯一标识符。该标
识符基于特定存储标准，在所有主机之间具有唯一和持久性，且采用以下格式之一： n naa.xxx n eui.xxx VMware ESXi 升级 VMware, Inc. 46 [第47页] n t10.xxx 基于路径的标识符
如果设备未提供标识符，主机将生成 mpx.path 名称，其中 path 代表设备的第一个路径，例如
mpx.vmhba1:C0:T1:L3。此标识符的使用方法可以与存储提供的标识符相同。
假设本地设备的路径名称唯一时，才会为其创建 mpx. path 标识符。但是，此标识符不是唯一的也不
是永久的，并且每次系统重新启动后都会发生变化。
设备路径通常采用以下格式：
vmhbaAdapter:CChannel:TTarget:LLUN n
vmhbaAdapter 是存储适配器的名称。此名称指的是主机上的物理适配器，而不是由虚拟机使用 的 SCSI 控制器。 n
CChannel 是存储通道号。
软件 iSCSI 适配器和从属硬件适配器使用通道号来显示到同一目标的多个路径。 n
TTarget 为目标号。目标编号由主机确定，对主机可见的目标的映射更改时，编号也可能更改。由
不同主机共享的目标可能没有相同的目标号。
n
LLUN 是显示目标中 LUN 位置的 LUN 号。LUN 号由存储系统提供。如果目标只有一个 LUN，
则 LUN 号始终为零 (0)。
例如，vmhba1:C0:T3:L1 表示通过存储适配器 vmhba1 和通道 0 访问的目标 3 上的 LUN 1。 旧标识符
除了设备提供的标识符或 mpx.Path 标识符，ESXi 还会为每个设备生成一个备用的旧名称。标识符具 有以下格式： vml.number
旧标识符包含一系列对于设备唯一的数字。可以从通过 SCSI INQUIRY 命令获取的元数据部分派生出
标识符。对于未提供 SCSI INQUIRY 标识符的非本地设备，使用 vml.number 标识符作为唯一可用的 标识符。
示例： 在 vSphere CLI 中显示设备名称
您可以在 vSphere CLI 中使用 esxcli storage core device list 命令显示所有设备名称。输出与 下例类似：
# esxcli storage core device list
naa.XXX
Display Name: DGC Fibre Channel Disk(naa.XXX) ...
Other UIDs: vml.000XXX
mpx.vmhba1:C0:T0:L0
Display Name: Local VMware Disk (mpx.vmhba1:C0:T0:L0) ...
Other UIDs: vml.0000000000XYZ
VMware ESXi 升级
VMware, Inc.
47
[第48页]
关于 boot.cfg 文件
引导加载程序配置文件 boot.cfg 指定 mboot.c32 或 mboot.efi 引导加载程序在 ESXi 安装中使用的 内核、内核选项以及引导模块。
ESXi 安装程序中提供了 boot.cfg 文件。您可以修改 boot.cfg 文件的 kernelopt 行，以便指定安装脚 本的位置或传递其他引导选项。
boot.cfg 文件的语法如下：
# boot.cfg -- mboot configuration file
#
# Any line preceded with '#' is a comment.
title=STRING
prefix=DIRPATH
kernel=FILEPATH
kernelopt=STRING
modules=FILEPATH1 --- FILEPATH2... --- FILEPATHn
# Any other line must remain unchanged.
boot.cfg 中的命令配置引导加载程序。
表 3-9. boot.cfg 中的命令。
命令
描述
title=STRING
将引导加载程序标题设置为 STRING。
prefix=STRING
（可选）在尚未以 / 或 http:// 开头的 kernel= 和 modules=
命令中，在每个 FILEPATH 前面添加 DIRPATH/。
kernel=FILEPATH
将内核路径设置为 FILEPATH。
kernelopt=STRING
将 STRING 附加到内核引导选项。
modules=FILEPATH1 --- FILEPATH2... --- FILEPATHn
列出要加载的模块，用三个连字符 (---) 分隔。
请参见 使用自定义安装或升级脚本创建安装程序 ISO 映像和#unique_12。
使用脚本从 CD 或 DVD 安装或升级 ESXi
可以使用指定安装或升级选项的脚本从 CD-ROM 或 DVD-ROM 驱动器安装或升级 ESXi。
可通过在启动主机时输入引导选项来启动安装或升级脚本。您也可以创建包含安装脚本的安装程序 ISO 映
像。使用安装程序 ISO 映像，可在引导结果安装程序 ISO 映像时，执行无需人工干预的脚本式安装。请参
见 使用自定义安装或升级脚本创建安装程序 ISO 映像。
前提条件
运行脚本式安装或升级之前，请确认是否满足以下必备条件：
n
要在其上进行安装或升级的系统满足相应的硬件要求。请参见ESXi 硬件要求。 VMware ESXi 升级 VMware, Inc. 48 [第49页] n
安装 CD 或 DVD 上有 ESXi 安装程序 ISO。请参见将 ESXi 安装程序 ISO 映像下载并刻录至 CD or DVD 。 n
系统可以访问默认安装或升级脚本 (ks.cfg) 或者自定义安装或升级脚本。请参见关于安装和升级脚 本。 n
已选择引导命令来运行脚本式安装或升级。请参见 输入引导选项以启动安装或升级脚本。有关引导命
令的完整列表，请参见 引导选项 。
步骤
1
从本地 CD-ROM 或 DVD-ROM 驱动器引导 ESXi 安装程序。 2
出现 ESXi 安装程序窗口时，请按 Shift+O 编辑引导选项。 3
键入称为默认安装或升级脚本的引导选项，或您创建的安装或升级脚本文件。 引导选项的格式为 ks=。 4 按 Enter。 结果
安装、升级或迁移过程应用您所指定的选项运行。
使用脚本从 USB 闪存驱动器安装或升级 ESXi
可以使用指定安装或升级选项的脚本从 USB 闪存驱动器安装或升级 ESXi。
引导选项 中列出了受支持的引导选项。
前提条件
运行脚本式安装或升级之前，请确认是否满足以下必备条件：
n
安装或升级到 ESXi 的系统满足安装或升级的硬件要求。请参见ESXi 硬件要求。 n
可引导的 USB 闪存驱动器上有 ESXi 安装程序 ISO。请参见格式化 USB 闪存驱动器以引导 ESXi 安装 或升级。 n
系统可以访问默认安装或升级脚本 (ks.cfg) 或者自定义安装或升级脚本。请参见关于安装和升级脚 本。 VMware ESXi 升级 VMware, Inc. 49 [第50页] n
已选择引导选项来运行脚本式安装、升级或迁移。请参见 输入引导选项以启动安装或升级脚本。 步骤 1
从 USB 闪存驱动器引导 ESXi 安装程序。
2
出现 ESXi 安装程序窗口时，请按 Shift+O 编辑引导选项。 3
键入称为默认安装或升级脚本的引导选项，或您创建的安装或升级脚本文件。 引导选项的格式为 ks=。 4 按 Enter。 结果
安装、升级或迁移过程应用您所指定的选项运行。
利用通过网络引导安装程序执行 ESXi 脚本式安装或升级
ESXi 7.0 提供了多个用于通过网络引导安装程序和使用安装或升级脚本的选项。 n
有关设置网络基础架构的信息，请参见#unique_12。
n
有关创建和查找安装脚本的信息，请参见关于安装和升级脚本。
n
有关通过网络引导 ESXi 安装程序并使用安装脚本的特定过程，请参见以下主题之一： n
使用本机 UEFI HTTP 引导 ESXi 安装程序
n
使用 iPXE 和 HTTP 引导 ESXi 安装程序
n
使用 PXE 和 TFTP 引导 ESXi 安装程序
n
有关使用 vSphere Auto Deploy 通过使用 PXE 引导执行脚本式升级的信息，请参见第 4 章 使用
vSphere Auto Deploy 重新置备主机 。
VMware ESXi 升级
VMware, Inc.
50
[第51页]
网络引导安装过程概述
可以从网络接口引导 ESXi 主机。网络引导过程随以下因素而异：目标主机是使用旧版 BIOS 还是 UEFI 固
件，以及引导过程是使用　PXE TFTP、iPXE HTTP 还是 UEFI HTTP。
引导目标主机时，该主机会与环境中的不同服务器交互，以获得网络适配器、引导加载程序、内核、内核
的　IP 地址，最后获得安装脚本。所有组件就位后，安装即会开始，如下图所示。
图 3-2. PXE 引导安装过程概览
安装程序
启动
UDP
IP 和 TFTP 服务器
向我提供
网络适配器的 IP
TCP 或 UDP
mboot 和支持文件
向我提供网络引导加载程序
TCP 或 UDP
内核
向我提供内核
UDP
IP
向我提供内核的 IP
TCP
ks.cfg
向我提供安装脚本
ESXi 主机
ESXi 目标主机
DHCP 服务器
TFTP 或 HTTP
服务器
TFTP 或 HTTP
服务器
DHCP 服务器
脚本库
ESXi 主机与其他服务器之间的交互按如下所示进行：
1
用户引导目标 ESXi 主机。
2
目标 ESXi 主机生成 DHCP 请求。
3
DHCP 服务器做出如下响应：提供 IP 信息、TFTP 或 HTTP 服务器的位置以及初始网络引导加载程序 的文件名或 URL。 4
ESXi 主机连接 TFTP 或 HTTP 服务器，并请求　DHCP 服务器指定的文件名或 URL。 VMware ESXi 升级 VMware, Inc. 51 [第52页] 5
TFTP 或 HTTP 服务器发送网络引导加载程序，然后 ESXi 主机运行该程序。初始引导加载程序可能会
从服务器加载更多引导加载程序组件。
6
引导加载程序在 TFTP 或 HTTP 服务器上搜索配置文件，下载配置文件中指定的内核和其他　ESXi 组
件，并在 ESXi 主机上引导内核。
7
安装程序以交互方式或者使用　kickstart 脚本运行，如配置文件中所指定。
使用 PXE 和 TFTP 引导 ESXi 安装程序
可以使用 TFTP 服务器以 PXE 方式引导 ESXi 安装程序。具体过程将根据您是使用 UEFI 还是从旧版
BIOS 进行引导而稍有不同。因为大多数环境都包括支持 UEFI 引导的 ESXi 主机和仅支持旧版 BIOS 的主
机，所以本主题讨论这两种主机类型的必备条件和步骤。
n
对于旧版 BIOS 计算机，该过程支持引导多个不同版本的 ESXi 安装程序，方法是对所有目标计算机使
用同一 pxelinux.0 初始引导加载程序，但 PXELINUX 配置文件可能不同，具体视目标计算机的 MAC 地址而定。 n
对于 UEFI 计算机，该过程支持引导多个不同版本的 ESXi 安装程序，方法是对所有目标计算机使用同
一 mboot.efi 初始引导加载程序，但 boot.cfg 文件可能不同，具体视目标计算机的 MAC 地址而 定。 前提条件
确认您的环境满足以下必备条件。
n
从 VMware 网站下载的 ESXi 安装程序 ISO 映像。 n
硬件配置受 ESXi 版本支持的目标主机。请参见《VMware 兼容性指南》。 n
目标 ESXi 主机上支持 PXE 的网络适配器。
n
可以配置以进行 PXE 引导的 DHCP 服务器。请参见示例 DHCP 配置。 n TFTP 服务器。 n
允许 TFTP 流量的网络安全策略（UDP 端口 69）。
n
对于旧版 BIOS，您只能使用 IPv4 网络连接。对于 UEFI PXE 引导，可以使用 IPv4 或 IPv6 网络连 接。 n
（可选）安装脚本（kickstart 文件）。
n
多数情况下使用本地 VLAN。如果要指定用于 PXE 引导的 VLAN ID，请检查您的网卡是否支持 VLAN ID 规范。
对于旧版 BIOS 系统，请获取 3.86 版本的 SYSLINUX 软件包。有关详细信息，请参见网络引导背景信 息。 VMware ESXi 升级 VMware, Inc. 52 [第53页] 步骤 1
如果 ESXi 主机仅运行旧版 BIOS 固件，请获取并配置 PXELINUX。 a
获取 SYSLINUX 版本 3.86 并进行解压，然后将 pxelinux.0 文件复制到 TFTP 服务器的顶级 / tftpboot 目录。 b
使用以下代码模型创建 PXELINUX 配置文件。
ESXi-7.x.x-XXXXXX 是包含 ESXi 安装程序文件的 TFTP 子目录的名称。
DEFAULT install
NOHALT 1
LABEL install
KERNEL ESXi-7.x.x-XXXXXX/mboot.c32
APPEND -c ESXi-7.x.x-XXXXXX/boot.cfg IPAPPEND 2 c
将 PXELINUX 文件保存在 TFTP 服务器的 /tftpboot/pxelinux.cfg 目录中，所用文件名将
确定所有主机是否都默认引导此安装程序：
选项
描述
同一安装程序
如果希望所有主机都默认引导此 ESXi 安装程序，请将文件命名为 default。 不同安装程序
如果只希望特定主机使用此文件进行引导，请使用目标主机的 MAC 地址 (01-
mac_address_of_target_ESXi_host) 来命名此文件，例如
01-23-45-67-89-0a-bc。
2
如果 ESXi 主机运行 UEFI 固件，请将 efi/boot/bootx64.efi 文件从 ESXi 安装程序 ISO 映像复
制到 TFTP 服务器的 /tftpboot 文件夹中，并且将文件重命名为 mboot.efi。对于 7.0 Update 3
及更高版本，还请将 efi/boot/crypto64.efi 文件复制到 /tftpboot 文件夹。
注 新版本的 mboot.efi 通常可以引导旧版本的 ESXi，但旧版本的 mboot.efi 可能无法引导新版
本的 ESXi。如果您计划配置不同的主机以引导不同版本的 ESXi 安装程序，请使用最新版本中的 mboot.efi。 3 配置 DHCP 服务器。 4
创建 TFTP 服务器顶级 /tftpboot 目录的子目录，并以其将保存的 ESXi 版本命名，例如 /
tftpboot/ESXi-7.x.x-xxxxx。
5
将 ESXi 安装程序映像的内容复制到新创建的目录。
VMware ESXi 升级
VMware, Inc.
53
[第54页]
6
修改 boot.cfg 文件
a
添加以下行：
prefix=ESXi-7.x.x-xxxxxx
其中，ESXi-7.x.x-xxxxxx 是安装程序文件相对于 TFTP 服务器 root 目录的路径名称。 b
如果 kernel= 和 modules= 行中的文件名以正斜杠 (/) 字符开头，请删除该字符。 c
如果 kernelopt= 行包含字符串 cdromBoot，请只移除该字符串。 7
（可选） 对于脚本式安装，在 boot.cfg 文件中内核命令后的一行添加 kernelopt 选项以指定安装 脚本的位置。
将以下代码用作模型，其中 XXX.XXX.XXX.XXX 是安装脚本所在的服务器的 IP 地址，
esxi_ksFiles 是包含 ks.cfg 文件的目录。
kernelopt=ks=http://XXX.XXX.XXX.XXX/esxi_ksFiles/ks.cfg 8
如果您的 ESXi 主机运行 UEFI 固件，请指定是否希望所有 UEFI 主机引导同一安装程序。 选项 描述 同一安装程序
将 boot.cfg 文件复制或链接到 /tftpboot/boot.cfg 不同安装程序 a
创建 /tftpboot 的子目录，并以目标主机的 MAC 地址 (01-
mac_address_of_target_ESXi_host) 命名，例如 01-23-45-67-89-0a- bc。 b
将主机 boot.cfg 文件的副本（或链接）置于此目录中，例如 /tftpboot/
01-23-45-67-89-0a-bc/boot.cfg。
使用 iPXE 和 HTTP 引导 ESXi 安装程序
您可以使用 iPXE 从 HTTP 服务器引导 ESXi 安装程序。以下主题讨论支持 UEFI 引导的 ESXi 主机和仅支
持旧版 BIOS 的主机适用的必备条件和步骤。
n
对于旧版 BIOS 计算机，该过程支持引导多个不同版本的 ESXi 安装程序，方法是对所有目标计算机使
用同一 pxelinux.0 初始引导加载程序，但 PXELINUX 配置文件可能不同，具体视目标计算机的 MAC 地址而定。 n
对于 UEFI 计算机，该过程支持引导多个不同版本的 ESXi 安装程序，方法是对所有目标计算机使用同
一 mboot.efi 初始引导加载程序，但 boot.cfg 文件可能不同，具体视目标计算机的 MAC 地址而 定。 前提条件 确认您的环境包含以下组件： n
从 VMware 网站下载的 ESXi 安装程序 ISO 映像。 n
硬件配置受 ESXi 版本支持的目标主机。请参见《VMware 兼容性指南》。 VMware ESXi 升级 VMware, Inc. 54 [第55页] n
目标 ESXi 主机上支持 PXE 的网络适配器。
n
可以配置以进行 PXE 引导的 DHCP 服务器。请参见示例 DHCP 配置。 n TFTP 服务器。 n
允许 TFTP 流量的网络安全策略（UDP 端口 69）。
n
对于旧版 BIOS，您只能使用 IPv4 网络连接。对于 UEFI PXE 引导，可以使用 IPv4 或 IPv6 网络连 接。 n
（可选）安装脚本（kickstart 文件）。
n
多数情况下使用本地 VLAN。如果要指定用于 PXE 引导的 VLAN ID，请检查您的网卡是否支持 VLAN ID 规范。
确认您的环境还满足使用 HTTP 服务器进行 PXE 引导所需的以下必备条件： n
确认 HTTP 服务器可供目标 ESXi 主机访问。
n
如果 ESXi 主机仅运行旧版 BIOS 固件，请获取 3.86 版本的 SYSLINUX 软件包。有关详细信息，请参 见网络引导背景信息。 步骤 1 获取并配置 iPXE。 a 获取 iPXE 源代码。 b
在 iPXE 下载页面上，按照构建说明进行操作，但要运行以下命令之一。 n
对于仅运行旧版 BIOS 固件的 ESXi 主机，请运行 make bin/undionly.kpxe。 n
对于运行 UEFI 固件的 ESXi 主机，请运行 make bin-x86_64-efi/snponly.efi。 c
将 undionly.kpxe 或 snponly.efi 文件复制到 TFTP 服务器上的 /tftpboot 目录中。 VMware ESXi 升级 VMware, Inc. 55 [第56页] 2
如果 ESXi 主机仅运行旧版 BIOS 固件，请获取并配置 PXELINUX。 a
获取 SYSLINUX 版本 3.86 并进行解压，然后将 pxelinux.0 文件复制到 TFTP 服务器的 / tftpboot 目录中。 b
使用以下代码模型创建 PXELINUX 配置文件。
ESXi-7.x.x-XXXXXX 是包含 ESXi 安装程序文件的 TFTP 子目录的名称。
DEFAULT install
NOHALT 1
LABEL install
KERNEL ESXi-7.x.x-XXXXXX/mboot.c32
APPEND -c ESXi-7.x.x-XXXXXX/boot.cfg IPAPPEND 2 c
将 PXELINUX 文件保存在 TFTP 服务器上的 /tftpboot/pxelinux.cfg/ 目录中。
文件名决定了是否所有主机都默认引导此安装程序。
选项
描述
同一安装程序
如果希望所有主机都默认引导此 ESXi 安装程序，请将文件命名为 default。 不同安装程序
如果只有特定主机必须引导此文件，请使用目标主机的 MAC 地址 (01-
mac_address_of_target_ESXi_host) 命名文件。例如，
01-23-45-67-89-0a-bc。
3
如果 ESXi 主机运行 UEFI 固件，请将 efi/boot/bootx64.efi 文件从 ESXi 安装程序 ISO 映像复
制到 TFTP 服务器的 /tftpboot 文件夹中，并且将文件重命名为 mboot.efi。
注 新版本的 mboot.efi 通常可以引导旧版本的 ESXi，但旧版本的 mboot.efi 可能无法引导新版
本的 ESXi。如果您计划配置不同的主机以引导不同版本的 ESXi 安装程序，请使用最新版本中的 mboot.efi。 4 配置 DHCP 服务器。 5
在 HTTP 服务器上创建一个与其将包含的 ESXi 的版本同名的目录。例如， /var/www/html/
ESXi-7.x.x-XXXXXX。
6
将 ESXi 安装程序映像的内容复制到新创建的目录。
7
修改 boot.cfg 文件
a
添加以下行：
prefix=http://XXX.XXX.XXX.XXX/ESXi-7.x.x-XXXXXX
其中，http://XXX.XXX.XXX.XXX/ESXi-7.x.x-XXXXXX 是安装程序文件在 HTTP 服务器上的位 置。 b
如果 kernel= 和 modules= 行中的文件名以正斜杠 (/) 字符开头，请删除该字符。 c
如果 kernelopt= 行包含字符串 cdromBoot，请只移除该字符串。 VMware ESXi 升级 VMware, Inc. 56 [第57页] 8
（可选） 对于脚本式安装，在 boot.cfg 文件中内核命令后的一行添加 kernelopt 选项以指定安装 脚本的位置。
将以下代码用作模型，其中 XXX.XXX.XXX.XXX 是安装脚本所在的服务器的 IP 地址，
esxi_ksFiles 是包含 ks.cfg 文件的目录。
kernelopt=ks=http://XXX.XXX.XXX.XXX/esxi_ksFiles/ks.cfg 9
如果您的 ESXi 主机运行 UEFI 固件，请指定是否希望所有 UEFI 主机引导同一安装程序。 选项 描述 同一安装程序
将 boot.cfg 文件复制或链接到 /tftpboot/boot.cfg 不同安装程序 a
创建 /tftpboot 的子目录，并以目标主机的 MAC 地址 (01-
mac_address_of_target_ESXi_host) 命名，例如 01-23-45-67-89-0a- bc。 b
将主机 boot.cfg 文件的副本（或链接）置于此目录中，例如 /tftpboot/
01-23-45-67-89-0a-bc/boot.cfg。
使用本机 UEFI HTTP 引导 ESXi 安装程序
您可以直接从 HTTP 服务器引导 ESXi 安装程序，而无需其他软件的支持。
UEFI HTTP 支持引导多个版本的 ESXi 安装程序。您可以对所有目标计算机使用相同的 mboot.efi 初始
引导加载程序，但 boot.cfg 文件可能有所不同，具体取决于目标计算机的 MAC 地址。
注 在引导过程中，不要混合使用 IPv4 或 IPv6 网络。使用 IPv4 或者 IPv6 网络。 前提条件 确认您的环境包含以下组件： n
具有支持 HTTP 引导功能的 UEFI 固件的 ESXi 主机。 n
从 VMware 网站下载的 ESXi 安装程序 ISO 映像。 n
硬件配置受 ESXi 版本支持的目标主机。请参见《VMware 兼容性指南》。 n
目标 ESXi 主机上支持 UEFI 网络连接的网络适配器。
n
您可以为 UEFI HTTP 引导配置的 DHCP 服务器。请参见示例 DHCP 配置 n
（可选）安装脚本（kickstart 文件）。
n
多数情况下使用本地 VLAN。如果要指定用于 PXE 引导的 VLAN ID，请检查您的网卡是否支持 VLAN ID 规范。 VMware ESXi 升级 VMware, Inc. 57 [第58页] 步骤 1
将 efi/boot/bootx64.efi 文件从 ESXi 安装程序 ISO 映像复制到 HTTP 服务器上的目录中，并将
文件重命名为 mboot.efi。例如，http://www.example.com/esxi/mboot.efi。
注 新版本的 mboot.efi 通常可以引导旧版本的 ESXi，但旧版本的 mboot.efi 可能无法引导新版
本的 ESXi。如果您计划配置不同的主机以引导不同版本的 ESXi 安装程序，请使用最新版本中的 mboot.efi。 2 配置 DHCP 服务器。 3
在 HTTP 服务器上创建一个与其将包含的 ESXi 的版本同名的目录。例如，http://
www.example.com/esxi/ESXi-7.x.x-XXXXXX。 4
将 ESXi 安装程序映像的内容复制到新创建的目录。
5
修改 boot.cfg 文件。
a
添加以下包含了新创建目录的 URL 的行。
prefix=http://www.example.com/esxi/ESXi-7.x.x-XXXXXX b
如果 kernel= 和 modules= 行中的文件名以正斜杠 (/) 字符开头，请删除该字符。 c
如果 kernelopt= 行包含字符串 cdromBoot，请只移除该字符串。 6
（可选） 对于脚本式安装，在 boot.cfg 文件中内核命令后的一行添加 kernelopt 选项以指定安装 脚本的位置。
例如，kernelopt=ks=http://www.example.com/esxi_ksFiles/ks.cfg 7
（可选） 从 ESXi 7.0 Update 2 开始，可以使用虚拟机配置参数 networkBootProtocol 和
networkBootUri 指定虚拟机可以从何处引导。设置 networkBootProtocol 指定引导协议（IPv4 或
IPv6）。例如，networkBootProtocol = httpv4。设置 networkBootUri 指定 ESXi 引导加载程序
(bootx64.efi) 的 HTTP URL。例如，networkBootUri = http://192.168.30.6/esxi70uc1/efi/
boot/bootx64.efi。
8
指定是否希望所有 UEFI 主机都引导同一安装程序。
选项
描述
同一安装程序
将 boot.cfg 文件添加到 mboot.efi 所在的目录中。例如，http://
www.example.com/esxi/boot.cfg
不同安装程序
a
为包含 mboot.efi 文件的目录创建一个子目录。将目录命名为目标主机的
MAC 地址 (01-mac_address_of_target_ESXi_host)，例如
01-23-45-67-89-0a-bc。
b
在该目录中添加自定义 boot.cfg 文件。例如，http://
www.example.com/esxi/01-23-45-67-89-0a-bc/boot.cfg。
这两种安装程序都可以使用。如果 ESXi 主机在 HTTP 服务器上不具有自定义 boot.cfg 文件，则从
默认的 boot.cfg 文件中进行引导。
VMware ESXi 升级
VMware, Inc.
58
[第59页]
网络引导背景信息
了解网络引导过程可在故障排除过程中为您提供帮助。
TFTP 服务器
简单文件传输协议 (TFTP) 与 FTP 服务类似，通常仅用于网络引导系统或在网络设备（如路由器）上加载
固件。TFTP 在 Linux 和 Windows 上都可用。 n
大多数 Linux 发行版都包含 tftp-hpa 服务器的副本。如果您需要受支持的解决方案，请从选择的供应
商处购买受支持的 TFTP 服务器。您也可以从 VMware Marketplace 中随附提供的一个设备中获取 TFTP 服务器。 n
如果您的 TFTP 服务器在 Microsoft Windows 主机上运行，请使用 tftpd32 版本 2.11 或更高版本。请
参见http://tftpd32.jounin.net/。
SYSLINUX 和 PXELINUX
如果在旧版 BIOS 环境中使用 PXE，则必须了解不同的引导环境。 n
SYSLINUX 是一个开源引导环境，适用于运行旧版 BIOS 固件的计算机。用于 BIOS 系统的 ESXi 引导
加载程序 mboot.c32 作为 SYSLINUX 插件运行。可以将 SYSLINUX 配置为从多种类型的介质（包
括磁盘、ISO 映像和网络）引导。可以从以下网址找到 SYSLINUX 软件包：http://
www.kernel.org/pub/linux/utils/boot/syslinux/。 n
PXELINUX 是一种 SYSXLINUX 配置，用于根据 PXE 标准从 TFTP 服务器引导。如果使用
PXELINUX 引导 ESXi 安装程序，则 pxelinux.0 二进制文件、mboot.c32、配置文件、内核以及
其他文件将通过 TFTP 传输。
注 VMware 构建了用于 SYSLINUX 版本 3.86 的 mboot.c32 插件，并且仅对该版本测试了 PXE 引导。
其他版本可能不兼容。Open Source Disclosure Package for VMware vSphere Hypervisor 包括
SYSLINUX 版本 3.86 的错误修复。
iPXE
iPXE 是提供 HTTP 实现的开源软件。可以使用该软件执行初始引导。有关详细信息，请参见https:// ipxe.org/。
VMware 将 iPXE 内部版本作为 Auto Deploy 的一部分包括在内。Open Source Disclosure Package
for VMware vCenter Server 提供此内部版本的源树。
UEFI PXE 和 UEFI HTTP
大多数 UEFI 固件本身包含 PXE 支持，允许从 TFTP 服务器引导。固件可直接加载用于 UEFI 系统的
ESXi 引导加载程序 mboot.efi，而不需要 PXELINUX 等其他软件。
某些 UEFI 固件支持本机 UEFI HTTP 引导。UEFI 规范版本 2.5 中引入了该功能。固件可以从 HTTP 服务
器加载 ESXi 引导加载程序，而无需其他软件，如 iPXE。
注 Apple Macintosh 产品不支持 PXE 引导，但支持通过 Apple 特定协议从网络引导。 VMware ESXi 升级 VMware, Inc. 59 [第60页] 网络引导的替代方法
除了网络引导外，还可以使用其他方法在不同主机上引导不同软件，例如： n
将 DHCP 服务器配置为根据 MAC 地址或其他标准为不同主机提供不同的初始引导加载程序文件名。
请参见相应 DCHP 服务器文档。
n
这些方法使用 iPXE 作为初始引导加载程序，并通过 iPXE 配置文件根据 MAC 地址或其他标准选择下 一个引导加载程序。 PXELINUX 配置文件
需要有 PXELINUX 配置文件才能在传统 BIOS 系统上引导 ESXi 安装程序。该配置文件定义了目标 ESXi 主机启动时向其显示的菜单。
本节提供有关 PXELINUX 配置文件的常规信息。
有关语法详细信息，请参见 SYSLINUX 网站，网址为 http://www.syslinux.org/。 需要的文件
在 PXE 配置文件中，必须包括以下文件的路径：
n
mboot.c32 是引导加载程序。
n
boot.cfg 是引导加载程序配置文件。
请参见 关于 boot.cfg 文件
PXE 配置文件的文件名
对于 PXE 配置文件的文件名，请选择以下选项之一：
n
01-mac_address_of_target_ESXi_host。例如，01-23-45-67-89-0a-bc n
以十六进制表示的目标 ESXi 主机 IP 地址。
n
default
初始引导文件 pxelinux.0 尝试按以下顺序加载 PXE 配置文件： 1
它会尝试加载目标 ESXi 主机的 MAC 地址，此地址以其 ARP 类型代码为前缀（如果是以太网，则为 01）。 2
如果尝试失败，则会尝试加载以十六进制表示的目标 ESXi 系统 IP 地址。 3
最后，它会尝试加载名为 default 的文件。
PXE 配置文件的文件位置
将文件保存在 TFTP 服务器上的 /tftpboot/pxelinux.cfg/ 中。
例如，您可能会将文件保存在 TFTP 服务器的 /tftpboot/pxelinux.cfg/01-00-21-5a-ce-40-f6
下。目标 ESXi 主机的网络适配器 MAC 地址为 00-21-5a-ce-40-f6。 VMware ESXi 升级 VMware, Inc. 60 [第61页] 示例 DHCP 配置
要通过网络引导 ESXi 安装程序，DHCP 服务器必须将 TFTP 或 HTTP 服务器的地址以及初始引导加载程
序的文件名发送到 ESXi 主机。
目标计算机首次引导时，它会通过网络广播数据包，请求信息以便自行引导。DHCP 服务器将响应此请
求。DHCP 服务器必须能够确定目标计算机是否允许引导以及初始引导加载程序二进制文件的位置。对于
PXE 引导，该位置是 TFTP 服务器上的文件。对于 UEFI HTTP 引导，该位置是一个 URL。
小心 如果网络中已有一个 DHCP 服务器，则不要设置第二个 DHCP 服务器。如果有多个 DHCP 服务器
响应 DHCP 请求，计算机可能会获得错误或存在冲突的 IP 地址，或者可能接收不到正确的引导信息。在
设置 DHCP 服务器之前，请与网络管理员联系。有关配置 DHCP 的支持，请与 DHCP 服务器供应商联 系。
可以使用许多 DHCP 服务器。以下示例针对的是 ISC DHCP 服务器。如果使用的是适用于 Microsoft
Windows 的某个 DHCP 版本，请参见 DHCP 服务器文档以确定如何将 next-server 和 filename 参数 传递到目标计算机。
使用 PXE 和 TFTP (IPv4) 引导的示例
此示例显示如何配置 ISC DHCP 服务器以使用 IPv4 地址为 xxx.xxx.xxx.xxx 的 TFTP 服务器来以 PXE 方 式引导 ESXi。 #
# ISC DHCP server configuration file snippet. This is not a complete
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option client-system-arch code 93 = unsigned integer 16;
class "pxeclients" {
match if substring(option vendor-class-identifier, 0, 9) = "PXEClient";
next-server xxx.xxx.xxx.xxx;
if option client-system-arch = 00:07 or option client-system-arch = 00:09 {
filename = "mboot.efi";
} else {
filename = "pxelinux.0";
}
}
在计算机尝试以 PXE 方式引导时，DHCP 服务器会提供 IP 地址和 TFTP 服务器上 pxelinux.0 或
mboot.efi 二进制文件的位置。
使用 PXE 和 TFTP (IPv6) 引导的示例
此示例显示如何配置 ISC DHCPv6 服务器以使用 IPv6 地址为 xxxx:xxxx:xxxx:xxxx::xxxx 的 TFTP 服务器
来以 PXE 方式引导 ESXi。
#
# ISC DHCPv6 server configuration file snippet. This is not a complete
VMware ESXi 升级
VMware, Inc.
61
[第62页]
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option dhcp6.bootfile-url code 59 = string;
option dhcp6.bootfile-url "tftp://[xxxx:xxxx:xxxx:xxxx::xxxx]/mboot.efi";
在计算机尝试以 PXE 方式引导时，DHCP 服务器会提供 IP 地址和 TFTP 服务器上 mboot.efi 二进制文 件的位置。
使用 iPXE 和 HTTP (IPv4) 引导的示例
此示例显示如何配置 ISC DHCP 服务器以通过从 IPv4 地址为 xxx.xxx.xxx.xxx 的 TFTP 服务器加载 iPXE 来引导 ESXi。 #
# ISC DHCP server configuration file snippet. This is not a complete
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option client-system-arch code 93 = unsigned integer 16;
class "pxeclients" {
match if substring(option vendor-class-identifier, 0, 9) = "PXEClient";
next-server xxx.xxx.xxx.xxx;
if option client-system-arch = 00:07 or option client-system-arch = 00:09 {
if exists user-class and option user-class = "iPXE" {
# Instruct iPXE to load mboot.efi as secondary bootloader
filename = "mboot.efi";
} else {
# Load the snponly.efi configuration of iPXE as initial bootloader
filename = "snponly.efi";
}
} else {
if exists user-class and option user-class = "iPXE" {
# Instruct iPXE to load pxelinux as secondary bootloader
filename = "pxelinux.0";
} else {
# Load the undionly configuration of iPXE as initial bootloader
filename = "undionly.kpxe";
}
}
在计算机尝试以 PXE 方式引导时，DHCP 服务器会提供 IP 地址和 TFTP 服务器上 undionly.kpxe 或
snponly.efi 二进制文件的位置。在旧版 BIOS 情况下，iPXE 随即向 DHCP 服务器询问下一个要加载
的文件，而此时该服务器返回 pxelinux.0 作为文件名。在 UEFI 情况下，iPXE 随即向 DHCP 服务器询
问下一个要加载的文件，而此时该服务器返回 mboot.efi 作为文件名。在这两种情况下，iPXE 是常驻
项，并且系统具有 HTTP 功能。因此，系统可以从 HTTP 服务器加载其他文件。 VMware ESXi 升级 VMware, Inc. 62 [第63页]
使用 iPXE 和 HTTP (IPv6) 引导的示例
此示例显示如何配置 ISC DHCPv6 服务器以通过从 IPv6 地址为 xxxx:xxxx:xxxx:xxxx::xxxx 的
TFTP 服务器加载 iPXE 来引导 ESXi。
#
# ISC DHCPv6 server configuration file snippet. This is not a complete
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option dhcp6.bootfile-url code 59 = string;
if exists user-class and option user-class = "iPXE" {
# Instruct iPXE to load mboot.efi as secondary bootloader
option dhcp6.bootfile-url "tftp://[xxxx:xxxx:xxxx:xxxx::xxxx]/mboot.efi"; } else {
# Load the snponly.efi configuration of iPXE as initial bootloader
option dhcp6.bootfile-url "tftp://[xxxx:xxxx:xxxx:xxxx::xxxx]/snponly.efi"; }
在计算机尝试以 PXE 方式引导时，DHCP 服务器会提供 IP 地址和 TFTP 服务器上 snponly.efi (iPXE)
二进制文件的位置。iPXE 随即向 DHCP 服务器询问下一个要加载的文件，而此时该服务器返回
mboot.efi 作为文件名。iPXE 是常驻项，并且系统具有 HTTP 功能。因此，系统可以从 HTTP 服务器加 载其他文件。
使用 UEFI HTTP (IPv4) 引导的示例
此示例显示如何配置 ISC DHCP 服务器以从 Web 服务器 www.example.com 通过 IPv4 使用本机 UEFI HTTP 引导 ESXi。 #
# ISC DHCP server configuration file snippet. This is not a complete
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option client-system-arch code 93 = unsigned integer 16;
class "httpclients" {
match if substring(option vendor-class-identifier, 0, 10) = "HTTPClient";
option vendor-class-identifier "HTTPClient";
if option client-system-arch = 00:10 {
# x86_64 UEFI HTTP client
filename = http://www.example.com/esxi/mboot.efi; } } VMware ESXi 升级 VMware, Inc. 63 [第64页]
使用 UEFI HTTP (IPv6) 引导的示例
此示例显示如何配置 ISC DHCPv6 服务器以从 Web 服务器 www.example.com 通过 IPv6 使用本机
UEFI HTTP 引导 ESXi。
#
# ISC DHCPv6 server configuration file snippet. This is not a complete
# configuration file; see the ISC server documentation for details on
# how to configure the DHCP server.
#
allow booting;
allow bootp;
option dhcp6.bootfile-url code 59 = string;
option dhcp6.user-class code 15 = { integer 16, string };
option dhcp6.vendor-class code 16 = { integer 32, integer 16, string };
if option dhcp6.client-arch-type = 00:10 {
# x86_64 HTTP clients
option dhcp6.vendor-class 0 10 "HTTPClient";
option dhcp6.bootfile-url "http://www.example.com/esxi/mboot.efi"; }
使用 ESXCLI 命令升级主机
通过使用 ESXCLI，可以将 ESXi 6.5 主机或 ESXi 6.7 主机升级到版本 7.0，以及更新或修补 ESXi 6.5、
ESXi 6.7 和 ESXi 7.0 主机。
vSphere 7.0 将组件、基础映像和加载项作为新的软件交付产品引入，可用于更新或修补 ESXi 7.0 主机。
有关在 ESXi 上管理组件、基础映像和加载项的信息，请参见《ESXCLI 概念和示例》
要使用 ESXCLI 命令，必须安装独立的 ESXCLI。有关安装和使用 ESXCLI 的详细信息，请参见以下文 档。 n 《ESXCLI 入门》 n 《ESXCLI 参考指南》
注 如果在 esxcli 命令运行时按 Ctrl+C，命令行界面将退出到新的提示符，而不显示消息。但是，命令 将继续运行直至完成。
对于使用 vSphere Auto Deploy 部署的 ESXi 主机，工具 VIB 必须是用于初始 Auto Deploy 安装的基础
引导映像的一部分。以后不能单独添加工具 VIB。
VIB、映像配置文件和软件库
使用 esxcli 命令升级 ESXi 需要了解 VIB、映像配置文件和软件库。
以下技术术语在整个 vSphere 文档集中用于论述安装和升级任务。 VIB VMware ESXi 升级 VMware, Inc. 64 [第65页]
VIB 是一个 ESXi 软件包。包括 VMware 及其合作伙伴软件包解决方案、驱动程序、CIM 提供程序以
及将 ESXi 平台扩展为 VIB 的应用程序。VIB 在软件库中可用。可以使用 VIB 创建和自定义 ISO 映像
或者通过在 ESXi 主机上异步安装 VIB 来升级主机。
映像配置文件
映像配置文件定义 ESXi 映像并包含 VIB。映像配置文件始终包含一个基础 VIB 且可能包含多个
VIB。可以使用 vSphere ESXi Image Builder 检查和定义映像配置文件。 软件库
软件库是 VIB 和映像配置文件的集合。软件库是文件和文件夹的一个层次结构，可以通过 HTTP URL
（联机库）或 ZIP 文件（脱机库）获取。VMware 及其合作伙伴提供了软件库。安装大型 VMware 的
公司可以创建内部库，以便为 ESXi 主机置备 vSphere Auto Deploy 或导出 ISO 用于 ESXi 安装。
了解 VIB 和主机的接受级别
每个发布的 VIB 均具有无法更改的接受程度。主机接受程度决定了能够在该主机上安装哪些 VIB。
接受级别将应用到使用 esxcli software vib install 和 esxcli software vib update 命令
安装的各个 VIB、使用 vSphere Lifecycle Manager 安装的 VIB 以及映像配置文件中的 VIB。
主机上所有 VIB 的接受程度必须至少与主机接受程度相同。例如，如果主机接受程度为
VMwareAccepted，则可以安装接受程度为 VMwareCertified 和 VMwareAccepted 的 VIB，但不能安
装接受程度为 PartnerSupported 或 CommunitySupported 的 VIB。要安装接受级别的限制性比主机低
的 VIB，可以使用 vSphere Client 或运行 esxcli software acceptance 命令来更改主机的设置。
最佳做法是设置主机接受程度，这样您就可以指定可以安装在主机上并与映像配置文件配合使用的 VIB，
并且还可以指定期望的 VIB 接受程度。例如，可以为生产环境中的主机设置的接受级别比为测试环境中的 主机设置的接受级别更严格。
VMware 支持以下接受级别。
VMware 认证
“VMware 认证”接受级别具有最严格的要求。此级别的 VIB 能够完全通过全面测试，该测试等效于
相同技术的 VMware 内部质量保证测试。当前，只有 I/O Vendor Program (IOVP) 程序驱动程序在
此级别发布。VMware 受理此接受级别的 VIB 的支持致电。 VMware 认可
此接受级别的 VIB 通过验证测试，但是这些测试并未对软件的每个功能都进行全面测试。合作伙伴运
行测试，VMware 验证结果。现在，以此级别发布的 VIB 包括 CIM 提供程序和 PSA 插件。VMware
将此接受级别的 VIB 支持致电转交给合作伙伴的支持组织。
合作伙伴支持
接受级别为“合作伙伴支持”的 VIB 是由 VMware 信任的合作伙伴发布的。合作伙伴执行所有测试。
VMware 不验证结果。合作伙伴要在 VMware 系统中启用的新的或非主流的技术将使用此级别。现 VMware ESXi 升级 VMware, Inc. 65 [第66页]
在，驱动程序 VIB 技术（例如 Infiniband、ATAoE 和 SSD）处于此级别，且具有非标准的硬件驱动
程序。VMware 将此接受级别的 VIB 支持致电转交给合作伙伴的支持组织。 社区支持
“社区支持”接受级别用于由 VMware 合作伙伴程序外部的个人或公司创建的 VIB。此级别的 VIB 尚
未通过任何 VMware 批准的测试程序，且不受 VMware 技术支持或 VMware 合作伙伴的支持。
表 3-10. 需要在主机上安装的 VIB 接受程度
主机接受程度
接受程度为
VMwareCertified 的
VIB
接受程度为
VMwareAccepted 的
VIB
接受程度为
PartnerSupported 的
VIB
接受程度为
CommunitySupporte
d 的 VIB
VMware 认证
x
VMware 认可
x
x
合作伙伴支持
x
x
x
社区支持
x
x
x
x
将主机接受程度与更新接受程度进行匹配
可以更改主机接受程度，使其与要安装的 VIB 或映像配置文件的接受程度匹配。主机上所有 VIB 的接受程
度必须至少与主机接受程度相同。
使用此程序确定主机接受程序和要安装的 VIB 或映像配置文件的接受程度，并更改主机接受程度（如果更 新需要）。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1
检索 VIB 或映像配置文件的接受程度。
选项
描述
列出所有 VIB 的信息
esxcli --server=<server_name> software sources vib list --
depot=<depot_URL>
列出指定 VIB 的信息
esxcli --server=<server_name> software sources vib list --
viburl=<vib_URL>
VMware ESXi 升级
VMware, Inc.
66
[第67页]
选项
描述
列出所有映像配置文件的信息
esxcli --server=<server_name> software sources profile
list --depot=<depot_URL>
列出指定映像配置文件的信息
esxcli --server=<server_name> software sources profile
get --depot=<depot_URL> --profile=<profile_name> 2 检索主机接受程度。
esxcli --server=<server_name> software acceptance get 3
（可选） 如果 VIB 接受程度比主机接受程度更严格，则更改主机接受程度。
esxcli --server=<server_name> software acceptance set --level=<acceptance_level>
acceptance_level 可以是 VMwareCertified、VMwareAccepted、PartnerSupported 或
CommunitySupported。接受程度的值区分大小写。
注 可以在 esxcli software vib 或 esxcli software profile 命令中使用 --force 选项，
添加接受程度低于主机接受程度的 VIB 或映像配置文件。将显示警告。由于您的设置不再一致，因此
当您在主机上安装 VIB、移除 VIB 和执行其他某些操作时，会重复出现警告。
确定更新是否需要主机处于维护模式或重新引导
可以通过实时安装进行安装的 VIB 不需要重新引导主机，但可能需要将主机置于维护模式。其他 VIB 和配
置文件可能需要在安装或更新后重新引导主机。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 VMware ESXi 升级 VMware, Inc. 67 [第68页] 步骤 1
检查您要安装的 VIB 或映像配置文件需要将主机置于维护模式，还是需要在安装或更新后重新引导主 机。 运行以下命令之一。 选项 描述 检查 VIB
esxcli --server=<server_name> software sources vib get -v
<absolute_path_to_vib>
检查库中的 VIB
esxcli --server=<server_name> software sources vib get --
depot=<depot_name>
检查库中的映像配置文件
esxcli --server=<server_name> software sources profile
get --depot=<depot_name>
2
查看返回值。
从 VIB 元数据读取的返回值指示在安装 VIB 或映像配置文件之前，主机是否必须处于维护模式，以及
安装 VIB 或配置文件是否需要重新引导主机。
注 vSphere Lifecycle Manager 依赖内部 ESXi 软件扫描 API 确定是否需要处于维护模式。在实时系
统上安装 VIB 时，如果 Live-Install-Allowed 的值设置为 false，则安装结果将指示 vSphere
Lifecycle Manager 重新引导主机。从实时系统中移除 VIB 时，如果 Live-Remove-Allowed 的值
设置为 false，则移除结果将指示 vSphere Lifecycle Manager 重新引导主机。在这两种情况下，修复
开始时，vSphere Lifecycle Manager 会自动将主机置于维护模式。 后续步骤
如有必要，请将主机置于维护模式。请参见将主机置于维护模式。如果需要重新引导，且主机属于
vSphere HA 集群，则在安装或更新之前从集群中移除该主机或在集群上停用 HA。此外，请将主机置于
维护模式，以便在升级期间最大程度地减少引导磁盘活动。
将主机置于维护模式
某些使用实时安装的安装和更新操作要求主机处于维护模式。
当更新操作需要重新引导时，需要处于维护模式。但是，在使用 esxcli 命令执行更新和升级操作时，只能 手动将主机置于维护模式。
要确定升级操作是否需要主机处于维护模式，请参见 确定更新是否需要主机处于维护模式或重新引导。
注 如果主机是 vSAN 集群的成员，并且主机上有任何虚拟机对象在其存储策略中使用“允许的故障数
=0”的设置，则在进入维护模式时，主机可能会出现异常延迟。发生延迟的原因是 vSAN 必须将此对象从
主机中逐出才能成功完成维护操作。
VMware ESXi 升级
VMware, Inc.
68
[第69页]
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1 检查主机是否处于维护模式。
esxcli --server=<server_name> system maintenanceMode get 2
关闭 ESXi 主机上运行的每个虚拟机的电源。
注 可以通过运行以下命令列出所有正在运行的虚拟机并检索每个虚拟机的环境 ID。
esxcli --server=<server_name> vm process list 选项 命令
关闭客户机操作系统，然后再关闭虚拟机
电源
esxcli --server=<server_name> vm process kill --type soft
--world-id <vm_ID>
立即关闭虚拟机电源
esxcli --server=<server_name> vm process kill --type hard
--world-id <vm_ID>
强制执行关闭电源操作
esxcli --server=<server_name> vm process kill --type
force --world-id <vm_ID>
此外，为避免关闭虚拟机的电源，可以将其迁移至其他主机。请参见《《vCenter Server 和主机管
理》》文档中的主题“迁移虚拟机”。
3
将主机置于维护模式。
esxcli --server=<server_name> system maintenanceMode set --enable true 4 确认主机处于维护模式。
esxcli --server=<server_name> system maintenanceMode get VMware ESXi 升级 VMware, Inc. 69 [第70页] 使用各个 VIB 更新主机
可以使用存储在软件库中的 VIB 更新主机，该软件库可以通过 URL 进行访问或在脱机 ZIP 库中获取。
重要说明 如果要通过 VMware 提供的库中 ZIP 包更新 ESXi（可以登录 VMware 网站在线更新，或者下
载到本地进行更新），VMware 仅支持主题使用映像配置文件升级或更新主机 中为 VMware 提供的库指 定的更新方法。
注 不支持使用 esxcli software vib update 和 esxcli software vib install 命令进行升
级。请参见使用映像配置文件升级或更新主机 。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
n
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 n
确定更新是否需要将主机置于维护模式或重新引导主机。如有必要，请将主机置于维护模式。
请参见 确定更新是否需要主机处于维护模式或重新引导。请参见将主机置于维护模式。 n
如果更新需要重新引导，并且主机属于 vSphere HA 集群，请从集群中移除该主机或停用集群上的 HA。 步骤 1 确定在主机上安装的 VIB。
esxcli --server=<server_name> software vib list 2 查找出库中可用的 VIB。 选项 描述 从可通过 URL 访问的库中
esxcli --server=<server_name> software sources vib list --
depot=http://<web_server>/<depot_name> 从本地库 ZIP 文件中
esxcli --server=<server_name> software sources vib list --
depot=<absolute_path_to_depot_zip_file>
可以使用 --proxy 参数指定代理服务器。
VMware ESXi 升级
VMware, Inc.
70
[第71页]
3
更新现有的 VIB 以包含库中的 VIB 或安装新的 VIB。 选项 描述
从通过 URL 访问的库中更新 VIB
esxcli --server=<server_name> software vib update --
depot=http://<web_server>/<depot_name>
从本地库 ZIP 文件中更新 VIB
esxcli --server=<server_name> software vib update --
depot=<absolute_path_to_depot_ZIP_file>
安装指定脱机库上的 ZIP 文件中的所有
VIB（包括 VMware VIB 和合作伙伴提
供的 VIB）
esxcli --server=<server_name> software vib install --
depot <path_to_VMware_vib_ZIP_file>\<VMware_vib_ZIP_file> --depot
<path_to_partner_vib_ZIP_file>\<partner_vib_ZIP_file>
通过 update 和 install 命令选项，可以执行试运行、指定特定的 VIB 以及跳过接受级别验证等。
请勿跳过对生产系统的验证。请参见《ESXCLI 参考》。
4
验证 VIB 是否已安装在 ESXi 主机上。
esxcli --server=<server_name> software vib list
使用映像配置文件升级或更新主机
可以使用存储在软件库中的映像配置文件升级或更新主机，该软件库可通过 URL 或脱机 ZIP 库访问。
可以使用 esxcli software profile update 或 esxcli software profile install 命令升级 或更新 ESXi 主机。
升级或更新主机时，esxcli software profile update 或
esxcli software profile install 命令会在主机上应用更高版本（主版本或次版本）的完整映像
配置文件。此操作完成并重新引导后，该主机可加入到同一或更高版本的 vCenter Server 环境中。
esxcli software profile update 命令会使 ESXi 主机映像的整个内容具有与使用 ISO 安装程序的
对应升级方法相同的级别。但是，ISO 安装程序会针对潜在问题（如内存不足或设备不受支持）执行升级
前检查。从 ESXi 6.7 Update 1 或更高版本升级到较新版本时，esxcli 升级方法仅执行此类检查。
有关 ESXi 升级过程和方法的详细信息，请参见 ESXi 主机升级过程概览。
重要说明 如果要通过 VMware 提供的库中的 ZIP 包（可从 VMware 网站联机访问或下载到本地）升级
或更新 ESXi，则 VMware 仅支持更新命令 esxcli software profile update --
depot=<depot_location> --profile=<profile_name>。 VMware ESXi 升级 VMware, Inc. 71 [第72页]
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
注 update 和 install 命令的选项允许您执行试运行、绕过接受级别验证、忽略硬件兼容性检查警告
等。绕过硬件兼容性检查警告的选项仅适用于 ESXi 6.7 Update 1 或更高版本。请勿跳过对生产系统的验 证。
有关选项帮助，请键入 esxcli software profile install --help 或 esxcli software
profile update --help。有关可用命令行选项的完整列表，请参见《ESXCLI 参考》。 前提条件 n
安装独立 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命 令。 n
确定更新是否需要将主机置于维护模式或重新引导主机。如有必要，请将主机置于维护模式。
请参见 确定更新是否需要主机处于维护模式或重新引导。请参见将主机置于维护模式。
重要说明 使用 ESXCLI 更新或升级主机时，请手动将主机置于维护模式，以确保在升级开始之前引导 磁盘未在使用中。 n
如果更新需要重新引导，并且主机属于 vSphere HA 集群，请从集群中移除该主机或停用集群上的 HA。 步骤 1 确定在主机上安装的 VIB。
esxcli --server=<server_name> software vib list 2 确定库中可用的映像配置文件。
esxcli --server=<server_name> software sources profile list --depot=http://<web_server>/ <depot_name>
可以使用 --proxy 参数指定代理服务器。
VMware ESXi 升级
VMware, Inc.
72
[第73页]
3
更新现有的映像配置文件以包含 VIB 或安装新的 VIB。
重要说明 software profile update 命令使用指定配置文件中的相应 VIB 来更新现有的 VIB，
但不影响目标服务器上安装的其他 VIB。software profile install 命令安装库映像配置文件中
显示的 VIB，并且移除目标服务器上安装的任何其他 VIB。
选项
描述
通过 VMware 提供的库中的 ZIP 包（可
从 VMware 网站联机访问或下载到本地
库）更新映像配置文件
esxcli software profile update --depot=<depot_location> --
profile=<profile_name>
重要说明 对于 VMware 提供的 ZIP 包，VMware 仅支持这一种更新方法。
VMware 提供的 ZIP 包文件名采用以下格式：VMware-ESXi-
<version_number>-<build_number>-depot.zip。
VMware 提供的 ZIP 包的配置文件名采用以下格式之一： n
ESXi-<version_number>-<build_number>-standard n
ESXi-<version_number>-<build_number>-notools（不包括 VMware Tools）
从可通过 URL 访问的库中更新映像配置
文件
esxcli --server=<server_name> software profile update --
depot=http://<web_server>/<depot_name> --
profile=<profile_name>
从本地存储在目标服务器上的 ZIP 文件
中更新映像配置文件
esxcli --server=<server_name> software profile update --
depot=file:///<path_to_profile_ZIP_file>/
<profile_ZIP_file> --profile=<profile_name>
从复制到数据存储的目标服务器上的 ZIP
文件中更新映像配置文件
esxcli --server=<server_name> software profile update --
depot=<datastore_name>/<profile_ZIP_file> --
profile=<profile_name>
从复制到目标服务器本地并在其上应用的
ZIP 文件中更新映像配置文件
esxcli --server=<server_name> software profile update --
depot=/<root_dir>/<path_to_profile_ZIP_file>/
<profile_ZIP_file> --profile=<profile_name>
将所有新 VIB 安装在可通过 URL 访问的
指定配置文件中
esxcli --server=<server_name> software profile install --
depot=http://<web_server>/<depot_name> --
profile=<profile_name>
从本地存储在目标上的 ZIP 文件中将所
有新 VIB 安装在指定配置文件中。
esxcli --server=<server_name> software profile install --
depot=file:///<path_to_profile_ZIP_file>/
<profile_ZIP_file> --profile=<profile_name>
从复制到目标服务器上数据存储的 ZIP
文件中安装所有新 VIB
esxcli --server=<server_name> software profile install --
depot=<datastore_name>/<profile_ZIP_file> --
profile=<profile_name>
从复制到目标服务器本地并在其上应用的
ZIP 文件中安装所有新 VIB
esxcli --server=<server_name> software profile install --
depot=/<root_dir>/<path_to_profile_ZIP_file>/
<profile_ZIP_file> --profile=<profile_name> VMware ESXi 升级 VMware, Inc. 73 [第74页] 4
验证 VIB 是否已安装在 ESXi 主机上。
esxcli --server=<server_name> software vib list
使用 Zip 文件更新 ESXi 主机
您可通过下载库的 ZIP 文件，以 VIB 或映像配置文件更新主机。
VMware 合作伙伴准备第三方 VIB 以提供管理代理或异步发行的驱动程序。
重要说明 如果要通过 VMware 提供的库中 ZIP 包更新 ESXi（可以登录 VMware 网站在线更新，或者下
载到本地进行更新），VMware 仅支持主题使用映像配置文件升级或更新主机 中为 VMware 提供的库指 定的更新方法。
不支持使用 esxcli software vib update 和 esxcli software vib install 命令进行升级。
请参见使用映像配置文件升级或更新主机 。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
n
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 n
下载由第三方 VMware 合作伙伴提供的库的 ZIP 包文件。 n
确定更新是否需要将主机置于维护模式或重新引导主机。如有必要，请将主机置于维护模式。
请参见 确定更新是否需要主机处于维护模式或重新引导。请参见将主机置于维护模式。 n
如果更新需要重新引导，并且主机属于 vSphere HA 集群，请从集群中移除该主机或停用集群上的 HA。 步骤 u 安装该 ZIP 文件。
esxcli --server=<server_name> software vib update --depot=/<path_to_vib_ZIP>/
<ZIP_file_name>.zip
从主机中移除 VIB
可以从 ESXi 主机卸载第三方 VIB 或 VMware VIB。
VMware 合作伙伴准备第三方 VIB 以提供管理代理或异步发行的驱动程序。
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 前提条件 n
如果移除需要重新引导，并且主机属于 vSphere HA 集群，请停用主机的 HA。 VMware ESXi 升级 VMware, Inc. 74 [第75页] n
确定更新是否需要将主机置于维护模式或重新引导主机。如有必要，请将主机置于维护模式。
请参见 确定更新是否需要主机处于维护模式或重新引导。请参见将主机置于维护模式。
重要说明 要确保在使用 ESXCLI 更新或升级主机时引导磁盘未在使用中，请手动将主机置于维护模 式。 n
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1
关闭 ESXi 主机上运行的每个虚拟机的电源。
注 可以通过运行以下命令列出所有正在运行的虚拟机并检索每个虚拟机的环境 ID。
esxcli --server=<server_name> vm process list 选项 命令
关闭客户机操作系统，然后再关闭虚拟机
电源
esxcli --server=<server_name> vm process kill --type soft
--world-id <vm_ID>
立即关闭虚拟机电源
esxcli --server=<server_name> vm process kill --type hard
--world-id <vm_ID>
强制执行关闭电源操作
esxcli --server=<server_name> vm process kill --type
force --world-id <vm_ID>
此外，为避免关闭虚拟机的电源，可以将其迁移至其他主机。请参见《《vCenter Server 和主机管
理》》文档中的主题“迁移虚拟机”。
2
将主机置于维护模式。
esxcli --server=<server_name> system maintenanceMode set --enable true 3
如果需要，请关闭或迁移虚拟机。
4
确定在主机上安装的 VIB。
esxcli --server=<server_name> software vib list 5 移除 VIB。
esxcli --server=<server_name> software vib remove --vibname=<name>
通过以下形式之一指定要移除的一个或多个 VIB。
n
<name>
n
<name>:<version>
VMware ESXi 升级
VMware, Inc.
75
[第76页]
n
<vendor>:<name>
n
<vendor>:<name>:<version>
例如，移除按供应商、名称和版本指定的 VIB 的命令可采用以下形式。
esxcli –-server myEsxiHost software vib remove --vibname=PatchVendor:patch42:version3
注 remove 命令支持更多选项。请参见《ESXCLI 参考指南》。
使用 ESXCLI 命令将第三方扩展添加到主机
可以使用 esxcli software vib 命令将作为 VIB 软件包发布的第三方扩展添加到系统。如果使用此命
令，则在重新引导系统之后，VIB 系统将更新防火墙规则集并刷新主机守护进程。
另外，您可以使用防火墙配置文件指定要为扩展启用的主机服务的端口规则。《vSphere 安全性》文档讨
论了如何添加、应用和刷新防火墙规则集，并列出了 esxcli network firewall 命令。
执行 ESXCLI 安装或升级试运行
可以使用 --dry-run 选项预览安装或升级操作的结果。安装或更新程序练习不会进行任何更改，但会在运
行不带 --dry-run 选项的命令时报告将要执行的 VIB 级操作。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1
输入安装或升级命令，同时添加 --dry-run 选项。
n
esxcli --server=<server_name> software vib install --dry-run n
esxcli --server=<server_name> software vib update --dry-run n
esxcli --server=<server_name> software profile install --dry-run n
esxcli --server=<server_name> software profile update --dry-run 2 查看返回的输出。
输出结果会显示将安装或移除的 VIB，以及安装或更新是否需要重新引导。 VMware ESXi 升级 VMware, Inc. 76 [第77页]
显示将在下一次重新引导主机后激活的已安装 VIB 和配置文件
您可以使用 --rebooting-image 选项列出安装在主机上并且将在下一次重新引导主机后激活的 VIB 和配 置文件。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1 输入以下命令之一。 选项 描述 对于 VIB
esxcli --server=<server_name> software vib list --
rebooting-image
对于配置文件
esxcli --server=<server_name> software profile get --
rebooting-image
2
查看返回的输出。
输出显示有关将在下一次重新引导后激活的 ESXi 映像的信息。如果尚未创建挂起重新引导映像，则输 出不会返回任何内容。
显示主机的映像配置文件和接受程度
您可以使用 software profile get 命令针对指定的主机显示当前安装的映像配置文件和接受程度。
此命令还可显示已安装映像配置文件历史记录的详细信息，包括配置文件修改。
使用 --server=<server_name> 指定目标服务器时，服务器将提示您输入用户名和密码。支持其他连接选
项，如配置文件或会话文件。有关连接选项的列表，请参见《ESXCLI 入门》，或在 ESXCLI 命令提示符
处运行 esxcli --help。
前提条件
安装 ESXCLI。请参见《ESXCLI 入门》。要进行故障排除，请在 ESXi Shell 中运行 esxcli 命令。 步骤 1 输入以下命令。
esxcli --server=<server_name> software profile get 2 查看输出。 VMware ESXi 升级 VMware, Inc. 77 [第78页] 升级 ESXi 主机之后
要完成主机升级，请确保主机已重新连接到其管理 vCenter Server 系统并根据需要进行重新配置。还应检 查主机是否已获得正确的许可。
升级 ESXi 主机之后，请执行以下操作：
n
查看升级日志。可以使用 vSphere Client 导出日志文件。 n
如果由 vCenter Server 系统管理主机，必须将主机重新连接到 vCenter Server，方法是在 vCenter
Server 清单中右键单击主机并选择连接。
n
当升级完成后，ESXi 主机将进入评估模式。评估期为 60 天。您必须在评估期到期之前分配 vSphere
7.0 许可证。您可以升级现有许可证或从 My VMware 获取新的许可证。使用 vSphere Client 为环境
中的主机配置许可。有关管理 vSphere 中的许可证的详细信息，请参见《vCenter Server 和主机管 理》文档。 n
主机 sdX 设备可能会在升级之后重新编号。如有需要，可更新引用 sdX 设备的任何脚本。 n
升级主机上的虚拟机。请参见升级虚拟机和 VMware Tools。 n
设置 vSphere Authentication Proxy 服务。早期版本的 vSphere Authentication Proxy 与 vSphere
7.0 不兼容。有关配置 vSphere Authentication Proxy 服务的详细信息，请参见《vSphere 安全性》 文档。
关于 ESXi 评估和许可模式
可以使用评估模式来浏览 ESXi 主机的全套功能。评估模式提供了相当于 vSphere Enterprise Plus 许可证
的功能集。在评估模式到期之前，必须向主机分配支持正在使用的所有功能的许可证。
例如，在评估模式下，可以使用 vSphere vMotion 技术、vSphere HA 功能、vSphere DRS 功能以及其
他功能。如果要继续使用这些功能，必须分配支持它们的许可证。
ESXi 主机的安装版本始终以评估模式安装。ESXi Embedded 由硬件供应商预安装在内部存储设备上。它 可能处于评估模式或已预授权。
评估期为 60 天，从打开 ESXi 主机时开始计算。在 60 天评估期中的任意时刻，均可从许可模式转换为评
估模式。评估期剩余时间等于评估期时间减去已用时间。
例如，假设您使用了处于评估模式的 ESXi 主机 20 天，然后将 vSphere Standard Edition 许可证密钥分
配给了该主机。如果将主机设置回评估模式，则可以在评估期剩余的 40 天内浏览主机的全套功能。
对于 ESXi 主机，许可证或评估期到期会导致主机与 vCenter Server 的连接断开。所有已打开电源的虚拟
机将继续工作，但您无法打开任何曾关闭电源的虚拟机电源。无法更改已在使用中的功能的当前配置。无
法使用在许可证过期之前一直未使用的功能。
有关管理 ESXi 主机许可的信息，请参见《《vCenter Server 和主机管理》》文档。 VMware ESXi 升级 VMware, Inc. 78 [第79页]
为升级后的 ESXi 主机提供许可
升级到 ESXi 7.0 之后，必须应用 vSphere 7 许可证。
如果将 ESXi 主机升级到以相同数字开头的版本，则不需要将现有许可证替换为新许可证。例如，如果将主
机从 ESXi 6.5 升级到 6.7，则该主机可以使用相同的许可证。
如果将 ESXi 主机升级到以不同数字开头的版本，则必须应用新的许可证。例如，如果将 ESXi 主机从 6.x
升级到 7.0，需要使用 vSphere 7 许可证向主机提供许可。
将 ESXi 6.5 或 ESXi 6.7 主机升级到 ESXi 7.0 主机时，主机将进入 60 天的评估模式期，直至应用正确的
vSphere 7 许可证为止。请参见关于 ESXi 评估和许可模式。
您可以从 My VMware 获取 vSphere 7 许可证。获取 vSphere 7 许可证之后，必须使用 vSphere Client
中的许可证管理功能将其分配给所有已升级的 ESXi 7.0 主机。有关详细信息，请参见《vCenter Server
和主机管理》文档。如果使用脚本式方法升级到 ESXi 7.0，则可以提供 kickstart (ks) 文件中的许可证密 钥。
在升级后的 ESXi 主机上运行安全引导验证脚本
从不支持 UEFI 安全引导的 ESXi 旧版本升级 ESXi 主机之后，您可能能够启用安全引导。是否能够启用安
全引导取决于您执行升级的方式，以及升级是替换所有现有 VIB 还是保持某些 VIB 不变。您可以在执行升
级后运行验证脚本以确定升级后的安装是否支持安全引导。
要使安全引导成功，每个已安装 VIB 的签名必须在系统上可用。在安装 VIB 时，ESXi 的旧版本不会保存 签名。 n
如果使用 ESXCLI 命令升级，ESXi 的旧版本将安装新 VIB，因此不会保存其签名，并且无法实现安全 引导。 n
如果使用 ISO 升级，新 VIB 则会保存其签名。这同样适用于使用 ISO 的 vSphere Lifecycle Manager 升级。 n
如果有旧版 VIB 保留在系统上，这些 VIB 的签名不可用，无法进行安全引导。 n
如果系统使用第三方驱动程序，而 VMware 升级不包括新版本的驱动程序 VIB，则在升级后旧版
本的 VIB 仍会保留在系统上。
n
在极少数情况下，VMware 可能会停止持续开发特定 VIB，且不提供新版本的 VIB 来替换或弃用
它，因此在升级后旧版本的 VIB 会保留在系统上。
注 UEFI 安全引导还需要最新的引导加载程序。此脚本不会检查最新的引导加载程序。 前提条件 n
验证硬件是否支持 UEFI 安全引导。
n
验证是否所有 VIB 均已签名且接受级别至少为“合作伙伴支持”。如果 VIB 为“社区支持”级别，则 无法使用安全引导。 VMware ESXi 升级 VMware, Inc. 79 [第80页] 步骤 1
升级 ESXi 并运行以下命令。
/usr/lib/vmware/secureboot/bin/secureBoot.py -c 2 检查输出结果。
输出包含 Secure boot can be enabled 或 Secure boot CANNOT be enabled。 系统日志记录所需的可用空间
如果使用 Auto Deploy 安装了 ESXi7.0 主机，或如果独立于 VMFS 卷上暂存目录中的默认位置设置日志
目录，则可能需要更改当前日志大小和轮换设置以确保存在足够的空间用于系统日志记录。
所有 vSphere 组件都使用此基础架构。此基础架构中的日志容量的默认值有所不同，具体取决于可用的存
储量和系统日志记录的配置方式。使用 Auto Deploy 部署的主机将日志存储在内存磁盘上，这意味着日志 的可用空间量较小。
如果使用 Auto Deploy 配置主机，则通过以下方式之一重新配置日志存储： n
通过网络将日志重定向至远程收集器。
n
将日志重定向至 NAS 或 NFS 存储。
如果将日志重定向至非默认存储，例如 NAS 或 NFS 存储，可能还要为安装到磁盘的主机重新配置日志大 小和轮换。
无需为使用默认配置的 ESXi 主机重新配置日志存储，这些主机会将日志存储在 VMFS 卷上的暂存目录
中。对于这些主机，ESXi7.0 会配置最适合安装的日志，并会提供足够的空间来容纳日志消息。
表 3-11. 建议的 hostd、vpxa 和 fdm 日志的最小大小和轮换配置 日志 最大日志文件大小 要保留的轮换数 所需最小磁盘空间 管理代理 (hostd) 10 MB 10 100 MB
VirtualCenter 代理 (vpxa)
5 MB
10
50 MB
vSphere HA 代理（故障域
管理器，fdm）
5 MB
10
50 MB
有关设置和配置 syslog 和 syslog 服务器以及安装 vSphere Syslog Collector 的信息，请参见
《《vCenter Server 安装和设置》》文档。
在 ESXi 主机上配置 Syslog
可以使用 vSphere Client、VMware Host Client 或 esxcli system syslog 命令配置 syslog 服务。
有关使用 esxcli system syslog 命令和其他 ESXCLI 命令的信息，请参见《ESXCLI 入门》。有关如
何为每个远程主机规范中指定的端口打开 ESXi 防火墙的详细信息，请参见 ESXi 防火墙配置。 步骤 1
在 vSphere Client 清单中，浏览到主机。
VMware ESXi 升级
VMware, Inc.
80
[第81页]
2
单击配置。
3
在系统下，单击高级系统设置。
4
单击编辑。
5
筛选出 syslog。
6
要全局设置日志记录并配置各种高级设置，请参见ESXi Syslog 选项。 7
（可选） 要覆盖任何日志的默认日志大小和日志轮换，请执行以下操作： a 单击要自定义的日志的名称。 b 输入所需的轮换数和日志大小。 8 单击确定。 结果
对 syslog 选项的更改生效。
注 使用 vSphere Client 或 VMware Host Client 定义的 Syslog 参数设置将立即生效。但是，使用
ESXCLI 定义的大多数设置都需要额外命令才能生效。有关更多详细信息，请参见ESXi Syslog 选项。 ESXi Syslog 选项
可以使用一组 syslog 选项定义 ESXi syslog 文件和传输的行为。
除了基本设置（如 Syslog.global.logHost）之外，从 ESXi 7.0 Update 1 开始，还提供了用于自定
义和 NIAP 合规性的高级选项列表。
注 所有审核记录设置（以 Syslog.global.auditRecord 开头）会立即生效。但是，对于使用
ESXCLI 定义的其他设置，请确保运行 esxcli system syslog reload 命令以启用更改。 VMware ESXi 升级 VMware, Inc. 81 [第82页]
表 3-12. 旧版 Syslog 选项
选项
ESXCLI 命令
描述
Syslog.global.logHost
esxcli system syslog config
set --loghost=<str>
定义有关消息传输的以逗号分隔的远程主
机列表和规范。如果 loghost=<str>
字段为空，则不会转发任何日志。虽然对
接收 syslog 消息的远程主机数量没有硬
性限制，但最好将远程主机的数量保持在
5 个或 5 个以下。远程主机规范的格式
为：protocol://hostname|
ipv4|'['ipv6']'[:port]。该协议必须
是 TCP、UDP 或 SSL 之一。端口值可以
是介于 1 到 65535 之间的任何十进制数
字。如果未提供端口，则 SSL 和 TCP 使
用 1514。UDP 使用 514。例如：ssl://
hostName1:1514。
Syslog.global.defaultRotate
esxcli system syslog config
set --default-rotate=<long>
要保留的旧日志文件的最大数目。您可以
在全局范围内设置该数字，也可以针对单
个子记录器设置该数字（请参见
Syslog.global.defaultSize）。
Syslog.global.defaultSize
esxcli system syslog config
set --default-size=<long>
日志文件的默认大小 (KiB)。文件达到默
认大小后，syslog 服务会创建一个新文
件。可以在全局范围内设置该数目，也可
以为单个子记录器设置该数目。
Syslog.global.logDir
esxcli system syslog config
set --logdir=<str>
日志所在的目录。该目录可以位于挂载的
NFS 或 VMFS 卷中。只有本地文件系统
中的 /scratch 目录在重新引导后仍然
存在。将目录指定为 [数据存储名称] 文
件路径，其中，路径是相对于支持数据存
储卷的 root 目录的路径。例如，路径
[storage1] /systemlogs 将映射为
路径 /vmfs/volumes/storage1/
systemlogs。
Syslog.global.logDirUnique
esxcli system syslog config
set --logdir-unique=<bool>
指定要与 Syslog.global.logDir 值
连接的 ESXi 主机名。当多个 ESXi 主机
登录到共享文件系统时，启用此设置至关
重要。选择此选项将使用 ESXi 主机的名
称在 Syslog.global.LogDir 指定的目录
下创建子目录。如果多个 ESXi 主机使用
同一个 NFS 目录，则唯一的目录非常有
用。
Syslog.global.certificate.chec
kSSLCerts
esxcli system syslog config
set --check-ssl-certs=<bool>
将消息传输到远程主机时强制检查 SSL
证书。
VMware ESXi 升级
VMware, Inc.
82
[第83页]
表 3-13. 从 ESXi 7.0 Update 1 开始可用的 Syslog 选项 选项 ESXCLI 命令 描述
Syslog.global.auditRecord.stor
ageCapacity
esxcli system auditrecords
local set --size=<long>
指定位于 ESXi 主机上的审核记录存储目
录的容量（以 MiB 为单位）。无法减少
审核记录存储的容量。可以在启用审核记
录存储之前或之后（请参见
Syslog.global.auditRecord.stor
ageEnable）增加容量。
Syslog.global.auditRecord.remo
teEnable
esxcli system auditrecords
remote enable
启用将审核记录发送到远程主机的功能。
远程主机通过使用
Syslog.global.logHost 参数指定。
Syslog.global.auditRecord.stor
ageDirectory
esxcli system auditrecords
local set --directory=<dir>
指定审核记录存储目录的位置。启用审核
记录存储（请参见
Syslog.global.auditRecord.stor
ageEnable）后，无法更改审核记录存
储目录。
Syslog.global.auditRecord.stor
ageEnable
esxcli system auditrecords
local enable
在 ESXi 主机上启用审核记录存储。如果
审核记录存储目录不存在，则使用
Syslog.global.auditRecord.stor
ageCapacity 指定的容量创建该目录。
Syslog.global.certificate.chec
kCRL
esxcli system syslog config
set --crl-check=<bool>
启用检查 SSL 证书链中所有证书的吊销
状态。
启用 X.509 CRL 验证，默认情况下不会
根据行业约定检查这些 CRL。经过 NIAP
验证的配置需要进行 CRL 检查。由于实
施限制，如果启用了 CRL 检查，则证书
链中的所有证书都必须提供 CRL 链接。
不要为与认证无关的安装启用 crl-
check 选项，因为很难正确配置使用
CRL 检查的环境。
Syslog.global.certificate.stri
ctX509Compliance
esxcli system syslog config
set --x509-strict=<bool>
启用严格遵守 X.509。在验证期间对 CA
根证书执行额外的有效性检查。通常不会
执行这些检查，因为 CA 根本来就受信
任，并且可能会导致与现有配置错误的
CA 根不兼容。经过 NIAP 验证的配置甚
至需要 CA 根来通过验证。
不要为与认证无关的安装启用 x509-
strict 选项，因为很难正确配置使用
CRL 检查的环境。
Syslog.global.droppedMsgs.file
Rotate
esxcli system syslog config
set --drop-log-rotate=<long>
指定要保留的旧的已丢弃消息日志文件
数。
Syslog.global.droppedMsgs.file
Size
esxcli system syslog config
set --drop-log-size=<long>
指定切换为新的日志文件之前每个已丢弃
消息日志文件的大小 (KiB)。
VMware ESXi 升级
VMware, Inc.
83
[第84页]
表 3-13. 从 ESXi 7.0 Update 1 开始可用的 Syslog 选项 （续） 选项 ESXCLI 命令 描述
Syslog.global.logCheckSSLCerts
esxcli system syslog config
set --check-ssl-certs=<bool>
将消息传输到远程主机时强制检查 SSL
证书。
注 已弃用。在 ESXi 7.0 Update 1 及更
高版本中使用
Syslog.global.certificate.chec
kSSLCerts。
Syslog.global.logFilters
esxcli system syslog logfile
[add | remove | set] ...
指定一个或多个日志筛选规范。每个日志
筛选器必须用双竖线“||”分隔。日志筛
选器的格式为：numLogs | ident |
logRegexp。numLogs 为指定的日志消
息设置最大日志条目数。达到此数目之
后，将会筛选并忽略指定日志消息。
ident 指定一个或多个系统组件以将筛
选器应用于这些组件生成的日志消息。
logRegexp 使用 Python 正则表达式语
法指定区分大小写的短语，以按内容筛选
日志消息。
Syslog.global.logFiltersEnable
允许使用日志筛选器。
Syslog.global.logLevel
esxcli system config set --
log-level=<str>
指定日志筛选级别。仅当对 syslog 守护
进程问题进行故障排除时，才必须更改此
参数。可以使用值 debug 表示最详细级
别，使用 info 表示默认详细级别，使用
warning 表示仅警告或错误，使用
error 表示仅错误。
Syslog.global.msgQueueDropMark
esxcli system syslog config --
queue-drop-mark=<long>)
指定占消息队列容量的百分比，达到此值
后丢弃消息。
Syslog.global.remoteHost.conne
ctRetryDelay
esxcli system syslog config
set --default-timeout=<long>
指定连接尝试失败后重试连接到远程主机
之前的延迟（以秒为单位）。
Syslog.global.remoteHost.maxMs
gLen
esxcli system syslog config
set --remote-host-max-msg-
len=<long>
对于 TCP 和 SSL 协议，此参数指定截断
发生之前 syslog 传输的最大长度（以字
节为单位）。远程主机消息的默认最大长
度为 1 KiB。可以将最大消息长度增加到
多达 16 KiB。但是，将此值提高到 1 KiB
以上不能确保长传输到达 syslog 收集器
时未被截断。例如，发出消息的 syslog
基础架构位于 ESXi 外部时。
RFC 5426 将 UDP 协议的最大消息传输
长度设置为 480 字节 (IPV4) 和 1180 字
节 (IPV6)。
Syslog.global.vsanBacking
esxcli system syslog config
set --vsan-backing=<bool>
允许将日志文件和审核记录存储目录放置
在 vSAN 集群上。但是，启用此参数可
能会导致 ESXi 主机变得无响应。
VMware ESXi 升级
VMware, Inc.
84
[第85页]
在 ESXi 主机上配置日志筛选
日志筛选功能可用于修改运行于 ESXi 主机上的 syslog 服务的日志记录策略。可以通过创建日志筛选器减
少 ESXi 日志中的重复条目数并将特定日志事件全部列入拒绝列表。
无论是记录到日志目录还是远程 syslog 服务器，日志筛选器将会影响由 ESXi 主机 vmsyslogd 守护进程 处理的所有日志事件。
创建日志筛选器时，为日志消息设置最大日志条目数。这些日志消息由一个或多个指定系统组件生成且与
指定短语匹配。要在 ESXi 主机上激活日志筛选器，必须启用日志筛选功能并重新加载 syslog 守护进程。
重要说明 如果设置日志记录信息量限制，则您可能无法正确地对潜在系统故障进行故障排除。如果在达到
最大日志条目数后发生日志轮换，则您可能会丢失已筛选消息的所有实例。 步骤 1
以 root 身份登录 ESXi Shell。
2
在 /etc/vmware/logfilters 文件中，添加下列条目以创建日志筛选器。
numLogs | ident | logRegexp
其中：
n
numLogs 为指定日志消息设置最大日志条目数。达到此数目之后，将会筛选并忽略指定日志消
息。使用 0 筛选并忽略所有指定日志消息。
n
ident 指定一个或多个系统组件以将筛选器应用于这些组件生成的日志消息。有关生成日志消息的
系统组件的信息，请参见 syslog 配置文件中的 idents 参数的值。这些文件位于 /etc/
vmsyslog.conf.d 目录中。使用逗号分隔列表将筛选器应用于多个系统组件。使用 * 将筛选器 应用于所有系统组件。 n
logRegexp 使用 Python 正则表达式语法指定区分大小写的短语以按内容筛选日志消息。
例如，对于包含 SOCKET connect failed, error 2: No such file or directory 短语和
任意错误号的消息，要将来自 hostd 组件的最大日志条目设置为 2，请添加以下条目：
2 | hostd | SOCKET connect failed, error .*: No such file or directory
注 以 # 开头的行表示备注，该行的其余部分将被忽略。
3
在 /etc/vmsyslog.conf 文件中，添加下列条目以启用日志筛选功能。
enable_logfilters = true
4
运行 esxcli system syslog reload 命令重新加载 syslog 守护进程并应用配置更改。 VMware ESXi 升级 VMware, Inc. 85 [第86页]
使用 vSphere Auto Deploy 重新置
备主机
4
如果某个主机是使用 vSphere Auto Deploy 部署的，则可以使用 vSphere Auto Deploy 通过包含不同版
本的 ESXi 的新映像配置文件重新置备该主机。可以使用 vSphere ESXi Image Builder 创建和管理映像配 置文件。
注 如果升级主机以使用 ESXi 6.0 或更高版本的映像，则 vSphere Auto Deploy 服务器会使用 VMCA 签
名的证书置备 ESXi 主机。如果当前使用自定义证书，则可将主机设置为在升级后使用自定义证书。请参见 《vSphere 安全性》。
如果升级对应的 vCenter Server 系统，vSphere Auto Deploy 服务器将自动升级。自版本 6.0 起，
vSphere Auto Deploy 服务器始终与 vCenter Server 系统位于相同的管理节点上。 本章讨论了以下主题： n
vSphere Auto Deploy 简介
n
准备 vSphere Auto Deploy
n
重新置备主机
vSphere Auto Deploy 简介
当启动为 vSphere Auto Deploy 设置的物理主机时，vSphere Auto Deploy 会将 PXE 引导基础架构与
《vSphere 主机配置文件》结合使用来置备并自定义该主机。主机本身并不存储任何状况，而是由
vSphere Auto Deploy 服务器管理每个主机的状况信息。 ESXi 主机的状况信息
vSphere Auto Deploy 会将要置备的 ESXi 主机的信息存储在不同位置中。最初，在将计算机映射到映像
配置文件和主机配置文件的规则中指定有关映像配置文件和主机配置文件的位置信息。
表 4-1. vSphere Auto Deploy 存储部署信息 信息类型 描述 信息源 映像状况
ESXi 主机上运行的可执行软件。
映像配置文件，使用 vSphere ESXi Image Builder 创建。 配置状况
确定主机如何配置的可配置设置，例如，虚拟交换机
及其设置、驱动程序设置、引导参数等。
使用主机配置文件 UI 创建的主机配置文件。通常来
自模板主机。
VMware, Inc.
86
[第87页]
表 4-1. vSphere Auto Deploy 存储部署信息 （续） 信息类型 描述 信息源 动态状况
由正在运行的软件生成的运行时状况，例如，生成的
专用密钥或运行时数据库。
重新引导时丢失的主机内存。
虚拟机状况
存储在主机上的虚拟机以及虚拟机自动启动信息（仅
限于后续引导）。
由 vCenter Server 向 vSphere Auto Deploy 发送
的虚拟机信息必须能够向 vSphere Auto Deploy 提 供虚拟机信息。 用户输入
基于用户输入的状况（如系统启动时用户提供的 IP
地址）无法自动包含在主机配置文件中。
在首次引导过程中，由 vCenter Server 存储的主机 自定义信息。
可以创建某些值需要用户输入的主机配置文件。
当 vSphere Auto Deploy 应用需要用户提供信息的
主机配置文件时，主机将置于维护模式。使用主机配
置文件 UI 可检查主机配置文件合规性，并对提示作
出响应以自定义主机。
vSphere Auto Deploy 架构
vSphere Auto Deploy 基础架构由若干个组件组成。
有关详细信息，请观看“Auto Deploy 架构”视频：
(Auto Deploy 架构 )
VMware ESXi 升级
VMware, Inc.
87
[第88页]
图 4-1. vSphere Auto Deploy 架构
通过 HTTP 获取映像/VIB
和主机配置文件（iPXE 引导
和更新）
主机配置文件
引擎
ESXi 主机
插件
VIB 和
映像配置文件
公用库
获取预定义映像
配置文件和 VIB
Auto Deploy
PowerCLI
规则引擎
Auto Deploy
服务器
（Web 服务器）
Image Builder
PowerCLI
映像
配置文件
主机配置文件
UI
主机配置文件和
主机自定义
vSphere Auto Deploy 服务器
为 ESXi 主机提供映像和主机配置文件。
vSphere Auto Deploy 规则引擎
向 vSphere Auto Deploy 服务器发送信息，告知哪个映像配置文件和哪个主机配置文件是为哪个主机
提供的。管理员使用 vSphere Auto Deploy 定义将映像配置文件和主机配置文件分配给主机的规则。 映像配置文件
定义一组用于引导 ESXi 主机的 VIB。
n
VMware 及其合作伙伴在公用库中提供了映像配置文件和 VIB。使用 vSphere ESXi Image
Builder 检查库，以及使用 vSphere Auto Deploy 规则引擎指定哪个映像配置文件分配给哪个主 机。 n
VMware 客户可以根据库中的公用映像配置文件和 VIB 创建自定义映像配置文件并将此文件应用 到主机。 主机配置文件
定义特定于计算机的配置，如网络连接或存储设置。使用主机配置文件 UI 创建主机配置文件。您可以
为引用主机创建主机配置文件，并将该主机配置文件应用到环境中的其他主机，以使配置一致。 主机自定义 VMware ESXi 升级 VMware, Inc. 88 [第89页]
存储在将主机配置文件应用到主机时由用户提供的信息。主机自定义可能包含 IP 地址或用户为该主机
提供的其他信息。有关主机自定义的详细信息，请参见《《vSphere 主机配置文件》》文档。
在先前版本的 vSphere Auto Deploy 中，主机自定义被称为应答文件。
准备 vSphere Auto Deploy
您必须先准备环境，然后才能开始使用 vSphere Auto Deploy。首先设置服务器并准备硬件。必须在计划
用于管理置备的主机的 vCenter Server 系统中配置 vSphere Auto Deploy 服务启动类型，然后安装 PowerCLI。 n
为系统准备 vSphere Auto Deploy
在可以通过 vSphere Auto Deploy 对 ESXi 主机进行 PXE 引导之前，必须安装必备软件并设置
vSphere Auto Deploy 与之交互的 DHCP 和 TFTP 服务器。 n
使用 vSphere Auto Deploy Cmdlet
vSphere Auto Deploy cmdlet 作为 Microsoft PowerShell cmdlet 实施并包含在 PowerCLI 中。
vSphere Auto Deploy cmdlet 的用户可以利用所有的 PowerCLI 功能。 n 设置批量许可
可以使用 vSphere Client 或 ESXi Shell 指定各个许可证密钥，或使用 PowerCLI cmdlet 设置批量
许可。批量许可适用于所有 ESXi 主机，但对使用 vSphere Auto Deploy 置备的主机尤其有用。
为系统准备 vSphere Auto Deploy
在可以通过 vSphere Auto Deploy 对 ESXi 主机进行 PXE 引导之前，必须安装必备软件并设置 vSphere
Auto Deploy 与之交互的 DHCP 和 TFTP 服务器。
如果要使用 PowerCLI cmdlet 管理 vSphere Auto Deploy，请参见使用 vSphere PowerCLI 设置
vSphere Auto Deploy 并置备主机。
前提条件
n
验证计划使用 vSphere Auto Deploy 进行置备的主机是否满足 ESXi 的硬件要求。请参见ESXi 硬件 要求。 n
验证 ESXi 主机是否已与 vCenter Server 建立网络连接，且满足所有端口要求。请参见vCenter Server。 n
确认您的环境中有 TFTP 服务器和 DHCP 服务器可以向 Auto Deploy 置备的 ESXi 主机发送文件并分
配网络地址。请参见#unique_76 和#unique_77。 n
验证 ESXi 主机与 DHCP、TFTP 和 vSphere Auto Deploy 服务器是否具有网络连接。 n
如果在 vSphere Auto Deploy 环境中要使用 VLAN，必须正确设置端到端网络。PXE 引导主机时，
必须将固件驱动程序设置为使用适当的 VLAN ID 来标记帧。这必须通过在 UEFI/BIOS 界面中进行正
确的更改来手动进行。还必须使用正确的 VLAN ID 来正确配置 ESXi 端口组。请咨询网络管理员以了
解 VLAN ID 在环境中的使用方式。
VMware ESXi 升级
VMware, Inc.
89
[第90页]
n
验证您是否具有足够存储空间用于 vSphere Auto Deploy 存储库。vSphere Auto Deploy 服务器使
用存储库存储其需要的数据，包括您创建的规则和规则集，以及在规则中指定的 VIB 和映像配置文 件。
最佳做法是分配 2 GB 以具有足够的空间容纳四个映像配置文件和一些额外空间。每个映像配置文件大
约需要 400 MB。通过考虑希望使用的映像配置文件数量来确定为 vSphere Auto Deploy 存储库预留 多少空间。 n
获取对 DHCP 服务器（该服务器管理要从其进行引导的网络段）的管理特权。可以使用环境中已有的
DHCP 服务器或安装一台 DHCP 服务器。对于 vSphere Auto Deploy 设置，请将 gpxelinux.0 文
件名替换为 snponly64.efi.vmw-hardwired（对于 UEFI）或 undionly.kpxe.vmw-
hardwired（对于 BIOS）。有关 DHCP 配置的详细信息，请参见示例 DHCP 配置。 n
就像保护使用任何其他基于 PXE 的部署方法的网络一样保护您的网络。vSphere Auto Deploy 通过
SSL 传输数据，以防止意外干扰和侦听。但是，在 PXE 引导期间不会检查客户端或 vSphere Auto
Deploy 服务器的真实性。
n
如果要使用 PowerCLI cmdlet 管理 vSphere Auto Deploy，请确认 Windows 计算机上装有
Microsoft .NET Framework 4.5 或 4.5.x 和 Windows PowerShell 3.0 或 4.0。请参见《vSphere
PowerCLI 用户指南》。
n
设置远程 Syslog 服务器。有关 Syslog 服务器配置信息，请参见《vCenter Server 和主机管理》文
档。将您引导的第一台主机配置为使用远程 Syslog 服务器并将主机的主机配置文件应用于所有其他目
标主机。或者，安装并使用 vSphere Syslog Collector，该工具是 vCenter Server 支持工具，提供了
统一的系统日志记录架构，能够进行网络日志记录并将多台主机的日志结合使用。 n
安装 ESXi Dump Collector 并设置第一台主机，以便所有核心转储都指向 ESXi Dump Collector 并将
该主机的主机配置文件应用于所有其他主机。
n
如果您计划使用 vSphere Auto Deploy 置备的主机带有旧版 BIOS，请验证 vSphere Auto Deploy
服务器是否采用 IPv4 地址。使用旧版 BIOS 固件进行 PXE 引导只能通过 IPv4 实现。使用 UEFI 固件
进行 PXE 引导可以通过 IPv4 或 IPv6 实现。
步骤
1
导航到主页 > Auto Deploy。
默认情况下，只有管理员角色才有权使用　vSphere Auto Deploy 服务。 2
在 Auto Deploy 页面上，从顶部下拉菜单中选择您的 vCenter Server。 3
单击启用 Auto Deploy 和 Image Builder 以激活服务。
如果 Image Builder 服务已处于活动状态，请选择配置选项卡，然后单击启用 Auto Deploy 服务。 此时将显示软件库页面。 VMware ESXi 升级 VMware, Inc. 90 [第91页] 4 配置 TFTP 服务器。 a 单击配置选项卡。 b
单击下载 TFTP Boot Zip 以下载 TFTP 配置文件，并将该文件解压缩到 TFTP 服务器存储文件的 目录下。 c
（可选） 要使用代理服务器，请单击 Auto Deploy 运行时摘要窗格上的添加，然后在文本框中输 入代理服务器 URL。
使用反向代理服务器可以卸载对 vSphere Auto Deploy 服务器发出的请求。 5
设置 DHCP 服务器，以指向 TFTP ZIP 文件所在的 TFTP 服务器。 a
在 DHCP 选项 66（通常称为 next-server）中指定 TFTP 服务器的 IP 地址。 b
在 DHCP 选项 67 中指定引导文件名（通常叫作 boot-filename）；对于 UEFI，它是
snponly64.efi.vmw-hardwired，而对于 BIOS，它是 undionly.kpxe.vmw- hardwired。 6
按照制造商的说明将要使用 vSphere Auto Deploy 置备的每个主机设置为网络引导或 PXE 引导。 7
（可选） 如果将环境设置为使用指纹模式，则通过将 OpenSSL 证书 rbd-ca.crt 和 OpenSSL 专用
密钥 rbd-ca.key 替换为自己的证书和密钥文件，便可使用自己的证书颁发机构 (CA)。
这些文件位于 /etc/vmware-rbd/ssl/ 中。
默认情况下，vCenter Server 使用 VMware Certificate Authority (VMCA)。 结果
在启动为 vSphere Auto Deploy 设置的 ESXi 主机时，该主机会与 DHCP 服务器联系并直接指向
vSphere Auto Deploy 服务器，这将使用活动规则集中指定的映像配置文件置备该主机。 后续步骤 n
可以更改 Auto Deploy 服务的默认配置属性。有关详细信息，请参见《vCenter Server 和主机管
理》文档中的“配置 vCenter Server”。
n
可以更改 Image Builder 服务的默认配置属性。有关详细信息，请参见《vCenter Server 和主机管
理》文档中的“配置 vCenter Server”。
n
定义一个将映像配置文件和可选主机配置文件、主机位置或脚本包分配给主机的规则。 n
（可选） 配置第一台置备为引用主机的主机。使用要针对目标主机共享的存储、网络和其他设置。为
该引用主机创建主机配置文件，并编写将已测试的映像配置文件和主机配置文件分配给目标主机的规 则。 n
（可选） 如果要使 vSphere Auto Deploy 覆盖现有分区，请将引用主机设置为进行自动分区并将引
用主机的主机配置文件应用于其他主机。
n
（可选） 如果必须配置特定于主机的信息，可以设置引用主机的主机配置文件，以便提示用户输入。
有关主机自定义的详细信息，请参见《《vSphere 主机配置文件》》文档。 VMware ESXi 升级 VMware, Inc. 91 [第92页]
使用 vSphere Auto Deploy Cmdlet
vSphere Auto Deploy cmdlet 作为 Microsoft PowerShell cmdlet 实施并包含在 PowerCLI 中。
vSphere Auto Deploy cmdlet 的用户可以利用所有的 PowerCLI 功能。
具有丰富经验的 PowerShell 用户可以像使用其他 PowerShell cmdlet 一样使用 vSphere Auto Deploy
cmdlet。如果您是 PowerShell 和 PowerCLI 的新用户，以下提示可能对您有所帮助。
您可以在 PowerCLI shell 中键入 cmdlet、参数和参数值。 n
通过运行 Get-Helpcmdlet_name 获取有关任何 cmdlet 的帮助。 n
请记住，PowerShell 不区分大小写。
n
对 cmdlet 名称和参数名称使用 Tab 自动补全。
n
使用 Format-List 或 Format-Table，或者它们的缩写 fl 或 ft 格式化任何变量和 cmdlet 输出。
有关详细信息，请运行 Get-Help Format-List cmdlet。 通过名称传递参数
在大多数情况下，可以通过名称传递参数，并使用双引号将包含空格或特殊字符的参数值引起来。
Copy-DeployRule -DeployRule testrule -ReplaceItem MyNewProfile
《vCenter Server 安装和设置》文档中的大多数示例均按名称传递参数。 将参数作为对象传递
如果希望执行脚本操作并实现自动化，则可以将参数作为对象传递。将参数作为对象传递对于返回多个对
象和返回单个对象的 cmdlet 都有用。请参见下面的示例：
1
将封装主机规则集合规信息的对象绑定到变量。
$tr = Test-DeployRuleSetCompliance MyEsxi42 2
查看对象的 itemlist 属性以查看规则集中的规则与主机当前使用的规则之间有何差异。 $tr.itemlist 3
通过将 Repair-DeployRuleSetCompliance cmdlet 与变量结合使用来修复主机，从而使用修改 后的规则集。
Repair-DeployRuleSetCompliance $tr
该示例将在下次引导主机时修复主机。
VMware ESXi 升级
VMware, Inc.
92
[第93页]
设置批量许可
可以使用 vSphere Client 或 ESXi Shell 指定各个许可证密钥，或使用 PowerCLI cmdlet 设置批量许可。
批量许可适用于所有 ESXi 主机，但对使用 vSphere Auto Deploy 置备的主机尤其有用。
通过 vSphere Client 分配许可证密钥和使用 PowerCLI cmdlet 分配许可的工作方式不同。
使用 vSphere Client 分配许可证密钥
将主机添加到 vCenter Server 系统时或主机由 vCenter Server 系统管理时，可为主机分配许可证密 钥。
使用 LicenseDataManager PowerCLI 分配许可证密钥
可以指定添加到一组主机中的一组许可证密钥。这些许可证将添加到 vCenter Server 数据库中。每当
将主机添加到 vCenter Server 系统或将主机重新连接到该系统时，都会为主机分配许可证密钥。通过
PowerCLI 分配的许可证密钥被视为默认的许可证密钥。添加或重新连接未获许可的主机时，将为主机
分配默认的许可证密钥。如果主机已获得许可，则可保留其许可证密钥。
下面的示例为数据中心中的所有主机分配许可证。您也可将许可证与主机和集群关联。
以下示例适用于了解如何使用 PowerShell 变量的高级 PowerCLI 用户。 前提条件
为系统准备 vSphere Auto Deploy.
步骤
1
在 PowerCLI 会话中，连接到想使用的 vCenter Server 系统，并将关联的许可证管理器绑定到某个变 量。
Connect-VIServer -Server 192.XXX.X.XX -User username -Password password
$licenseDataManager = Get-LicenseDataManager 2
运行检索数据中心的 cmdlet，要对其使用批量许可功能的主机位于该数据中心中。
$hostContainer = Get-Datacenter -Name Datacenter-X
也可以运行检索集群的 cmdlet 以对集群中的所有主机使用批量许可，或者运行检索文件夹的 cmdlet
以对文件夹中的所有主机使用批量许可。
3
创建 LicenseData 对象以及具有关联类型 ID 和许可证密钥的 LicenseKeyEntry 对象。
$licenseData = New-Object VMware.VimAutomation.License.Types.LicenseData $licenseKeyEntry
= New-Object Vmware.VimAutomation.License.Types.LicenseKeyEntry $licenseKeyEntry.TypeId =
"vmware-vsphere” $licenseKeyEntry.LicenseKey = "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX" 4
将步骤 3 中创建的 LicenseData 对象的 LicenseKeys 属性与 LicenseKeyEntry 对象关联。
$licenseData.LicenseKeys += $licenseKeyEntry VMware ESXi 升级 VMware, Inc. 93 [第94页] 5
使用 LicenseData 对象更新数据中心的许可证数据，并验证许可证是否与主机容器关联。
$licenseDataManager.UpdateAssociatedLicenseData($hostContainer.Uid, $licenseData)
$licenseDataManager.QueryAssociatedLicenseData($hostContainer.Uid) 6
使用 vSphere Auto Deploy 置备一个或多个主机，并将这些主机分配到为其分配许可证数据的数据中 心或集群中。 7
可以使用 vSphere Client 以验证主机是否成功分配到默认许可证 XXXXX-XXXXX-XXXXX-XXXXX- XXXXX。 结果
所有分配到数据中心的主机现在均已自动获得许可。
重新置备主机
vSphere Auto Deploy 支持多个重新置备选项。可以使用不同的映像配置文件或不同的主机配置文件执行 简单的重新引导或重新置备。
使用 vSphere Auto Deploy 首次引导时需要设置环境并将规则添加到规则集中。请参见《vSphere 安装
和设置》文档中的“准备 vSphere Auto Deploy”主题。 可用的重新置备操作如下： n 简单地重新引导。 n
重新引导用户在引导操作过程中回答其问题的主机。
n
使用不同的映像配置文件重新置备。
n
使用不同的主机配置文件重新置备。
通过简单的重新引导操作重新置备主机
使用 vSphere Auto Deploy 置备的主机的简单重新引导只要求仍满足所有的必备条件。此过程使用之前分
配的映像配置文件、主机配置文件、自定义脚本和 vCenter Server 位置。 前提条件 n
确认首次引导操作过程中执行的设置不变。
n
确认所有关联项可用。项可以是映像配置文件、自定义脚本或 vCenter Server 清单位置。 n
确认主机具有它在先前引导操作中具有的标识信息（资产标记、IP 地址）。 VMware ESXi 升级 VMware, Inc. 94 [第95页] 步骤 1 将主机置于维护模式。 主机类型 操作 主机是 DRS 集群的一部分
将主机置于维护模式时，VMware DRS 会将虚拟机迁移到相应主机。
主机不是 DRS 集群的一部分
必须将所有虚拟机迁移到不同主机，并将每一主机置于维护模式。
2
重新引导主机。
结果
主机关闭。主机重新引导时，将使用 vSphere Auto Deploy 服务器提供的映像配置文件。vSphere Auto
Deploy 服务器也应用存储在 vCenter Server 系统中的主机配置文件。
使用 PowerCLI 时用新映像配置文件重新置备主机
您可以在 PowerCLI 会话中，更改适用于主机的规则并执行测试和修复合规性操作，以便使用 vSphere
Auto Deploy 用新的映像配置文件重新置备主机。
重新置备主机存在多个选项。
n
如果要使用的 VIB 支持实时更新，则可以使用 esxcli software vib 命令。在这种情况下，还必
须更新规则集以使用包含新 VIB 的映像配置文件。
n
测试过程中，可以使用 Apply-EsxImageProfile cmdlet 将映像配置文件应用于单个主机并重新引
导主机以使更改生效。Apply-EsxImageProfile cmdlet 可更新主机和映像配置文件之间的关联， 但不在主机上安装 VIB。 n
在其他所有情况下，请使用此过程。
前提条件
n
确认要用于重新置备主机的映像配置文件可用。在 PowerCLI 会话中使用 vSphere ESXi Image
Builder。请参见《vSphere 安装和设置》文档中的“使用 vSphere ESXi Image Builder CLI”。 n
确认首次引导操作过程中执行的设置不变。
步骤
1
在 PowerShell 提示符下，运行 Connect-VIServer PowerCLI cmdlet 以连接到已向其注册
vSphere Auto Deploy 的 vCenter Server 系统。
Connect-VIServer ipv4_or_ipv6_address
Cmdlet 可能会返回服务器证书警告。在生产环境中，请确保不会产生服务器证书警告。在开发环境 中，可以忽略此警告。 2
确定包含要使用的映像配置文件的公用软件库的位置，或使用 vSphere ESXi Image Builder 定义自定 义映像配置文件。 VMware ESXi 升级 VMware, Inc. 95 [第96页] 3
运行 Add-EsxSoftwareDepot 将包含映像配置文件的软件库添加到 PowerCLI 会话。 库类型 Cmdlet 远程库
运行 Add-EsxSoftwareDepot depot_url。 ZIP 文件 a
将 ZIP 文件下载到本地文件路径，或者在 PowerCLI 计算机本地创建一个挂载 点。 b 运行
Add-EsxSoftwareDepot C:\file_path\my_offline_depot.zip。 4
运行 Get-EsxImageProfile 查看映像配置文件列表，并决定要使用的配置文件。 5
运行 Copy-DeployRule 并指定 ReplaceItem 参数以更改将映像配置文件分配给主机的规则。
以下 cmdlet 使用 my_new_imageprofile 配置文件替换规则分配给主机的当前映像配置文件。
cmdlet 完成后，myrule 会将新映像配置文件分配给主机。重命名并隐藏旧版本的 myrule。
Copy-DeployRule myrule -ReplaceItem my_new_imageprofile 6
测试要将映像部署到的每个主机的规则合规性。
a
验证您是否可以访问要测试规则集合规性的主机。
Get-VMHost -Name ESXi_hostname
b
运行 cmdlet 测试主机的规则集合规性，然后将返回值与变量绑定供以后使用。
$tr = Test-DeployRuleSetCompliance ESXi_hostname c
检查规则集的内容与主机配置之间的区别。
$tr.itemlist
如果要为其测试新规则集合规性的主机与活动规则集相符，系统将返回一个当前和预期项目表。
CurrentItem ExpectedItem
----------- ------------
my_old_imageprofilemy_new_imageprofile d
修复主机，以便在下次引导主机时使用修改后的规则集。
Repair-DeployRuleSetCompliance $tr 7
重新引导主机，以使用新映像配置文件置备主机。
编写规则并给主机分配主机配置文件
vSphere Auto Deploy 可以将一个主机配置文件分配给一个或多个主机。主机配置文件可能包含有关主机
的存储配置、网络配置或其他特性的信息。如果将主机添加到集群，则将使用该集群的主机配置文件。
多数情况下，将主机分配给集群，而不用明确指定主机配置文件。主机使用集群的主机配置文件。 VMware ESXi 升级 VMware, Inc. 96 [第97页] 前提条件 n
安装 PowerCLI 和所有必备软件。有关信息，请参见《《vCenter Server 安装和设置》》。 n 导出要使用的主机配置文件。 步骤 1
在 PowerCLI 会话中，运行 Connect-VIServer cmdlet 以连接到已注册了　vSphere Auto
Deploy 的 vCenter Server 系统。
Connect-VIServer ipv4_or_ipv6_address
Cmdlet 可能会返回服务器证书警告。在生产环境中，请确保不会产生服务器证书警告。在开发环境 中，可以忽略此警告。 2
使用 vSphere Client 设置主机，使该主机具有您要使用的设置，然后从该主机创建主机配置文件。 3
通过运行 Get-VMhostProfilePowerCLI cmdlet，并进入您创建主机配置文件的 ESXi 主机，查找 主机配置文件的名称。 4
在 PowerCLI 提示符处，定义一个规则，以将主机配置文件分配给具有某些属性（例如 IP 地址范围） 的主机。
New-DeployRule -Name "testrule2" -Item my_host_profile -Pattern "vendor=Acme,Zven",
"ipv4=192.XXX.1.10-192.XXX.1.20"
将指定项分配给具有指定属性的所有主机。此示例指定了一个名为 testrule2 的规则。该规则将指定的
主机配置文件 my_host_profile 分配给 IP 地址在指定范围内且制造商为 Acme 或 Zven 的所有主 机。 5 将规则添加到规则集。
Add-DeployRule testrule2
默认情况下，工作规则集将成为活动规则集，规则集的所有更改将在添加规则时处于活动状态。如果使
用 NoActivate 参数，则工作规则集不会成为活动规则集。 后续步骤 n
通过对已由 vSphere Auto Deploy 置备的主机执行合规性测试和修复操作，将其分配给新的主机配置
文件。有关详细信息，请参见 测试和修复规则合规性 。
n
打开未置备的主机电源，以使用主机配置文件对其进行置备。
测试和修复规则合规性
将规则添加到 vSphere Auto Deploy 规则集或修改一个或多个规则时，主机不会自动更新。仅当测试其规
则合规性并执行修复时，vSphere Auto Deploy 才应用新规则。 前提条件 n
准备系统并安装 Auto Deploy 服务器。有关详细信息，请参见为系统准备 vSphere Auto Deploy。 VMware ESXi 升级 VMware, Inc. 97 [第98页] n
验证基础架构是否包含一个或多个使用 vSphere Auto Deploy 置备的 ESXi 主机，并验证安装了
PowerCLI 的主机是否可以访问这些 ESXi 主机。
步骤
1
在 PowerCLI 会话中，运行 Connect-VIServer cmdlet 以连接到已注册了　vSphere Auto
Deploy 的 vCenter Server 系统。
Connect-VIServer ipv4_or_ipv6_address
Cmdlet 可能会返回服务器证书警告。在生产环境中，请确保不会产生服务器证书警告。在开发环境 中，可以忽略此警告。 2
使用 PowerCLI 查看当前可用的 vSphere Auto Deploy 规则。 Get-DeployRule
系统返回规则及关联的项目和模式。
3
修改可用规则之一。
例如，您可以更改映像配置文件和规则名称。
Copy-DeployRule -DeployRule testrule -ReplaceItem MyNewProfile
无法编辑已添加到活动规则集中的规则。但可以复制规则并替换要更改的项目或模式。 4
验证您是否可以访问要测试规则集合规性的主机。
Get-VMHost -Name MyEsxi42
5
运行 cmdlet 测试主机的规则集合规性，然后将返回值与变量绑定供以后使用。
$tr = Test-DeployRuleSetCompliance MyEsxi42 6
检查规则集的内容与主机配置之间的区别。
$tr.itemlist
如果要对其测试新规则集合规性的主机符合活动规则集，则系统将返回包含当前项目和预期项目的表。
CurrentItem ExpectedItem
----------- ------------
My Profile 25 MyNewProfile 7
修复主机，以便在下次引导主机时使用修改后的规则集。
Repair-DeployRuleSetCompliance $tr VMware ESXi 升级 VMware, Inc. 98 [第99页] 后续步骤
如果您更改的规则指定了清单位置，则更改会在您修复合规性时生效。对于其他所有更改，请重新引导主
机以使 vSphere Auto Deploy 应用新规则并实现规则集与主机之间的合规性。 VMware ESXi 升级 VMware, Inc. 99 [第100页]
收集日志以对 ESXi 主机进行故障排
除
5
可以收集 ESXi 的安装或升级日志文件。如果安装或升级失败，查看这些日志文件可帮助确定失败的原因。 解决方案 1
在 ESXi Shell 中或通过 SSH 输入 vm-support 命令。 2
导航到 /var/tmp/ 目录。
3
检索 .tgz 文件中的日志文件。
VMware, Inc.
100