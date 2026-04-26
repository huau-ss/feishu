---
title: "vCenter Server 配置"
doc_id: "6dcaeeb0-e27f-4b53-bf1e-1fb43facf33f"
source_file: "C:\Users\huaci\Desktop\VMware\vSphere\vCenter Server 閰嶇疆.pdf"
file_type: "pdf"
doc_type: "price_list"
cleaned_at: "2026-04-25 00:02:10"
---

# vCenter Server 配置

## 基本信息

| 字段 | 值 |
|------|-----|
| 文档ID | `6dcaeeb0-e27f-4b53-bf1e-1fb43facf33f` |
| 来源文件 | `C:\Users\huaci\Desktop\VMware\vSphere\vCenter Server 閰嶇疆.pdf` |
| 文件类型 | `pdf` |
| 文档类型 | `price_list` |
| 清洗时间 | `2026-04-25 00:02:10` |

## 清洗警告

- 自动检测 PDF 类型: marketing_whitepaper

---

## 正文

[第1页]
vCenter Server 配置
Update 3
VMware vSphere 7.0
VMware ESXi 7.0
vCenter Server 7.0
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
© 2019-2021 VMware, Inc. 保留所有权利。 版权和商标信息
vCenter Server 配置
VMware, Inc.
2
[第3页]
目录
关于 vCenter Server 配置
6
1
vCenter Server 配置概述
7
Platform Services Controller 发生了什么情况 8
2 使用 vCenter Server 管理界面配置 vCenter Server 9
登录 vCenter Server 管理界面
10
查看 vCenter Server 运行状况
10
重新引导或关闭 vCenter Server
11
创建支持包
11
监控 CPU 和内存使用情况
12
监控磁盘使用情况
12
监控网络使用情况
12
监控数据库使用情况
13
启用或禁用 SSH 访问和 Bash Shell 访问
13
配置 DNS、IP 地址和代理设置
14
重新配置主网络标识符
16
编辑防火墙设置
17
配置系统时区和时间同步设置
18
启动、停止和重新启动服务
18
配置更新设置
19
更改 root 用户的密码和密码过期设置
19
将 vCenter Server 日志文件转发到 远程 Syslog 服务器 20 配置和调度备份 21
3 使用 vSphere Client 配置 vCenter Server 22
配置 vCenter Server
22
配置 vCenter Server 的许可证设置
22
配置统计信息设置
23
为 vCenter Server 配置运行时设置
25
配置用户目录设置
26
配置邮件发件人设置
27
配置 SNMP 设置
28
查看端口设置
29
配置超时设置
29
配置日志记录选项
30
配置数据库设置
31
VMware, Inc.
3
[第4页]
验证旧版主机的 SSL 证书
31
配置高级设置
32
向其他已登录用户发送消息
33
加入或退出 Active Directory 域
33
将用户添加到 SystemConfiguration.BashShellAdministrators 组中 35 重新引导节点 36 查看 节点的运行状况 36 导出支持包 37
4 使用设备 Shell 配置 vCenter Server
38
访问设备 Shell
38
从设备 Shell 启用和访问 Bash Shell
39
用于编辑命令的键盘快捷键
39
获取有关设备中插件和 API 命令的帮助
40
vCenter ServerShell 中的插件
41
使用 showlog 插件浏览日志文件
42
设备 Shell 中的 API 命令
42
配置 vCenter Server 的 SNMP
47
配置轮询的 SNMP 代理
47
为 SNMP v1 和 v2c 配置 vCenter Server 47
为 SNMP v3 配置 vCenter Server
49
配置 SNMP 代理以筛选通知
52
配置 SNMP 管理客户端软件
52
将 SNMP 设置重置为出厂默认设置
53
配置 vCenter Server 中的时间同步设置
53
使用 VMware Tools 时间同步
54
在 vCenter Server 配置中添加或替换 NTP 服务器 54
将 vCenter Server 中的时间与 NTP 服务器同步 55
管理 vCenter Server 中的本地用户帐户
55
vCenter Server 中的用户角色
55
获取 vCenter Server 中的本地用户帐户列表
56
在 vCenter Server 中创建本地用户帐户
56
更新 vCenter Server 中的本地用户密码
57
更新 vCenter Server 中的本地用户帐户
57
删除 vCenter Server 中的本地用户帐户
58
监控 vCenter Server 中的运行状况和统计信息
58
使用 vimtop 插件监控服务的资源使用情况
59
通过在交互模式中使用 vimtop 监控服务
59
交互模式命令行选项
60
vimtop 的交互模式单键命令
60
vCenter Server 配置
VMware, Inc.
4
[第5页]
5 使用直接控制台用户界面配置 vCenter Server
62
登录直接控制台用户界面
62
更改 root 用户的密码
63
配置 vCenter Server 的管理网络
63
重新启动 vCenter Server 的管理网络
64
启用对 Bash Shell 的访问
64
访问 Bash shell 以进行故障排除。
65
导出 vCenter Server 支持包以进行故障排除
65
vCenter Server 配置
VMware, Inc.
5
[第6页]
关于 vCenter Server 配置
《vCenter Server 配置》提供有关配置 VMware vCenter® Server™ 的信息。 目标读者
本信息面向需要配置 VMware vCenter Server® 的所有用户。本信息的目标读者为熟悉虚拟机技术和数据
中心操作且具有丰富经验的系统管理员。
VMware 非常重视包容性。为了在客户、合作伙伴和内部社区中促进这一原则，我们采用包容性语言创建 内容。
vSphere Client 和 vCenter Server 管理界面
本指南中的说明体现的是 vSphere Client（基于 HTML5 的 GUI）和 vCenter Server 管理界面。可以使
用 vCenter Server Appliance Shell 和直接控制台用户界面执行其他一些功能。 VMware, Inc. 6 [第7页]
vCenter Server 配置概述
1
vCenter Server 部署时使用预配置的虚拟机，以针对运行 VMware vCenter Server® 及关联服务进行优 化。
部署 vCenter Server 时，可以创建 VMware vCenter® Single Sign-On™ 域或加入现有域。有关 vCenter
Server 部署的信息，请参见《vCenter Server 安装和设置》。
VMware ESXi™ 6.0 及更高版本支持 vCenter Server。软件包包含以下软件： n
Project Photon OS® 3.0
n
PostgreSQL 数据库
n
vCenter Server 7.0 和 vCenter Server 7.0 组件 n
运行 vCenter Server 所需的服务，如 vCenter Single Sign-On、License Service 和 VMware
Certificate Authority
有关身份验证的详细信息，请参见《vSphere 身份验证》。
不支持对预配置的虚拟机进行自定义，除非添加内存、CPU 和磁盘空间。
vCenter Server 具有以下默认用户名：
n
root 用户，使用部署虚拟设备期间设置的密码。使用 root 用户登录 vCenter Server 管理界面和预配 置虚拟机的操作系统。
重要说明 默认情况下，vCenter Server 的 root 帐户的密码会在 365 天后过期。有关更改 root 密码
和配置密码过期设置的信息，请参见更改 root 用户的密码和密码过期设置。 n
administrator@your_domain_name（vCenter Single Sign-On 用户），使用部署设备期间设置的 密码和域名。
安装 vCenter Server 时，可以更改 vSphere 域。请勿使用与 Microsoft Active Directory 域名或
OpenLDAP 域名相同的域名。
最初，仅用户 administrator@your_domain_name 有权登录到 vCenter Server 系统。默认情况
下，administrator@your_domain_name 用户是 SystemConfiguration.Administrators 组的成
员。该用户可以添加标识源，在该标识源中可将更多用户和组定义为 vCenter Single Sign-On，或为
用户和组提供权限。有关详细信息，请参见《vSphere 安全性》。
可以通过四种方法配置 vCenter Server 设置：
n
使用 vCenter Server 管理界面。
VMware, Inc.
7
[第8页]
可以编辑系统设置，如访问权限、网络、时间同步和 root 密码设置。这是配置 vCenter Server 的首 选方法。 n
使用 vSphere Client。
可以导航到 vCenter Server 的系统配置设置，并将部署加入到 Active Directory 域。可以管理在
vCenter Server 中运行的服务并修改访问权限、网络和防火墙设置等各种设置。 n 使用 Bash shell。
可以使用 TTY1 登录到控制台，也可以使用 SSH 并在 vCenter Server 中运行配置、监控以及故障排除 命令。 n 使用直接控制台用户界面。
可以使用 TTY2 登录 vCenter Server 直接控制台用户界面更改 root 用户的密码、配置网络设置或启
用对 Bash shell 或 SSH 的访问。
本章讨论了以下主题：
n
Platform Services Controller 发生了什么情况
Platform Services Controller 发生了什么情况
在 vSphere 7.0 中，所有 Platform Services Controller 服务都将整合到 vCenter Server 中。
从 vSphere 7.0 开始，在 vSphere 7.0 中部署或升级 vCenter Server 需要使用 vCenter Server
Appliance，它是针对运行 vCenter Server 而优化的预配置虚拟机。新的 vCenter Server 包含所有
Platform Services Controller 服务，同时保留功能和工作流，包括身份验证、证书管理和许可。不再需要
也无法部署和使用外部 Platform Services Controller。所有 Platform Services Controller 服务都已整合
到 vCenter Server 中，并且简化了部署和管理。
由于这些服务现在是 vCenter Server 的一部分，因此不再将其描述为 Platform Services Controller 的一
部分。在 vSphere 7.0 中，《vSphere 身份验证》出版物替换了 《Platform Services Controller 管理》
出版物。新出版物包含有关身份验证和证书管理的完整信息。有关使用 vCenter Server Appliance 从使用
现有外部 Platform Services Controller 的 vSphere 6.5 和 6.7 部署升级或迁移到 vSphere 7.0 的信息，
请参见 《vSphere 升级》文档。
vCenter Server 配置
VMware, Inc.
8
[第9页]
使用 vCenter Server 管理界面配置
vCenter Server
2
部署 vCenter Server 后，可以登录到 vCenter Server 管理界面并编辑设置。
有关修补 vCenter Server 和自动检查 vCenter Server 修补程序的信息，请参见《vSphere 升级》文档。
有关备份和还原 vCenter Server 的信息，请参见《vCenter Server 安装和设置》。 本章讨论了以下主题： n
登录 vCenter Server 管理界面
n
查看 vCenter Server 运行状况
n
重新引导或关闭 vCenter Server
n
创建支持包
n
监控 CPU 和内存使用情况
n
监控磁盘使用情况
n
监控网络使用情况
n
监控数据库使用情况
n
启用或禁用 SSH 访问和 Bash Shell 访问
n
配置 DNS、IP 地址和代理设置
n
重新配置主网络标识符
n
编辑防火墙设置
n
配置系统时区和时间同步设置
n
启动、停止和重新启动服务
n
配置更新设置
n
更改 root 用户的密码和密码过期设置
n
将 vCenter Server 日志文件转发到 远程 Syslog 服务器 n 配置和调度备份 VMware, Inc. 9 [第10页]
登录 vCenter Server 管理界面
登录 vCenter Server 管理界面可访问 vCenter Server 配置设置。
注 如果 vCenter Server 管理界面闲置时间达到 10 分钟，登录会话将过期。 前提条件
确认 vCenter Server 已成功部署和运行。
步骤
1
在 Web 浏览器中，转至 vCenter Server 管理界面，https://appliance-IP-address-or- FQDN:5480。 2 以 root 用户身份登录。
默认 root 密码是您在部署 vCenter Server 时设置的密码。
查看 vCenter Server 运行状况
可以使用 vCenter Server 管理界面查看 vCenter Server 的整体运行状况和运行状况消息。
vCenter Server 的整体运行状况基于硬件组件（如 CPU、内存、数据库和存储）的状态。它还基于更新组
件，这会根据最后一次对可用修补程序的检查来显示软件包是否为最新软件包。
重要说明 如果不执行可用修补程序定期检查，更新组件的健康状况可能已过时。有关如何检查 vCenter
Server 修补程序和启用 vCenter Server 修补程序自动检查的信息，请参见《vSphere 升级》。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击摘要。
2
在“健康状况”窗格中，查看“整体运行状况”标志。
表 2-1. 运行状况
标志图标
描述
正常。所有组件都运行正常。
警告。一个或多个组件可能即将过载。
请在“运行状况消息”窗格中查看详细信息。
警示一个或多个组件可能已降级。可能没有可用
的安全修补程序。
请在“运行状况消息”窗格中查看详细信息。
vCenter Server 配置
VMware, Inc.
10
[第11页]
表 2-1. 运行状况 （续）
标志图标
描述
严重。一个或多个组件可能处于不可用状态，
vCenter Server 可能很快无响应。可能存在可
用的安全修补程序。
请在“运行状况消息”窗格中查看详细信息。
未知。没有可用的数据。
重新引导或关闭 vCenter Server
可以使用 vCenter Server 管理界面重新启动或关闭正在运行的虚拟机。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击摘要。
2
从顶部菜单窗格中，单击操作下拉菜单。
3
单击重新引导或关闭以重新启动或关闭虚拟机。
4
在确认对话框中，单击是确认操作。
创建支持包
可以创建包含设备中运行的vCenter Server 实例的日志文件的支持包。可以在您的计算机上本地分析这些
日志，也可以将此包发送给 VMware 支持部门。
前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击摘要。
2
从顶部菜单窗格中，单击操作下拉菜单。
3
单击创建支持包，并将其保存到本地计算机。
结果
支持包将以 .tgz 文件的形式下载到您的本地计算机。
vCenter Server 配置
VMware, Inc.
11
[第12页]
监控 CPU 和内存使用情况
可以使用 vCenter Server 管理界面监控 vCenter Server 的 CPU 和内存总体使用情况。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击监控。
2
在“监控”页面中，单击 CPU 和内存选项卡。
3
从日期范围下拉菜单中，选择要为其生成 CPU 使用率趋势图和内存使用率趋势图的时间段。 4
指向图表可查看特定日期和时间的 CPU 和内存使用情况。
监控磁盘使用情况
可以使用 vCenter Server 管理界面监控 vCenter Server 的磁盘使用情况。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击监控。
2
在“监控”页面中，单击磁盘选项卡。
结果
“监控磁盘”窗格会显示一个磁盘，可按名称、分区或使用率对其进行排序。 监控网络使用情况
可以使用 vCenter Server 管理界面监控前一天、上周、上个月或上个季度的 vCenter Server 网络使用情 况。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击监控。
2
在“监控”页面中，单击网络选项卡。
3
在日期范围下拉菜单中，选择要生成网络利用率图的时段。
vCenter Server 配置
VMware, Inc.
12
[第13页]
4
在网格图下方的表中，选择要监控的数据包或字节传输速率。
选项因网络设置而异。
网络利用率图会刷新，以显示所选项目的使用情况。
5
指向网络利用率图可查看特定日期和时间的网络使用情况数据。
监控数据库使用情况
您可以使用 vCenter Server 管理界面按数据类型监控 vCenter Server 嵌入式数据库的使用情况。您还可
以监控空间使用趋势图，并筛选任意一个最大的数据类型。
前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击监控。
2
在“监控”页面中，单击数据库选项卡可监控 vCenter Server 数据库的已消耗和可用空间。 3
在日期范围下拉菜单中，选择要为其生成空间使用率趋势图的时段。
4
在图表底部，单击特定数据库组件的名称以在图表中包含或排除该组件。 选项 描述 SEAT 空间使用率趋势图
允许选择并查看警报、事件、任务和统计信息的趋势线。
整体空间使用率趋势图
允许选择并查看 SEAT、数据库日志和核心趋势线。
5
指向空间利用率图可查看特定日期和时间的数据库使用值。
启用或禁用 SSH 访问和 Bash Shell 访问
可以使用 vCenter Server 管理界面编辑设备的访问设置。
可以启用或禁用 SSH 管理员登录设备。还可以启用在特定时间间隔内对 vCenter Server Bash shell 进行 访问。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击访问，然后单击编辑。
vCenter Server 配置
VMware, Inc.
13
[第14页]
2
编辑 vCenter Server 的访问设置。
选项
描述
启用 SSH 登录
启用对 vCenter Server 的 SSH 访问。
启用 DCUI
启用对 vCenter Server 的 DCUI 访问。
启用控制台 CLI
启用对 vCenter Server 的控制台 CLI 访问。 启用 Bash Shell
启用对 vCenter Server 的 Bash shell 访问，持续时间为您输入的分钟数。 3 单击确定以保存设置。
配置 DNS、IP 地址和代理设置
可以为 vCenter Server 设置静态/DHCP 的 IPv4/IPv6 地址的组合，编辑 DNS 设置，以及定义代理设 置。 前提条件 n
要更改设备的 IP 地址，请验证设备的系统名称是否为 FQDN。系统名称用作主网络标识符。如果在部
署设备期间将 IP 地址设置为系统名称，您可在稍后将 PNID 更改为 FQDN。
注 只能将 IPv4 IP 地址设置为系统名称。必须先启用 IPv4 IP 地址，才能进行此设置。 n
要还原双堆栈 VC，第 1 阶段部署后的基础 VC 应配置为： n
如果备份的 VC 的 PNID 解析为 IPv4 且 IPv4 配置为静态，则第 1 阶段部署后的基础 VC 应配置 静态或 DHCP IPv4。 n
如果备份的 VC 的 PNID 解析为 IPv4 且 IPv4 配置为 DHCP，则第 1 阶段部署后的基础 VC 应配 置 DHCP IPv4。 n
如果备份的 VC 的 PNID 解析为 IPv6 且 IPv6 配置为静态，则第 1 阶段部署后的基础 VC 应配置 静态或 DHCP IPv6。 n
如果备份的 VC 的 PNID 解析为 IPv6 且 IPv6 配置为 DHCP，则第 1 阶段部署后的基础 VC 应配 置 DHCP IPv6。 n
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击网络。
2
从“网络设置”页面中，单击编辑。
vCenter Server 配置
VMware, Inc.
14
[第15页]
3
展开“主机名和 DNS”部分以配置 DNS 设置。
注 主机名的有效值是解析为已启用 IP 地址或 IPv4 IP 地址的 FQDN。 选项 描述 自动获取 DNS 设置
自动从网络获取 DNS 设置。
手动输入 DNS 设置
手动设置 DNS 地址设置。如果选择此选项，必须提供下列信息： n
首选 DNS 服务器的 IP 地址。
n
（可选） 备用 DNS 服务器的 IP 地址。
4
从“网络设置”页面中，单击编辑。
5
展开“网卡 0”部分以配置网关设置。
注 PNID 和网络 API 仅支持将网卡 0 作为主网卡。 6 编辑 IPv4 地址设置。 选项 描述 启用或禁用 IPv4 设置
根据切换开关选项启用或禁用 IPv4 地址。
自动获取 IPv4 设置
自动从网络获取设备的 IPv4 地址。
手动输入 IPv4 设置
使用手动设置的 IPv4 地址。必须输入 IP 地址、子网前缀长度以及默认网关。
注 对于静态 IPv4 或 IPv6 地址，必须手动设置 DNS 服务器。
注 IPv4 和 IPv6 IP 地址发生更改时，第二方和第三方解决方案需要重新注册。 7 编辑 IPv6 地址设置。 选项 描述 启用或禁用 IPv6 设置
根据切换开关选项启用或禁用 IPv6 地址。
通过 DHCP 自动获取 IPv6 设置
使用 DHCP 自动将网络的 IPv6 地址分配给设备。
通过路由器播发自动获取 IPv6 设置
使用路由器播发自动将网络的 IPv6 地址分配给设备。
使用静态 IPv6 地址
使用手动设置的静态 IPv6 地址。
1
单击此复选框。
2
输入 IPv6 地址和子网前缀长度。
3
单击添加输入其他 IPv6 地址。
4
单击保存。
注 对于静态 IPv4 或 IPv6 地址，必须手动设置 DNS 服务器。
可以将设备配置为通过 DHCP 和路由器播发自动获取 IPv6 设置。可以同时分配静态 IPv6 地址。
注 IPv4 和 IPv6 IP 地址发生更改时，第二方和第三方解决方案需要重新注册。 8
要配置代理服务器，请在“代理设置”部分中单击编辑。
vCenter Server 配置
VMware, Inc.
15
[第16页]
9
选择要启用的代理设置
选项
描述
HTTPS
启用此选项可配置 HTTPS 代理设置。
FTP
启用此选项可配置 FTP 代理设置。
注 确保在代理服务器上启用了 ICMP。
HTTP
启用此选项可配置 HTTP 代理设置。
10 输入服务器主机名或 IP 地址。
11
输入端口。
12 输入用户名（可选）。
13 输入密码（可选）。
14 单击保存。
重新配置主网络标识符
可以更改 vCenter Server 的管理网络的 FQDN、IP 或 PNID。 前提条件
系统名称用作主网络标识符。如果在部署设备期间将 IP 地址设置为系统名称，您可在稍后将 PNID 更改为 FQDN。
如果启用了 vCenter High Availability (HA)，则必须在重新配置 PNID 之前禁用 vCenter HA 设置。 步骤 1
使用管理员 SSO 凭据登录到 vCenter Server 管理界面。 2
在 vCenter Server 管理界面中，导航到网络页面，然后单击编辑。 3
选择要修改的网卡，然后单击下一步。
4
在编辑设置窗格中，更改主机名并提供新的 IP 地址。单击下一步。 5
在 SSO 凭据窗格中，提供管理员 SSO 凭据。您必须使用 administrator@<domain_name> 凭 据。 6
在即将完成窗格中，检查新设置并选中备份确认框。单击完成。
任务栏显示网络更新的状态。要取消更新，请单击取消网络更新。网络重新配置完成后，UI 会重定向 到新的 IP 地址。 7
要完成重新配置过程并重新启动服务，请使用管理员 SSO 凭据登录。 8
在网络页面上，验证新的主机名和 IP 地址。
vCenter Server 配置
VMware, Inc.
16
[第17页]
后续步骤
n
重新注册所有已部署的插件。
n
重新生成所有自定义证书。
n
如果已启用 vCenter HA，请重新配置 vCenter HA。 n
如果已启用活动域，请重新配置活动域。
n
如果已启用混合链接模式，请使用云 vCenter Server 重新配置混合链接。 编辑防火墙设置
部署 vCenter Server 后，可以使用管理界面编辑其防火墙设置和创建防火墙规则。
可以设置防火墙规则以接受或阻止vCenter Server 与特定服务器、主机或虚拟机之间的流量。您无法阻止
特定端口，但可以阻止所有流量。
前提条件
确认登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 中
SystemConfiguration.Administrators 组的成员。 步骤 1
在 vCenter Server 管理界面中，单击防火墙。
2
编辑防火墙设置。
命令
操作
添加
a
要创建防火墙规则，请单击添加。
b
选择虚拟机的网络接口。
c
输入要将此规则应用到的网络的 IP 地址。
IP 地址可以是 IPv4 和 IPv6 地址。
d
输入子网前缀长度。
e
从操作下拉菜单中，选择是接受、忽略、拒绝还是返回 vCenter Server 与所输 入网络之间的连接。 f 单击保存。 编辑 a 选择规则，然后单击编辑。 b 编辑规则的设置。 c 单击保存。 删除 a 选择规则，然后单击删除。 b 根据提示，再次单击删除。 重新排序 a 选择规则，然后单击重新排序。 b
在“重新排序”窗格中，选择要移动的规则。
c
单击上移或下移。
d
单击保存。
vCenter Server 配置
VMware, Inc.
17
[第18页]
配置系统时区和时间同步设置
部署 vCenter Server 后，可以从 vCenter Server 管理界面更改系统时区和时间同步设置。
部署 vCenter Server 时，可以使用运行 vCenter Server 的 ESXi 主机的时间设置，也可以基于 NTP 服务
器配置时间同步。如果 vSphere 网络中的时间设置发生更改，可以编辑设备中的时区和时间同步设置。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击时间。
2
配置系统时区设置。
a
在“时区”窗格中，单击编辑。
b
从时区下拉菜单中，选择一个位置或时区，然后单击保存。
3
配置时间同步设置。
a
在“时间同步”窗格中，单击编辑。
b
从模式下拉菜单中，配置时间同步方法。
选项
描述
已禁用
不进行时间同步。使用系统时区设置。
主机
启用 VMware Tools 时间同步。使用 VMware Tools 同步设备与 ESXi 主机的 时间。 NTP
启用 NTP 同步。必须输入一个或多个 NTP 服务器的 IP 地址或 FQDN。 c 单击保存。 启动、停止和重新启动服务
可以使用 vCenter Server 管理界面查看 vCenter Server 组件的状态以及启动、停止和重新启动服务。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击服务。
“服务”页面会显示一个可以按名称、启动类型、运行状况和状态进行排序的已安装服务的表。 2
选择服务，然后单击设置启动类型，为服务配置手动启动或自动启动。 3
选择服务，然后单击启动以启动服务。
vCenter Server 配置
VMware, Inc.
18
[第19页]
4
选择服务，并单击停止以停止服务，或单击重新启动以重新启动服务，然后单击确定。
警告 停止或重新启动某些服务可能会导致功能暂时不可用。
配置更新设置
可以使用 vCenter Server 管理界面来配置更新设置以及检查新更新。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击更新。
2
要配置更新设置，请单击设置。
a
要自动检查更新，请选中复选框。
b
选择要使用默认存储库还是自定义存储库。
c
如果选择了自定义存储库，请输入存储库 URL、用户名（可选）和密码（可选）。单击保存。
对于 URL，支持 HTTPS 和 FTPS 协议。
3
要手动检查更新，请单击检查更新下拉菜单。
a
选择要从 CD-ROM 还是 CD-ROM + URL 检查更新。 结果
“可用更新”表显示了可用的更新，您可以按版本、类型、发布日期、重新引导要求和严重性对这些更新 进行排序。
更改 root 用户的密码和密码过期设置
部署 vCenter Server 时，需要设置 root 用户的初始密码，默认情况下，该密码在 90 天后过期。可以从
vCenter Server 管理界面更改 root 密码和密码过期设置。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击管理。
2
在“密码”部分中，单击更改。
3
输入当前密码和新密码，然后单击保存。
vCenter Server 配置
VMware, Inc.
19
[第20页]
4
为 root 用户配置密码过期设置。
a
在“密码过期设置”部分中，单击编辑，然后选择密码过期策略。
选项
描述
是
root 用户的密码在指定天数后过期。您必须提供下列信息：
n
root 密码有效期 (天)
经过此天数后，密码过期。
n
过期警告电子邮件
vCenter Server 在过期日期之前向其发送警告消息的电子邮件地址。 否
root 用户的密码永不过期。
b
在“密码过期设置”窗格中，单击保存以应用新的密码过期设置。
“密码过期设置”部分会显示新的过期日期。
将 vCenter Server 日志文件转发到 远程 Syslog 服务器
您可以将 vCenter Server 日志文件转发到 远程 Syslog 服务器进行日志分析。
注 ESXi 可以配置为将日志文件发送到 vCenter Server，而不是将其存储到本地磁盘。建议最多从 30 个
支持的主机中收集日志。有关如何配置 ESXi 日志转发的信息，请参见 http://kb.vmware.com/s/article/
2003322。此功能适用于具有无状态 ESXi 主机的较小的环境。对于所有其他情况，请使用专用的日志服
务器。使用 vCenter Server 接收 ESXi 日志文件可能会影响 vCenter Server 性能。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，选择 Syslog。 2
如果尚未配置任何远程 syslog 主机，请在“转发配置”部分中，单击配置。如果已配置主机，请单击 编辑。 3
在“创建转发配置”窗格中，输入目标主机的服务器地址。受支持的目标主机的最大数量为三个。 4
在协议下拉菜单中，选择要使用的协议。
菜单项
描述
TLS
传输层安全
TCP
传输控制协议
RELP
可靠事件日志记录协议
UDP
用户数据报协议
5
在端口文本框中，输入与目标主机进行通信要使用的端口号。
vCenter Server 配置
VMware, Inc.
20
[第21页]
6
在“创建转发配置”窗格中，单击添加以输入其他的远程 syslog 服务器。 7 单击保存。 8
确认远程 syslog 服务器正在接收消息。
9
在“转发配置”部分中，单击发送测试消息。
10 确认远程 syslog 服务器已收到测试消息。
新配置设置会显示在“转发配置”部分中。
配置和调度备份
可以使用 vCenter Server 管理界面来设置备份位置，创建备份调度以及监控备份活动。 前提条件
以 root 用户身份登录 vCenter Server 管理界面。 步骤 1
在 vCenter Server 管理界面中，单击备份。
2
要创建备份调度，请单击配置。要编辑现有备份调度，请单击编辑。
a
在备份调度窗格中，使用
protocol://server-address<:port-number>/folder/subfolder 格式输入备份位置。
支持备份的协议为 FTPS、HTTPS、SFTP、FTP、NFS、SMB 和 HTTP。 b
输入备份服务器的用户名和密码。
c
输入进行备份的时间和频率。
d
（可选）输入备份的加密密码。
e
表示要保留的备份数量。
f
表示要备份的数据类型。
3
要启动手动备份，请单击立即备份。
结果
调度备份和手动备份的信息将显示在活动表中。
vCenter Server 配置
VMware, Inc.
21
[第22页]
使用 vSphere Client 配置 vCenter
Server
3
可以从 vSphere Client 执行一些配置操作，例如将设备加入 Active Directory 域、网络连接和其他设置。 本章讨论了以下主题： n
配置 vCenter Server
n
加入或退出 Active Directory 域
n
将用户添加到 SystemConfiguration.BashShellAdministrators 组中 n 重新引导节点 n 查看 节点的运行状况 n 导出支持包
配置 vCenter Server
可以从 vSphere Client 和 vCenter Server 管理界面配置 vCenter Server。 您可执行的操作取决于部署。
内部部署 vCenter Server
您可以更改多个 vCenter Server 设置，其中包括许可、统计信息收集和日志记录等。
VMware Cloud on AWS 中的 vCenter Server
创建 SDDC 时，VMware 将预配置vCenter Server 实例。您可以查看配置设置和高级设置，也可以 设置“今日消息”。
有关如何配置 vCenter Server 的详细信息，请参见《vCenter Server 配置》指南。
配置 vCenter Server 的许可证设置
评估期到期后或当前分配的许可证到期后，必须为 vCenter Server 系统分配许可证。如果在 Customer
Connect 中升级、合并或拆分 vCenter Server 许可证，您必须将新许可证分配给 vCenter Server 系统并 移除旧许可证。 前提条件 n
要在 vSphere 环境中查看和管理许可证，必须在运行 vSphere Client 的 vCenter Server 系统上具有 全局.许可证特权。 VMware, Inc. 22 [第23页] 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择许可。 4 单击分配许可证。 5
在分配许可证对话框中，选择要执行的任务。
u
在 vSphere Client 中，选择一个现有许可证，或选择新创建的许可证。 任务 步骤 选择现有许可证
从列表中选择现有许可证，然后单击确定。
选择新创建的许可证
a
单击新建许可证选项卡。
b
在分配许可证对话框中，键入或复制并粘贴许可证密钥，然后单击确定。 c
输入新许可证的名称，然后单击确定。
页面上将显示有关产品、产品功能、容量和有效期的详细信息。
d
单击确定。
e
在分配许可证对话框中，选择新创建的许可证，然后单击确定。
结果
将把许可证分配给 vCenter Server 系统，并为 vCenter Server 系统分配许可证容量的一个实例。 配置统计信息设置
要设置统计数据的记录方式，请配置统计信息的收集时间间隔。可以通过命令行监控实用程序或通过在
vSphere Client 中查看性能图表来访问存储的统计信息。
在 vSphere Client 中配置统计信息收集间隔
统计信息收集间隔可决定统计信息查询的发生频率、统计数据在数据库中的存储时间长度，以及所收集的
统计数据类型。您可以通过 vSphere Client 中的性能图表或通过命令行监控实用程序查看收集的统计信 息。
注 并非所有时间间隔属性都可以配置。
前提条件
所需特权：性能.修改时间间隔
步骤
1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。
vCenter Server 配置
VMware, Inc.
23
[第24页]
5
要启用或禁用统计间隔，请选中该间隔对应的框。
6
要更改统计间隔属性值，请从下拉菜单中选择一个值。
a
在间隔时间中，选择收集统计数据所采用的时间间隔。
b
在保存时间中，选择存档的统计信息保留在数据库中的时间。
c
在统计级别中，选择用于收集统计信息的新级别。
级别越低，使用的统计信息计数器就越少。级别 4 会使用所有统计信息计数器。该级别仅用于调试 目的。
统计级别不得高于为前一统计间隔设置的统计级别。该要求是 vCenter Server 的依赖项。 7
（可选） 在“数据库大小”中，估算统计信息设置对数据库的影响。 a 输入物理主机的数量。 b 输入虚拟机的数量。
此时将计算并显示估算的所需空间以及所需的数据库行数。
c
如果需要，请更改统计信息收集设置。
8
单击保存。
示例： 统计间隔的默认设置之间的关系
n
每隔 5 分钟收集一次的采样会存储 1 天。
n
每隔 30 分钟收集一次的采样会存储 1 周。
n
每隔 2 小时收集一次的采样会存储 1 个月。
n
每天收集一次的采样会存储 1 年。
对于所有统计间隔，默认级别为 1。该级别使用集群服务、CPU、磁盘、内存、网络、系统和虚拟机操作计 数器。
vCenter Server 配置
VMware, Inc.
24
[第25页]
数据集合级别
每个收集时间间隔都有一个默认的集合级别，用以确定收集的数据量以及可用于在图表中显示的计数器。 集合级别也称为统计级别。 表 3-1. 统计级别 级别 衡量指标 最佳做法 1 级 n
集群服务 (VMware Distributed Resource Scheduler) – 所有指 标 n
CPU – cpuentitlement, totalmhz, usage（平均值）, usagemhz n
磁盘 – capacity, maxTotalLatency, provisioned, unshared,
usage（平均值）, used
n
内存 – consumed, mementitlement, overhead, swapinRate,
swapoutRate, swapused, totalmb, usage（平均值）, vmmemctl（虚拟增长） n
网络 – usage（平均值）, IPv6
n
系统 – heartbeat, uptime
n
虚拟机操作 – numChangeDS, numChangeHost,
numChangeHostDS
在不需要设备统计信息时用于长期性能
监控。
级别 1 是所有收集时间间隔的默认集合级
别。
2 级
n
级别 1 衡量指标
n
CPU – idle, reservedCapacity
n
磁盘 – 所有指标，不包括 numberRead 和 numberWrite。 n
内存 – 所有指标，不包括 memUsed 以及最大和最小汇总值。 n 虚拟机操作 – 所有衡量指标
在不需要设备统计信息但希望监控基本
统计信息以外的信息时，用于长期性能
监控。
3 级
n
级别 1 和级别 2 衡量指标
n
所有计数器的衡量指标，但不包括最小和最大累计值。
n
设备衡量指标
在遇到问题后或需要设备统计信息时，
用于短期性能监控。
4 级
vCenter Server 支持的所有衡量指标，包括最小和最大累计值。
在遇到问题后或需要设备统计信息时，
用于短期性能监控。
注 当使用的统计级别（级别 3 或级别 4）超出默认值时，如果不能尽快将统计信息保存到数据库，则可能
会导致一个特定进程 (vpxd) 占用的内存增长。如果没有严密监控这些统计级别的使用限制，则可能会导致
vpxd 耗尽内存并最终崩溃。
因此，如果管理员决定提升其中任何一个级别，则管理员必须监控 vpxd 进程的大小，以确保它在更改后 不会无限增大。
为 vCenter Server 配置运行时设置
可以更改 vCenter Server ID、受管地址以及名称。如果在同一环境中运行多个 vCenter Server 系统，可 能需要进行更改。 前提条件 所需特权：全局.设置
vCenter Server 配置
VMware, Inc.
25
[第26页]
步骤
1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5
在“编辑 vCenter Server 设置”对话框中，选择运行时设置。 6
在 vCenter Server 的唯一 ID 中，输入唯一 ID。
可以将此值更改为一个介于 0 到 63 之间的数字，以标识在公用环境中运行的每个 vCenter Server 系
统。默认情况下，ID 值是随机生成的。
7
在 vCenter Server 受管地址中，输入 vCenter Server 系统地址。
地址可以为 IPv4、IPv6、完全限定域名、IP 地址或其他地址格式。 8
在 vCenter Server 名称中，输入 vCenter Server 系统的名称。
如果要更改 vCenter Server 的 DNS 名称，可以使用此文本框修改要匹配的 vCenter Server 名称。 9 单击保存。 后续步骤
如果对 vCenter Server 系统的唯一 ID 进行了更改，则必须重新启动 vCenter Server 系统，才能使这些 更改生效。 配置用户目录设置
可以配置 vCenter Server 与被配置为标识源的用户目录服务器进行交互的某些方式。
对于早于 vCenter Server 5.0 的 vCenter Server 版本，这些设置适用于与 vCenter Server 关联的
Active Directory。对于 vCenter Server 5.0 及更高版本，这些设置适用于 vCenter Single Sign-On 标 识源。 前提条件 所需特权：全局.设置 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5
在“编辑 vCenter 常规设置”窗口中，选择用户目录。
6
在用户目录超时中，键入连接目录服务器的超时时间间隔（以秒为单位）。
vCenter Server 配置
VMware, Inc.
26
[第27页]
7
启用查询限制框以设置查询限制大小。
8
在查询限制大小中，输入 vCenter Server 系统的子清单对象中可以关联权限的用户数和组数。
注 针对 vSphere 清单对象，在管理 > 权限中单击添加权限时会显示“添加权限”对话框，通过该对 话框可将权限与用户和组关联。 9 单击保存。 配置邮件发件人设置
必须配置发件人帐户的电子邮件地址，才能使用 vCenter Server 操作，如将电子邮件通知作为警报操作发
送。您可以使用匿名或身份验证模式发送电子邮件警示和警报。
前提条件
所需特权：全局.设置
SMTP 身份验证适用于：
n
仅 vSphere 7.0 Update 1 及更高版本。
n
仅限 Office 365 邮箱用户。
n
SMTP 邮件发件人应满足 SMTP 身份验证的基本要求，如 Microsoft 文档 SMTP AUTH 客户端提交要 求中所述。 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5
选择邮件，然后输入 vCenter Server 用于发送电子邮件警示的设置。 6
在邮件服务器文本框中，输入 SMTP 服务器信息。
“SMTP 服务器”是用于发送电子邮件的 SMTP 网关的 DNS 名称或 IP 地址。 n
要匿名发送邮件，可以输入任何 SMTP 服务器信息作为邮件服务器名称。 n
要使用 SMTP 身份验证，必须输入 smtp.office365.com 作为邮件服务器名称，除非您具有某些
自定义配置。不要使用 IP 地址作为邮件服务器，因为 SMTP 身份验证不支持 IP 地址。 7
在邮件发件人文本框中，输入发件人帐户信息。
“发件人帐户”是发件人的电子邮件地址。
要使用 SMTP 身份验证，必须在邮件发件人文本框中输入有效的 SMTP 帐户名称。
注 您必须输入完整的电子邮件地址，包括域名。
例如，mail_server@example.com
vCenter Server 配置
VMware, Inc.
27
[第28页]
8
单击保存。
9
此步骤仅适用于 SMTP 身份验证。
必须按以下方式配置 SMTP 用户设置：
a
选择配置选项卡。
b
选择高级设置。
c
单击编辑设置，然后输入以下配置参数值：
名称
值
mail.smtp.username
有效的 SMTP 帐户名称。
注 此帐户名称必须与步骤 7 中通过使用 SMTP 身份验证发
送邮件时在邮件发件人文本框中提供的帐户名称相同。
mail.smtp.password
有效的 SMTP 帐户密码。
注 目前，帐户密码未屏蔽且可见。在即将发布的版本中提
供屏蔽功能之前，必须使用专用的 SMTP 邮件用户。
mail.smtp.port
587
d
单击保存。
后续步骤
可以执行以下步骤以测试邮件设置：
1
创建由用户操作触发的警报。
例如，用户操作可以是关闭虚拟机电源。
2
验证在触发警报时是否收到邮件。
配置 SNMP 设置
最多可以配置四个接收方从 vCenter Server 接收 SNMP 陷阱。对于每个收件人，请指定主机名称、端口 和社区。 前提条件 所需特权：全局.设置 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5 选择 SNMP 接收方。
vCenter Server 配置
VMware, Inc.
28
[第29页]
6
选中启用接收方 1 框。
7
在主要接收方 URL 中，输入 SNMP 接收方的主机名或 IP 地址。 8
在接收方端口中，输入接收方的端口号。
端口号必须是介于 1 和 65535 之间的一个值。
9
在社区字符串中，输入社区标识符。
10 要向多个接收方发送警报，请选中其他启用接收方框，然后输入这些接收方的主机名、端口号和社区标 识符。 11 单击保存。 查看端口设置
可以查看由 Web 服务使用的端口，以与其他应用程序进行通信。不能配置这些端口设置。
Web 服务将随 VMware vCenter Server 一起安装。Web 服务是使用 VMware SDK 应用程序编程接口
(API) 的第三方应用程序的必备组件。有关安装 Web 服务的信息，请参见《vCenter Server 安装和设 置》文档。 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5 选择端口。
此时将显示 Web 服务使用的端口。
6
单击保存。
配置超时设置
可以配置 vCenter Server 操作的超时时间间隔。这些时间间隔指定的时间量表示在此段时间之后
vSphere Client 将超时。
前提条件
所需特权：全局.设置
步骤
1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。
vCenter Server 配置
VMware, Inc.
29
[第30页]
5
选择超时设置。
6
在正常中，键入正常操作的超时时间间隔（以秒为单位）。
请勿将该值设置为零 (0)。
7
在长时间中，输入长时间操作的超时时间间隔（以分钟为单位）。
请勿将该值设置为零 (0)。
8
单击保存。
9
重新启动 vCenter Server 系统以便更改生效。
配置日志记录选项
可以对 vCenter Server 在日志文件中收集的详细信息的数量进行配置。 前提条件 所需特权：全局.设置 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5 选择日志记录设置。 6 选择日志记录选项。 选项 描述 无 关闭日志记录 错误 仅显示错误日志条目 警告 显示警告和错误日志条目 信息 显示信息、错误和警告日志条目 详细
显示信息、错误、警告和详细日志条目
琐事
显示信息、错误、警告、详细和琐事日志条目
7
单击保存。
结果
对日志记录设置的更改将立即生效。无需重新启动 vCenter Server 系统。
vCenter Server 配置
VMware, Inc.
30
[第31页]
配置数据库设置
可以配置允许同时出现的最大数据库连接数。为了限制 vCenter Server 数据库的增长并节省存储空间，可
以将数据库配置为定期放弃有关任务或事件的信息。
注 如果要保留 vCenter Server 的任务和事件的完整历史记录，请不要使用数据库保留选项。 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5
在“编辑 vCenter 常规设置”窗口中，单击数据库。
6
在最大连接数字段中，输入所需连接数。
注 除非系统中存在这些问题之一，否则请勿更改该值。
n
如果 vCenter Server 系统频繁执行大量操作且性能至关重要，请增加连接数。 n
如果数据库已共享且到数据库的连接需要较大开销，请减少连接数。
7
启用 vCenter Server 的任务清理选项，以定期删除保留的任务。 8
（可选） 在任务保留 (天数) 字段中，输入值（以天为单位）。
在指定的天数后将放弃有关在此 vCenter Server 系统上执行的任务的信息。 9
启用 vCenter Server 的事件清理选项，以定期清理保留的事件。
10 （可选） 在事件保留 (天数) 字段中，输入值（以天为单位）。
在指定的天数后将放弃有关此 vCenter Server 系统的事件的信息。
注 在 vCenter Server 管理界面中监控 vCenter Server 数据库消耗和磁盘分区。
警告 将事件保留期延长至 30 天以上将导致 vCenter 数据库大小显著增加，并可能会关闭 vCenter
Server。确保相应地增加 vCenter 数据库。
11
重新启动 vCenter Server 以手动应用更改。
12 单击保存。
验证旧版主机的 SSL 证书
可以配置 vCenter Server 以检查其连接到的主机的 SSL 证书。如果配置此设置，则在连接到主机执行某
些操作（如添加主机或建立到虚拟机的远程控制台连接）之前，vCenter Server 和 vSphere Client 会先
检查该主机是否具有有效的 SSL 证书。
vCenter Server 配置
VMware, Inc.
31
[第32页]
vCenter Server 5.1 和 vCenter Server 5.5 始终使用 SSL 指纹证书连接到 ESXi 主机。从 vCenter
Server 6.0 开始，默认情况下，SSL 证书将由 VMware Certificate Authority 签名。您可以改用第三方
CA 的证书。只有旧版主机才支持指纹模式。
步骤
1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 在设置下，选择常规。 4 单击编辑。 5 选择 SSL 设置。 6
对于需要验证的每个主机，请确定其指纹。
a
登录到直接控制台。
b
在系统自定义菜单上，选择查看支持信息。
指纹显示在右侧的列中。
7
将从主机获取的指纹与 vCenter Server“SSL 设置”对话框中列出的指纹进行对比。 8
如果指纹匹配，请选中与该主机对应的复选框。
单击保存之后，未选中的主机将断开连接。
9
单击保存。
配置高级设置
在高级设置中，可以修改 vCenter Server 配置文件 vpxd.cfg。
可以使用高级设置将条目添加到 vpxd.cfg 文件中，但不可编辑或删除条目。VMware 建议您仅在
VMware 技术支持人员的指导下或遵循 VMware 文档中的特定指示来更改这些设置。 前提条件 所需特权：全局.设置 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 选择配置选项卡。 3 选择高级设置。 4 单击编辑设置。 5
在名称字段中，键入设置的名称。名称必须以“config”开头。例如：config.log。 6
在值字段中，键入指定设置的值。
7
单击添加。
vCenter Server 配置
VMware, Inc.
32
[第33页]
8
单击保存。
结果
在 vpxd.cfg 文件中，新添加的高级设置会将 config. 附加到设置键中。例如：
config.example.setting = exampleValue 后续步骤
许多高级设置更改都要求重新启动 vCenter Server 系统。请咨询 VMware 技术支持，以确定所作更改是
否需要重新启动 vCenter Server。
向其他已登录用户发送消息
管理员可以向当前登录到 vCenter Server 系统的用户发送消息。消息可能是通知要进行维护或要求用户暂 时注销。 步骤 1
在 vSphere Client 中，导航到 vCenter Server 实例。 2 单击配置。 3
选中设置 > 今日消息，然后单击编辑。
4
输入消息，然后单击确定。
结果
在每个活动用户会话中，消息将显示在 vSphere Client 顶部。
加入或退出 Active Directory 域
可以将 vCenter Server 加入到 Active Directory 域。您可以将此 Active Directory 域中的用户和组附加
到 vCenter Single Sign-On 域。您可以退出 Active Directory 域。
重要说明 不支持将 vCenter Server 加入到具有只读域控制器 (RODC) 的 Active Directory 域。只能将
vCenter Server 加入到具有可写入域控制器的 Active Directory 域。
如果想要配置权限，以便 Active Directory 的用户和组可以访问 vCenter Server 组件，您必须将
vCenter Server 实例加入到 Active Directory 域。
例如，要允许 Active Directory 用户使用 vSphere Client 登录到 vCenter Server 实例，则必须将
vCenter Server 实例加入到 Active Directory 域，然后为该用户分配管理员角色。 前提条件 n
确认登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 中
SystemConfiguration.Administrators 组的成员。
vCenter Server 配置
VMware, Inc.
33
[第34页]
n
确认设备的系统名称为 FQDN。如果在设备部署期间将 IP 地址设置为系统名称，则无法将 vCenter
Server 加入到 Active Directory 域。
步骤
1
使用 vSphere Client 以 administrator@your_domain_name 身份登录到 vCenter Server 实例。 2
在 vSphere Client 菜单中，选择系统管理。
3
选择 Single Sign On > 配置。
4
单击身份提供程序选项卡，然后选择 Active Directory 域作为标识提供类型。 5 单击加入 AD。 6
在“加入 Active Directory 域”窗口中，提供以下详细信息。 选项 描述 域
Active Directory 域名，例如 mydomain.com。请勿在此文本框中提供 IP 地址。 组织单位 (可选)
完整的组织单位 (OU) LDAP FQDN，例如，
OU=Engineering,DC=mydomain,DC=com。
重要说明 仅当您熟悉 LDAP 时才使用此文本框。
用户名
用户主体名称 (UPN) 格式的用户名，例如 jchin@mydomain.com。
重要说明 不支持向下登录名格式，例如 DOMAIN\UserName。 密码 用户的密码。
注 重新引导节点以应用更改。
7
单击加入，将 vCenter Server 加入到 Active Directory 域。
操作将静默成功，您可以看到“加入 AD”选项变为“退出 AD”。 8
（可选） 要退出 Active Directory 域，请单击退出 AD。 9
重新启动 vCenter Server 以应用更改。
重要说明 如果不重新启动 vCenter Server，在使用 vSphere Client 时可能会遇到问题。
10 选择标识源选项卡，然后单击添加。
a
在“添加标识源”窗口中，选择 Active Directory (集成 Windows 身份验证) 作为“标识源类 型”。
vCenter Server 配置
VMware, Inc.
34
[第35页]
b
输入所加入的 Active Directory 域的标识源设置，然后单击添加。 表 3-2. 添加标识源设置 文本框 描述 域名
域的 FDQN。请勿在此文本框中提供 IP 地址。
使用计算机帐户
选择此选项可将本地计算机帐户用作 SPN。选择此选项
时，应仅指定域名。如果您希望重命名此计算机，请勿选
择此选项。
使用服务主体名称 (SPN)
如果您希望重命名本地计算机，请选择此选项。必须指定
SPN、能够通过标识源进行身份验证的用户以及该用户的
密码。
服务主体名称
有助于 Kerberos 识别 Active Directory 服务的 SPN。请
在名称中包含域，例如 STS/example.com。
您可能需要运行 setspn -S 以添加要使用的用户。有关
setspn 的信息，请参见 Microsoft 文档。
SPN 在域中必须唯一。运行 setspn -S 可检查是否未创 建重复项。 用户名
能够通过此标识源进行身份验证的用户的名称。请使用电
子邮件地址格式，例如 jchin@mydomain.com。可以通
过 Active Directory 服务界面编辑器 (ADSI Edit) 验证用 户主体名称。 密码
用于通过此标识源进行身份验证的用户的密码，该用户是
在用户主体名称中指定的用户。请包括域名，例如
jdoe@example.com。
结果
在标识源选项卡上，您可以看到已加入的 Active Directory 域。 后续步骤
您可以配置权限，以便已加入的 Active Directory 域中的用户和组配置可以访问 vCenter Server 组件。
有关管理权限的信息，请参见 《vSphere 安全性》文档。
将用户添加到 SystemConfiguration.BashShellAdministrators 组中
要使用 vSphere Client 启用对设备 Bash shell 的访问，则用于登录的用户必须是
SystemConfiguration.BashShellAdministrators 组的成员。默认情况下，此组为空且必须手动将用户添 加到该组。 前提条件
验证用于登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 域中
SystemConfiguration.Administrators 组的成员。
vCenter Server 配置
VMware, Inc.
35
[第36页]
步骤
1
使用 vSphere Client 以 administrator@your_domain_name 身份登录到 vCenter Server 实例。
地址类型为 http://appliance-IP-address-or-FQDN/ui。 2
在 vSphere Client 菜单中，选择系统管理。
3
选择Single Sign On > 用户和组。
4
单击组选项卡，从“组名称”列中提供的选项中选择
SystemConfiguration.BashShellAdministrators。 5 单击编辑。 6
在编辑组窗口中，要添加成员，请从下拉菜单中选择域，然后搜索所需用户。 7 单击保存。 重新引导节点
在 vSphere Client 中，可以重新引导 vCenter Server 中的节点。 前提条件
验证用于登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 域中
SystemConfiguration.Administrators 组的成员。 步骤 1
使用 vSphere Client 以 administrator@your_domain_name 身份登录到 vCenter Server 实例。 2
在 vSphere Client 主页面中，单击系统管理 > 部署 > 系统配置。 3
在“系统配置”下，从列表中选择一个节点。
4
单击重新引导节点。
查看 节点的运行状况
在 vSphere Client 中，可以查看 vCenter Server 节点的运行状况。
vCenter Server 实例和运行 vCenter Server 服务的计算机可视为节点。图形标志表示节点的运行状况。 前提条件
验证用于登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 域中
SystemConfiguration.Administrators 组的成员。 步骤 1
使用 vSphere Client 以 administrator@your_domain_name 身份登录到 vCenter Server 实例。
地址类型为 http://appliance-IP-address-or-FQDN/ui。 2
在 vSphere Client 菜单中，选择系统管理。
vCenter Server 配置
VMware, Inc.
36
[第37页]
3
选择部署 > 系统配置。
4
选择一个节点以查看其运行状况。
表 3-3. 运行状况
标志图标
描述
正常。对象的运行状况正常。
警告。对象存在某些问题。
严重。对象可能无法正常运行，或者即将停止运
行。
未知。此对象没有可用的数据。
导出支持包
可以导出包含 vCenter Server 所含特定产品的日志文件的支持包。 前提条件
确认登录到 vCenter Server 实例的用户是 vCenter Single Sign-On 中
SystemConfiguration.Administrators 组的成员。 步骤 1
使用 vSphere Client 以 administrator@your_domain_name 身份登录到 vCenter Server 实例。
地址类型为 http://appliance-IP-address-or-FQDN/ui。 2
在 vSphere Client 主页上，单击管理 > 部署 > 系统配置。 3
从列表中选择节点，然后单击导出支持包。
4
在导出支持包窗口中，展开树以查看设备中运行的服务，并取消选择您不想导出日志文件的服务。
默认选择所有服务。如果要导出支持包并将其发送到 VMware 支持，请选中所有复选框。这些服务分
为两个类别：一个是云基础架构类别，其中包含设备中特定产品的服务，另一个是虚拟设备类别，其中
包含专用于设备和 vCenter Server 产品的服务。
5
单击导出支持包，并将其保存到本地计算机。
结果
您已经将支持包保存到计算机上，现在可以浏览支持包。
vCenter Server 配置
VMware, Inc.
37
[第38页]
使用设备 Shell 配置 vCenter Server
4
通过使用设备 shell，您可以访问可用于监控和配置设备并对其进行故障排除的所有 vCenter Server API 命令和插件。
无论是否包含 pi 关键字，您都可以在设备 shell 中运行所有命令。 本章讨论了以下主题： n 访问设备 Shell n
从设备 Shell 启用和访问 Bash Shell
n
用于编辑命令的键盘快捷键
n
获取有关设备中插件和 API 命令的帮助
n
vCenter ServerShell 中的插件
n
使用 showlog 插件浏览日志文件
n
设备 Shell 中的 API 命令
n
配置 vCenter Server 的 SNMP
n
配置 vCenter Server 中的时间同步设置
n
管理 vCenter Server 中的本地用户帐户
n
监控 vCenter Server 中的运行状况和统计信息
n
使用 vimtop 插件监控服务的资源使用情况
访问设备 Shell
为了访问设备 shell 中包括的插件以及能够查看和使用 API 命令，首先需要访问设备 shell。 步骤 1 访问设备 shell。 n
如果可以直接访问设备控制台，请按 Alt+F1。
n
如果您想要远程连接，请使用 SSH 或其他远程控制台连接启动与设备的会话。 2
输入设备能够识别的用户名和密码。
VMware, Inc.
38
[第39页]
结果
您将登录到设备 shell 且可查看欢迎消息。
从设备 Shell 启用和访问 Bash Shell
如果以具有超级管理员角色的用户身份登录到设备 shell，则可以为其他用户启用对设备 Bash shell 的访
问。默认情况下，root 用户可以访问设备 Bash Shell。
设备 Bash Shell 默认情况下为 root 启用
步骤
1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
如果您要为其他用户启用 Bash shell 访问，请运行以下命令。
shell.set --enabled true
3
要访问 Bash shell，请运行 shell 或 pi shell。 用于编辑命令的键盘快捷键
您可以使用各种键盘快捷键在设备 Bash shell 中输入和编辑命令。
表 4-1. 键盘快捷键和功能
键盘快捷键
详细信息
选项卡
完成当前命令。如果输入部分命令名称并按 Tab 键，系统将完成此命令名称。
要查看与您输入的字符集匹配的命令，请键入一个字符并按 Tab 键。 Enter（在命令行处） 运行您输入的命令。
Enter（在 More 提示符处）
显示下一页输出。
Delete 或 Backspace
删除位于光标左侧的字符。
向左箭头或 Ctrl+B
将光标向左移动一个字符。
当您输入的命令超出一行时，可以按向左箭头或 Ctrl-B 键返回到命令的开头。 向右箭头或 Ctrl+F 将光标向右移动一个字符。 Esc、B 将光标向后移动一个单词。 Esc、F 将光标向前移动一个单词。 Ctrl+A 将光标移至命令行的开头。 Ctrl+E 将光标移至命令行的结尾。 Ctrl+D 删除光标选择的字符。 Ctrl+W 删除光标旁边的单词。
vCenter Server 配置
VMware, Inc.
39
[第40页]
表 4-1. 键盘快捷键和功能 （续）
键盘快捷键
详细信息
Ctrl+K
向前删除行。按 Ctrl+K 时，将删除从光标所在位置到命令行结尾输入的所有内容。
Ctrl+U 或 Ctrl+X
向后删除行。按 Ctrl+U 时，将删除从命令行开头到光标所在位置的所有内容。 Ctrl+T
更换光标左侧字符与光标所选字符的位置。
Ctrl+R 或 Ctrl+L
显示系统提示符和命令行。
Ctrl+V 或 Esc、Q
插入代码以指示系统必须将后面的按键视为命令条目，而不是编辑键。 向上箭头或 Ctrl+P
撤消历史缓冲区中的命令（从最近的命令开始）。
向下箭头或 Ctrl+N
在使用向上箭头或 Ctrl+P 撤消命令之后，返回到历史缓冲区中的最近命令。 Ctrl+Y
撤消删除缓冲区中的最近条目。删除缓冲区包含已剪切或删除的最后 10 个项目。 Esc、Y
撤消删除缓冲区中的下一个条目。删除缓冲区包含已剪切或删除的最后 10 个项目。首先按
Ctrl+Y 撤消最近的条目，然后按 Esc、Y 最多九次以撤消缓冲区中的剩余条目。 Esc、C 将光标所选字符改为大写。 Esc、U
将光标所选单词中的所有字符（直到下一个空格）都更改为大写。
Esc、L
将单词中光标所选字符到单词结尾的大写字母更改为小写。
获取有关设备中插件和 API 命令的帮助
您可以从设备 shell 访问vCenter Server 插件和 API 命令。可以使用这些插件和命令监控和配置设备并对 其进行故障排除。
您可以使用 Tab 键自动完成 API 命令、插件名称和 API 参数。插件参数不支持自动完成。 步骤 1
访问设备 shell 并登录。
2
要获取有关插件的帮助，请运行 help pi list 或 ? pi list 命令。
您将收到一份包含设备中所有插件的列表。
3
要获取有关 API 命令的帮助，请运行 help api list 或 ? api list 命令。
您将收到一份包含设备中所有 API 命令的列表。
4
要获取有关特定 API 命令的帮助，请运行 help api api_name 或 ? api api_name 命令。
例如，要收到有关 com.vmware.appliance.version1.timesync.set 命令的帮助，请运行 help api
timesync.set 或 ? api timesync.set。
vCenter Server 配置
VMware, Inc.
40
[第41页]
vCenter ServerShell 中的插件
通过vCenter Server 中的插件，可以访问各种管理工具。这些插件驻留在 CLI 本身。这些插件是独立的
Linux 或 VMware 实用程序，不依赖于任何 VMware 服务。
表 4-2. vCenter Server 中可用的插件
插件
描述
com.vmware.clear
可用于清除终端屏幕的插件。
com.vmware.cmsso-util
该插件可用于协调对 PNID 和计算机证书的更改、从
Component Manager 和 vCenter Single Sign-On 取消注册
节点以及重新配置 vCenter Server。
com.vmware.dcli
基于 vAPI 的 CLI 客户端。
com.vmware.nslookup
可用于查询域名系统 (DNS) 以获取域名或 IP 地址映射或获取任
何其他特定 DNS 记录的插件。
com.vmware.pgrep
可用于搜索所有命名进程的插件。
com.vmware.pgtop
可用于监控 PostgreSQL 数据库的插件。
com.vmware.ping
可用于 ping 远程主机的插件。接受相同的参数作为 bin/ping。
com.vmware.ping6
可用于 ping 远程主机的插件。接受相同的参数作为 bin/ ping6。
com.vmware.portaccess
可用于排除主机的端口访问故障的插件。
com.vmware.ps
可用于查看正在运行进程的统计信息的插件。
com.vmware.rvc
Ruby vSphere 控制台
com.vmware.service-control
可用于管理 VMware 服务的插件。
com.vmware.shell
允许访问设备 Bash shell 的插件。
com.vmware.showlog
可用于浏览日志文件的插件。
com.vmware.shutdown
可用于重新启动设备或关闭其电源的插件。
com.vmware.software-packages
可用于更新设备中软件包的插件。
com.vmware.support-bundle
可用于在本地文件系统上创建包并将其导出到远程 Linux 系统
的插件。如果您将该插件与 stream 命令结合使用，则不会在
本地文件系统上创建支持包，而会直接将其导出到远程 Linux
系统。
com.vmware.top
显示进程信息的插件。接受相同的参数作为 /usr/bin/top/。
com.vmware.tracepath
跟踪网络主机路径的插件。接受相同的参数作为 /sbin/
tracepath。
com.vmware.tracepath6
跟踪网络主机路径的插件。接受相同的参数作为 /sbin/
tracepath6。
com.vmware.updatemgr-util
可用于配置 VMware Update Manager 的插件。
vCenter Server 配置
VMware, Inc.
41
[第42页]
表 4-2. vCenter Server 中可用的插件 （续） 插件 描述
com.vmware.vcenter-restore
可用于还原 vCenter Server 的插件。
com.vmware.vimtop
可用于查看 vSphere 服务列表及其资源使用情况的插件。
使用 showlog 插件浏览日志文件
您可以浏览 vCenter Server 中的日志文件以检查它们是否存在错误。 步骤 1
访问设备 shell 并登录。
2
键入 showlog 命令，添加空格，并按 Tab 键以查看 /var/log 文件夹的所有内容。 3
运行以下命令以查看首次引导日志文件。
showlog /var/log/firstboot/cloudvm.log
设备 Shell 中的 API 命令
vCenter Server 中的 API 命令允许您执行各种管理任务。API 命令由设备管理服务提供。您可以编辑时间
同步设置、监控进程和服务、设定 SNMP 设置等。
表 4-3. vCenter Server 中可用的 API 命令 API 命令 描述
com.vmware.appliance.health.applmgmt.get
获取 applmgmt 服务的运行状况。
com.vmware.appliance.health.databasestorage.get 获取数据库存储的运行状况。
com.vmware.appliance.health.load.get
获取 CPU 负载的运行状况。
com.vmware.appliance.health.mem.get 获取内存运行状况。
com.vmware.appliance.health.softwarepackages.get 获取系统更新的运行状况。
com.vmware.appliance.health.storage.get 获取整体存储运行状况。
com.vmware.appliance.health.swap.get 获取交换运行状况。
com.vmware.appliance.health.system.get 获取系统运行状况。
com.vmware.appliance.health.system.lastcheck 获取上次检查运行状况的时间。
com.vmware.appliance.monitoring.list 获取监控项目列表。
com.vmware.appliance.monitoring.get 获取监控项目信息。
com.vmware.appliance.monitoring.query 查询监控项目值的范围。
vCenter Server 配置
VMware, Inc.
42
[第43页]
表 4-3. vCenter Server 中可用的 API 命令 （续） API 命令 描述
com.vmware.appliance.recovery.backup.job.cancel 按 ID 取消备份作业。
com.vmware.appliance.recovery.backup.job.create 启动备份作业。
com.vmware.appliance.recovery.backup.job.get 按 ID 获取备份作业状态。
com.vmware.appliance.recovery.backup.job.list 获取备份作业列表。
com.vmware.appliance.recovery.backup.parts.list
获取可包含在备份作业中的 vCenter
Server 组件的列表。
com.vmware.appliance.recovery.backup.parts.get 获取备份部分的详细信息。
com.vmware.appliance.recovery.backup.validate
在不启动备份作业的情况下验证该作业的
参数。
com.vmware.appliance.recovery.restore.job.cancel 取消还原作业。
com.vmware.appliance.recovery.restore.job.create 启动还原作业。
com.vmware.appliance.recovery.restore.job.get 获取还原作业的状态。
com.vmware.appliance.recovery.restore.validate
在不启动还原作业的情况下验证该作业的
还原参数。
com.vmware.appliance.system.uptime.get 获取系统正常运行时间。
com.vmware.appliance.version1.access.consolecli.get
获取有关基于控制台的受控 CLI (TTY1)
状态的信息。
com.vmware.appliance.version1.access.consolecli.set
设置基于控制台的受控 CLI (TTY1) 的已
启用状态。
com.vmware.appliance.version1.access.dcui.get
获取有关直接控制台用户界面 (DCUI
TTY2) 状态的信息。
com.vmware.appliance.version1.access.dcui.set
设置直接控制台用户界面 (DCUI TTY2)
的已启用状态。
com.vmware.appliance.version1.access.shell.get
获取有关 Bash shell 状态（即从受控 CLI
中访问 Bash shell）的信息。
com.vmware.appliance.version1.access.shell.set
设置 Bash shell 的已启用状态（即从受
控 CLI 中访问 Bash shell）。
com.vmware.appliance.version1.access.ssh.get
获取基于 SSH 的受控 CLI 的已启用状
态。
com.vmware.appliance.version1.access.ssh.set
设置基于 SSH 的受控 CLI 的已启用状
态。
com.vmware.appliance.version1.localaccounts.user.add 创建新的本地用户帐户。
com.vmware.appliance.version1.localaccounts.user.delete 删除本地用户帐户。
com.vmware.appliance.version1.localaccounts.user.get 获取本地用户帐户信息。
com.vmware.appliance.version1.localaccounts.user.list 列出本地用户帐户。
vCenter Server 配置
VMware, Inc.
43
[第44页]
表 4-3. vCenter Server 中可用的 API 命令 （续） API 命令 描述
com.vmware.appliance.version1.localaccounts.user.password.update
更新已登录用户或 username 参数中指
定用户的密码。
com.vmware.appliance.version1.localaccounts.user.set
更新本地用户帐户属性，如角色、全名、
已启用状态和密码。
com.vmware.appliance.version1.monitoring.snmp.disable
停止已启用的 SNMP 代理。
com.vmware.appliance.version1.monitoring.snmp.enable
启动已禁用的 SNMP 代理。
com.vmware.appliance.version1.monitoring.snmp.get 返回 SNMP 代理配置。
com.vmware.appliance.version1.monitoring.snmp.hash
生成本地化密钥以进行安全 SNMPv3 通
信。
com.vmware.appliance.version1.monitoring.snmp.limits 获取 SNMP 限制信息。
com.vmware.appliance.version1.monitoring.snmp.reset 将设置还原为出厂默认值。
com.vmware.appliance.version1.monitoring.snmp.set 设置 SNMP 配置。
com.vmware.appliance.version1.monitoring.snmp.stats
为 SNMP 代理生成诊断报告。
com.vmware.appliance.version1.networking.dns.domains.add 将域添加到 DNS 搜索域。
com.vmware.appliance.version1.networking.dns.domains.list 获取 DNS 搜索域的列表。
com.vmware.appliance.version1.networking.dns.domains.set 设置 DNS 搜索域。
com.vmware.appliance.version1.networking.dns.hostname.get 获取完全限定域名。
com.vmware.appliance.version1.networking.dns.hostname.set 设置完全限定域名。
com.vmware.appliance.version1.networking.dns.servers.add
添加 DNS 服务器。如果使用 DHCP，此
方法将失败。
com.vmware.appliance.version1.networking.dns.servers.get 获取 DNS 服务器配置。
com.vmware.appliance.version1.networking.dns.servers.set
设置 DNS 服务器配置。如果将主机配置
为通过使用 DHCP 获取 DNS 服务器和
主机名，则会强制执行 DHCP 刷新。
com.vmware.appliance.version1.networking.firewall.addr.inbound.add
添加防火墙规则以允许或拒绝从入站 IP
地址访问。
com.vmware.appliance.version1.networking.firewall.addr.inbound.delete
删除给定位置上的特定规则，或删除所有
规则。
com.vmware.appliance.version1.networking.firewall.addr.inbound.list
获取防火墙规则允许或拒绝的入站 IP 地
址的排序列表。
com.vmware.appliance.version1.networking.interfaces.get 获取有关特定网络接口的信息。
com.vmware.appliance.version1.networking.interfaces.list
获取可用网络接口（包括尚未配置的接
口）的列表。
com.vmware.appliance.version1.networking.ipv4.get
获取接口的 IPv4 网络配置。
vCenter Server 配置
VMware, Inc.
44
[第45页]
表 4-3. vCenter Server 中可用的 API 命令 （续） API 命令 描述
com.vmware.appliance.version1.networking.ipv4.list
获取配置的所有接口的 IPv4 网络配置。
com.vmware.appliance.version1.networking.ipv4.renew
更新接口的 IPv4 网络配置。如果将接口
配置为使用 DHCP 进行 IP 地址分配，则
会更新接口租约。
com.vmware.appliance.version1.networking.ipv4.set
设置接口的 IPv4 网络配置。
com.vmware.appliance.version1.networking.ipv6.get
获取接口的 IPv6 网络配置。
com.vmware.appliance.version1.networking.ipv6.list
获取配置的所有接口的 IPv6 网络配置。
com.vmware.appliance.version1.networking.ipv6.set
设置接口的 IPv6 网络配置。
com.vmware.appliance.version1.networking.routes.add
添加静态路由规则。0.0.0.0/0（对于
IPv4）或 ::/0（对于 IPv6）类型的目标/
前缀指默认网关。
com.vmware.appliance.version1.networking.routes.delete 删除静态路由规则。
com.vmware.appliance.version1.networking.routes.list
获取路由表。0.0.0.0/0（对于 IPv4）
或 ::/0（对于 IPv6）类型的目标/前缀指
默认网关。
com.vmware.appliance.version1.ntp.get
获取 NTP 配置设置。如果运行
tymesync.get 命令，则可以检索当前
时间同步方法（通过使用 NTP 或
VMware Tools）。ntp.get 命令始终
会返回 NTP 服务器信息，即使时间同步
方法未设置为 NTP。如果未通过使用
NTP 设置时间同步方法，NTP 状态将显
示为关闭。
com.vmware.appliance.version1.ntp.server.add
添加 NTP 服务器。此命令可将 NTP 服
务器添加到配置中。如果时间同步基于
NTP，则将重新启动 NTP 守护进程以重
新加载新的 NTP 服务器。否则，此命令
仅将服务器添加到 NTP 配置中。
com.vmware.appliance.version1.ntp.server.delete
删除 NTP 服务器。此命令可从配置中删
除 NTP 服务器。如果时间同步模式基于
NTP，则将重新启动 NTP 守护进程以重
新加载新的 NTP 配置。否则，此命令仅
从 NTP 配置中删除服务器。
com.vmware.appliance.version1.ntp.server.set
设置 NTP 服务器。此命令可从配置中删
除旧的 NTP 服务器，并在配置中设置输
入 NTP 服务器。如果通过使用 NTP 设
置时间同步，则将重新启动 NTP 守护进
程以重新加载新的 NTP 配置。否则，此
命令仅使用您作为输入提供的 NTP 服务
器替换 NTP 配置中的服务器。
com.vmware.appliance.version1.resources.cpu.stats.get 获取 CPU 统计信息。
vCenter Server 配置
VMware, Inc.
45
[第46页]
表 4-3. vCenter Server 中可用的 API 命令 （续） API 命令 描述
com.vmware.appliance.version1.resources.load.health.get 获取负载运行状况。
com.vmware.appliance.version1.resources.load.stats.get
获取负载平均值（1、5 和 15 分钟时间间
隔内）。
com.vmware.appliance.version1.resources.mem.health.get 获取内存运行状况。
com.vmware.appliance.version1.resources.mem.stats.get 获取内存统计信息。
com.vmware.appliance.version1.resources.net.stats.get 获取网络统计信息。
com.vmware.appliance.version1.resources.net.stats.list
获取已打开并在运行的所有接口的网络统
计信息。
com.vmware.appliance.version1.resources.processes.stats.list 获取所有进程的统计信息。
com.vmware.appliance.version1.resources.softwarepackages.health.get 获取更新组件的运行状况。
com.vmware.appliance.version1.resources.storage.health.get 获取存储运行状况统计信息。
com.vmware.appliance.version1.resources.storage.stats.list
获取每个逻辑磁盘的存储统计信息。
com.vmware.appliance.version1.resources.swap.health.get 获取交换运行状况。
com.vmware.appliance.version1.resources.swap.stats.get 获取交换统计信息。
com.vmware.appliance.version1.resources.system.health.get 获取系统的整体运行状况。
com.vmware.appliance.version1.resources.system.stats.get 获取系统状态。
com.vmware.appliance.version1.services.list 获取所有已知服务的列表。
com.vmware.appliance.version1.services.restart 重新启动服务。
com.vmware.appliance.version1.services.status.get 获取服务的状态。
com.vmware.appliance.version1.services.stop 停止服务。
com.vmware.appliance.version1.system.storage.list 获取磁盘到分区的映射。
com.vmware.appliance.version1.system.storage.resize
将所有分区的大小调整为磁盘大小的 1
倍。
com.vmware.appliance.version1.system.time.get 获取系统时间。
com.vmware.appliance.version1.system.update.get
获取基于 URL 的修补配置。
com.vmware.appliance.version1.system.update.set
设置基于 URL 的修补配置。
com.vmware.appliance.version1.system.version.get 获取设备的版本。
com.vmware.appliance.version1.timesync.get 获取时间同步配置。
com.vmware.appliance.version1.timesync.set 设置时间同步配置。
vCenter Server 配置
VMware, Inc.
46
[第47页]
配置 vCenter Server 的 SNMP
vCenter Server 包括一个可发送陷阱通知并接收 GET、GETBULK 和 GETNEXT 请求的 SNMP 代理。
您可以使用设备 shell API 命令启用和配置vCenter ServerSNMP 代理。您可以根据要使用的是 SNMP
v1/v2c 还是 SNMP v3，对代理进行不同的配置。
不支持 SNMP v3 通知。vCenter Server 仅支持通知，如具有所有安全级别的 v1 和 v2c 陷阱以及 v3 陷 阱。 配置轮询的 SNMP 代理
如果配置 vCenter ServerSNMP 代理以用于轮询，则它可以侦听和响应来自 SNMP 管理客户端系统的请
求，如 GET、GETNEXT 和 GETBULK 请求。
默认情况下，嵌入式 SNMP 代理侦听 UDP 端口 161 以轮询来自管理系统的请求。可以使用snmp.set
--port 命令配置备用端口。为避免 SNMP 代理的端口与其他服务的端口之间发生冲突，请使用没有
在 /etc/services 中定义的 UDP 端口。
步骤
1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --port 命令以配置端口。
例如，运行以下命令：
snmp.set --port port
此处，port 是用于侦听轮询请求的 SNMP 代理的端口。
重要说明 您指定的端口不能已由其他服务使用。使用动态范围内的 IP 地址以及端口 49152 及以上。 3
（可选） 如果 SNMP 代理未启用，可以通过运行 snmp.enable 命令启用。
为 SNMP v1 和 v2c 配置 vCenter Server
为 SNMP v1 和 v2c 配置 vCenter ServerSNMP 代理时，代理会支持发送通知和接收 GET 请求。
在 SNMP v1 和 v2c 中，社区字符串是包含一个或多个受管对象的命名空间。命名空间可以作为一种身份
验证的形式，但此种形式无法确保通信安全。要确保通信安全，请使用 SNMP v3。 步骤 1 配置 SNMP 社区
要启用 vCenter ServerSNMP 代理来发送和接收 SNMP v1 和 v2c 消息，您必须至少为代理配置一个 社区。 2
配置 SNMP 代理以发送 v1 或 v2c 通知
您可以使用 vCenter ServerSNMP 代理将虚拟机和环境通知发送到管理系统。
vCenter Server 配置
VMware, Inc.
47
[第48页]
配置 SNMP 社区
要启用 vCenter ServerSNMP 代理来发送和接收 SNMP v1 和 v2c 消息，您必须至少为代理配置一个社 区。
SNMP 社区定义一组设备和管理系统。只有属于同一社区的设备和管理系统可以交换 SNMP 消息。设备或
管理系统可以是多个社区的成员。
步骤
1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --communities 命令以配置 SNMP 社区。
例如，要配置公共、东部和西部网络操作中心社区，请运行以下命令：
snmp.set --communities public,eastnoc,westnoc
每次使用此命令指定社区时，您所指定的设置将覆写所有之前的配置。
要指定多个社区，请用逗号分隔社区名称。
配置 SNMP 代理以发送 v1 或 v2c 通知
您可以使用 vCenter ServerSNMP 代理将虚拟机和环境通知发送到管理系统。
要使用 SNMP 代理发送 SNMP v1 和 v2c 通知，则必须配置目标（接收方）、单播地址、社区以及可选端
口。如果不指定端口，则 SNMP 代理默认将通知发送到目标管理系统上的 UDP 端口 162。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --targets 命令：
snmp.set --targets target_address@port/community
此处，target_address、port 和 community 分别是目标系统的地址、通知发送到的端口号和社区名
称。端口值是可选的。如果未指定端口，则使用默认端口 161。
每次使用此命令指定目标时，您所指定的设置将覆写所有之前指定的设置。要指定多个目标，请用逗号 分隔它们。
例如，运行以下命令以配置目标 192.0.2.1@678/targetcommunity 和 2001:db8::1/anothercom：
snmp.set --targets 192.0.2.1@678/targetcommunity,2001:db8::1/anothercom 3
（可选） 如果 SNMP 代理未启用，可以通过运行 snmp.enable 命令启用。 4
（可选） 要发送测试陷阱以验证是否正确配置了代理，请运行 snmp.test 命令。
代理将 warmStart 陷阱发送到已配置的目标。
vCenter Server 配置
VMware, Inc.
48
[第49页]
为 SNMP v3 配置 vCenter Server
为 SNMP v3 配置 SNMP 代理时，代理会支持发送陷阱。SNMP v3 还提供比 v1 或 v2c 更高的安全性，包 括密钥身份验证和加密。
不支持 SNMP v3 通知。vCenter Server 仅支持通知，如具有所有安全级别的 v1/v2c 陷阱和 v3 陷阱。 步骤 1 配置 SNMP 引擎 ID
每个 SNMP v3 代理都具有一个引擎 ID 作为其唯一标识符。引擎 ID 与哈希功能配合使用可生成用于
对 SNMP v3 消息进行身份验证和加密的本地化密钥。
2
配置 SNMP 身份验证和隐私协议
SNMP v3 选择性地支持身份验证和隐私协议。
3
配置 SNMP 用户
您最多可配置五个有权访问 SNMP v3 信息的用户。用户名长度不得超过 32 个字符。 4 配置 SNMP v3 目标
配置 SNMP v3 目标以允许 SNMP 代理发送 SNMP v3 陷阱。 配置 SNMP 引擎 ID
每个 SNMP v3 代理都具有一个引擎 ID 作为其唯一标识符。引擎 ID 与哈希功能配合使用可生成用于对
SNMP v3 消息进行身份验证和加密的本地化密钥。
如果在启用 SNMP 代理之前未指定引擎 ID，则启用独立 SNMP 代理时系统会生成一个引擎 ID。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --engineid 命令以配置目标。 例如，运行以下命令：
snmp.set --engineid 80001adc802417e202b8613f5400000000
此处，80001adc802417e202b8613f5400000000 ID 是介于 5 到 32 个字符之间的十六进制字符 串。
配置 SNMP 身份验证和隐私协议
SNMP v3 选择性地支持身份验证和隐私协议。
身份验证用于确保用户的身份。隐私允许对 SNMP v3 消息进行加密以确保数据的保密性。隐私协议提供
比 SNMP v1 和 v2c（使用社区字符串确保安全性）更高的安全性级别。
身份验证和隐私都是可选项。但是，如果您计划启用隐私，则必须启用身份验证。
SNMP v3 身份验证和隐私协议是许可的 vSphere 功能，在某些 vSphere 版本中可能不可用。
vCenter Server 配置
VMware, Inc.
49
[第50页]
步骤
1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
（可选） 运行 snmp.set --authentication 命令以配置身份验证。 例如，运行以下命令：
snmp.set --authentication protocol
此处，protocol 必须为 none（不进行身份验证）、SHA1 或 MD5。 3
（可选） 运行 snmp.set --privacy 命令以配置隐私协议。 例如，运行以下命令：
snmp.set --privacy protocol
此处，protocol 必须为 none（无隐私）或 AES128。 配置 SNMP 用户
您最多可配置五个有权访问 SNMP v3 信息的用户。用户名长度不得超过 32 个字符。
在配置用户时，可以根据用户的身份验证和隐私密码以及 SNMP 代理的引擎 ID 生成身份验证和隐私哈希
值。如果在配置用户后更改引擎 ID、身份验证协议或隐私协议，则用户将不再有效，并且您必须重新配置 这些用户。 前提条件 n
在配置用户之前，验证是否已配置身份验证和隐私协议。
n
确认您知道计划配置的每个用户的身份验证和隐私密码。密码必须至少为 8 个字符。将这些密码存储 在主机系统上的文件中。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
如果您正在使用身份验证或隐私，请通过运行 snmp.hash --auth_hash --priv_hash 命令为用 户获取身份验证和隐私哈希值。 例如，运行以下命令：
snmp.hash --auth_hash secret1 --priv_hash secret2
此处，secret1 是包含用户身份验证密码的文件的路径，secret2 是包含用户隐私密码的文件的路径。
或者，您也可以指定标记 --raw_secret 并将布尔参数设置为 true。
系统会显示身份验证和隐私哈希值。
vCenter Server 配置
VMware, Inc.
50
[第51页]
3
通过运行 snmp.set --user 配置用户。
例如，运行以下命令：
snmp.set --user userid/authhash/privhash/security 此命令中的参数如下。 参数 描述 userid 替换为用户名。 authhash 替换为身份验证哈希值。 privhash 替换为隐私哈希值。 security
替换成为该用户启用的安全级别，其可以为 auth（代表仅身份验证）、priv（代表身份验证和隐私）或 none （代表无身份验证和隐私）。 配置 SNMP v3 目标
配置 SNMP v3 目标以允许 SNMP 代理发送 SNMP v3 陷阱。
您最多可以分别配置三个 SNMP v3 目标以及三个 SNMP v1/v2c 目标。
要配置一个目标，您必须指定接收陷阱的系统的主机名或 IP 地址、用户名、安全级别以及是否发送陷阱。
安全级别可以为 none（代表无安全）、auth（代表仅身份验证）或 priv（代表身份验证和隐私）。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --v3targets 命令以设置 SNMP v3 目标。 例如，运行以下命令：
snmp.set --v3targets hostname@port/userid/secLevel/trap 此命令中的参数如下。 参数 描述 hostname
替换为接收陷阱的管理系统的主机名或 IP 地址。
port
替换为接收陷阱的管理系统的端口。如未指定端口，则使用默认端口 161。 userid 替换为用户名。 secLevel
替换为 none、auth 或 priv 以指明您已配置的身份验证和隐私的级别。如果您仅配置了身份验证，请使用
auth，如果配置了身份验证和隐私，请使用 priv，如果两者均未配置，请使用 none。 3
（可选） 如果 SNMP 代理未启用，可以通过运行 snmp.enable 命令启用。 4
（可选） 要发送测试陷阱以验证是否正确配置了代理，请运行 snmp.test 命令。
代理将 warmStart 陷阱发送到已配置的目标。
vCenter Server 配置
VMware, Inc.
51
[第52页]
配置 SNMP 代理以筛选通知
如果不希望 SNMP 管理软件接收通知，可以配置 vCenter ServerSNMP 代理以筛选出这些通知。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 snmp.set --notraps 命令以筛选陷阱。
n
要筛选特定陷阱，请运行以下命令：
snmp.set --notraps oid_list
此处，oid_list 是要筛选的陷阱的对象 ID 列表（以逗号分隔）。此列表替换了之前使用此命令指 定的所有对象 ID。 n
要清除所有陷阱筛选器，请运行以下命令：
snmp.set --notraps reset
3
（可选） 如果 SNMP 代理未启用，可以通过运行 snmp.enable 命令启用。 结果
由指定的对象 ID 所标识的陷阱从 SNMP 代理的输出中筛选出，不发送到 SNMP 管理软件。
配置 SNMP 管理客户端软件
在配置 vCenter Server 以发送陷阱之后，还必须配置管理客户端软件，才能接收和解释这些陷阱。
要配置管理客户端软件，请指定受管设备的社区、配置端口设置并加载 VMware MIB 文件。有关这些步骤
的具体说明，请参见管理系统的文档。
前提条件
从 https://kb.vmware.com/s/article/1013445 下载 VMware MIB 文件。 步骤 1
在管理软件中，指定 vCenter Server 实例作为基于 SNMP 的受管设备。 2
如果您使用的是 SNMP v1 或 v2c，请在管理软件中设置适当的社区名称。
这些名称必须对应于为 vCenter Server 上的 SNMP 代理所设置的社区。 3
如果您使用的是 SNMP v3，请配置用户和身份验证与隐私协议，以与 vCenter Server 上配置的协议 相匹配。 4
如果将 SNMP 代理配置为将陷阱发送到除默认 UDP 端口 162 之外的受管系统上的端口，则请配置管
理客户端软件以侦听您配置的端口。
vCenter Server 配置
VMware, Inc.
52
[第53页]
5
将 VMware MIB 加载到管理软件中，以便查看 vCenter Server 变量的符号名称。
为防止出现查找错误，请在加载其他 MIB 文件之前按以下顺序加载这些 MIB 文件： a
VMWARE-ROOT-MIB.mib
b
VMWARE-TC-MIB.mib
c
VMWARE-PRODUCTS-MIB.mib
结果
管理软件现在可以从 vCenter Server 接收和解释陷阱。
将 SNMP 设置重置为出厂默认设置
您可以将 SNMP 设置重置为出厂默认设置。您还可以将特定参数的值重置为出厂默认设置。
您可以重置特定参数，例如社区或目标。您还可以将 SNMP 配置重置为出厂默认设置。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
要重置特定参数，请运行命令 snmp.set --arguments reset。
例如，要重置已配置的社区，请运行以下命令：
snmp.set --communities reset
3
要将整个 SNMP 配置重置为出厂默认设置，请运行 snmp.reset 命令。
配置 vCenter Server 中的时间同步设置
可以在部署后更改 vCenter Server 中的时间同步设置。
部署vCenter Server 时，可以选择时间同步方法：使用 NTP 服务器或使用 VMware Tools。如果
vSphere 网络连接中的时间设置发生更改，可以通过使用设备 shell 中的命令来编辑 vCenter Server 并配 置时间同步设置。
启用周期性时间同步时，VMware Tools 将客户机操作系统的时间设置为与主机的时间相同。
执行时间同步之后，VMware Tools 会每分钟检查一次，以确定客户机操作系统和主机上的时钟是否仍然
匹配。如果不匹配，则将同步客户机操作系统上的时钟以与主机上的时钟匹配。
本机时间同步软件（例如网络时间协议 (NTP)）通常比 VMware Tools 周期性时间同步更准确，因此成为
用户的首选。只能在vCenter Server 中使用一种形式的周期性时间同步。如果您决定使用本机时间同步软
件，则会禁用 vCenter ServerVMware Tools 周期性时间同步，反之亦然。
vCenter Server 配置
VMware, Inc.
53
[第54页]
使用 VMware Tools 时间同步
可以将 vCenter Server 设置为使用 VMware Tools 时间同步。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行以下命令以启用 VMware Tools 时间同步。
timesync.set --mode host
3
（可选） 运行以下命令，确认您已成功应用 VMware Tools 时间同步。 timesync.get
命令返回时间同步处于主机模式。
结果
设备的时间已与 ESXi 主机的时间同步。
在 vCenter Server 配置中添加或替换 NTP 服务器
要设置 vCenter Server 以使用基于 NTP 的时间同步，必须将 NTP 服务器添加到 vCenter Server 配置 中。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
通过运行以下 ntp.set 命令将 NTP 服务器添加到 vCenter Server 配置中。
ntp.set --servers IP-addresses-or-host-names
在此命令中，IP-addresses-or-host-names 是 NTP 服务器的 IP 地址或主机名的逗号分隔列表。
此命令将移除当前 NTP 服务器（如果有），并将新的 NTP 服务器添加到配置。如果时间同步基于
NTP 服务器，则将重新启动 NTP 守护进程以重新加载新的 NTP 服务器。否则，此命令会将 NTP 配
置中的当前 NTP 服务器替换为您指定的新 NTP 服务器。
3
（可选） 要验证是否已成功应用新的 NTP 配置设置，请运行以下命令。 ntp.get
命令返回配置以进行 NTP 同步的服务器的空格分隔列表。如果已启用 NTP 同步，此命令返回 NTP 配
置处于启用状态。如果已禁用 NTP 同步，此命令返回 NTP 配置处于禁用状态。
vCenter Server 配置
VMware, Inc.
54
[第55页]
4
（可选） 要验证 NTP 服务器是否可访问，请运行以下命令。
ntp.test --servers IP-addresses-or-host-names
该命令将返回 NTP 服务器的状态。
后续步骤
如果已禁用 NTP 配置，您可以将vCenter Server 中的时间同步设置配置为基于 NTP 服务器。请参见将
vCenter Server 中的时间与 NTP 服务器同步。
将 vCenter Server 中的时间与 NTP 服务器同步
您可以将 vCenter Server 中的时间同步设置配置为基于 NTP 服务器。 前提条件
在vCenter Server 配置中设置一个或多个网络时间协议 (NTP) 服务器。请参见在 vCenter Server 配置中 添加或替换 NTP 服务器。 步骤 1
访问设备 shell 并以具有管理员或超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行以下命令以启用基于 NTP 的时间同步。
timesync.set --mode NTP
3
（可选） 运行以下命令，确认您已成功应用 NTP 同步。
timesync.get
命令返回时间同步处于 NTP 模式。
管理 vCenter Server 中的本地用户帐户
如果以超级管理员的身份登录到设备 shell，则可以通过在设备 shell 中运行命令来管理vCenter Server 中
的本地用户帐户。具有超级管理员角色的默认用户是 root。
vCenter Server 中的用户角色
vCenter Server 中有三个主要用户角色。
vCenter Server 的本地用户具有执行各种任务的权限。vCenter Server 中提供三个用户角色： 运算符
具有操作员用户角色的本地用户可以读取 vCenter Server 配置。 管理员
vCenter Server 配置
VMware, Inc.
55
[第56页]
具有管理员用户角色的本地用户可以配置 vCenter Server。 超级管理员
具有超级管理员用户角色的本地用户可以配置 vCenter Server、管理本地帐户并使用 Bash shell。
获取 vCenter Server 中的本地用户帐户列表
您可以查看本地用户帐户列表，以便决定要从设备 shell 管理哪些用户帐户。 步骤 1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 localaccounts.user.list 命令。
可以查看本地用户列表。用户信息包括用户名、状态、角色、密码的状态、全名以及电子邮件地址。
注 本地用户列表仅包括将其默认 shell 作为设备 shell 的本地用户。
在 vCenter Server 中创建本地用户帐户
您可以创建新的本地用户帐户。
有关用户角色的信息，请参见 vCenter Server 中的用户角色。 步骤 1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 localaccounts.user.add --role --username --password 命令。
例如，要添加具有操作员用户角色的本地用户帐户 test，请运行以下命令：
localaccounts.user.add --role operator --username test --password
角色可以是 operator、admin 或 superAdmin。
还可以设置新的本地用户帐户并指定用户的电子邮件及全名。例如，要添加具有操作员用户角色、全名
为 TestName 且电子邮件地址为 test1@mymail.com 的本地用户帐户 test1，请运行以下命令：
localaccounts.user.add --role operator --username test1 --password --fullname TestName --
email test1@mymail.com
不能在全名中使用空格。
3
出现提示时，输入并确认新本地用户的密码。
结果
此时已在设备中创建新的本地用户。
vCenter Server 配置
VMware, Inc.
56
[第57页]
更新 vCenter Server 中的本地用户密码
出于安全原因，您可以更新 vCenter Server 中的本地用户密码。 步骤 1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 localaccounts.user.password.update --username user name --password 命 令。
例如，要更改用户名为 test 的用户密码，请运行以下命令：
localaccounts.user.password.update --username test --password 3
出现提示时，输入并确认新密码。
更新 vCenter Server 中的本地用户帐户
您可以在 vCenter Server 中更新现有本地用户帐户。
有关用户角色的信息，请参见 vCenter Server 中的用户角色。 步骤 1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 localaccounts.user.set --username 命令以更新现有本地用户。 n
要更新本地用户的角色，请运行以下命令：
localaccounts.user.set --username user name --role new role
其中，user name 是要编辑的用户的名称，而 new role 是新角色。角色可以是 operator、
admin 或 superAdmin。
n
要更新本地用户的电子邮件，请运行以下命令：
localaccounts.user.set --username user name --email new email address
其中，user name 是要编辑的用户的名称，而 new email address 是新的电子邮件地址。 n
要更新本地用户的全名，请运行以下命令：
localaccounts.user.set --username user name --fullname new full name
其中，user name 是要编辑的用户的名称，而 new full name 是该用户的新全名。 n
要更新本地用户的状态，请运行以下命令：
localaccounts.user.set --username user name --status new status
vCenter Server 配置
VMware, Inc.
57
[第58页]
其中，user name 是要编辑的用户的名称，而 status 是本地用户的新状态。此状态可以是已禁用 或已启用。
删除 vCenter Server 中的本地用户帐户
您可以删除 vCenter Server 中的本地用户帐户。
步骤
1
访问设备 shell 并以具有超级管理员角色的用户身份登录。
具有超级管理员角色的默认用户是 root。
2
运行 localaccounts.user.delete --username 命令。
例如，要删除用户名为 test 的用户，请运行以下命令：
localaccounts.user.delete --username test 该用户将被删除。
监控 vCenter Server 中的运行状况和统计信息
您可以在设备 shell 中使用 API 命令监控 vCenter Server 的硬件运行状况。您还可以通过监控更新组件的
健康状况，了解有关可用修补程序的信息。
您可以查看硬件组件（如内存、CPU、存储和网络）的状态以及更新组件的状态，后者可根据最后一次检
查可用修补程序的情况显示软件包是否为最新软件包。
特定健康状况可能是绿色、黄色、橙色、红色或灰色。有关详细信息，请参见查看 vCenter Server 运行状 况。
有关可用于监控 vCenter Server 系统的统计信息和运行状况的 API 命令的完整列表，请参见 设备 Shell 中的 API 命令。 步骤 1
访问设备 shell 并登录。
用于登录的用户名可以是具有操作员、管理员或超级管理员角色的用户。 2 查看特定组件的健康状况。 n
要查看 vCenter Server 中内存的运行状况，请运行 mem.health.get 命令。 n
要查看 vCenter Server 中存储的运行状况，请运行 storage.health.get 命令。 n
要查看 vCenter Server 中交换的运行状况，请运行 swap.health.get 命令。
vCenter Server 配置
VMware, Inc.
58
[第59页]
n
要查看 vCenter Server 中更新组件的运行状况，请运行 softwarepackages.health.get 命 令。
重要说明 如果不执行可用修补程序定期检查，更新组件的健康状况可能已过时。有关检查
vCenter Server 修补程序和启用 vCenter Server 修补程序的自动检查的信息，请参见
《《vSphere 升级》》。
n
要查看 vCenter Server 系统的整体运行状况，请运行 health.system.get 命令。 3
要查看有关特定硬件组件的统计信息，请运行相应的命令。
例如，要查看每个逻辑磁盘的存储统计信息，请运行 storage.stats.list 命令。
使用 vimtop 插件监控服务的资源使用情况
您可以使用 vimtop 实用程序插件监控 vCenter Server 中运行的 vSphere 服务。
vimtop 工具类似于 esxtop，在 vCenter Server 环境中运行。通过在设备 shell 中使用 vimtop 的文本
界面，您可以查看 vCenter Server 的总体信息，以及 vSphere 服务及其资源使用情况的列表。 n
通过在交互模式中使用 vimtop 监控服务
可以使用 vimtop 插件实时监控服务。
n
交互模式命令行选项
运行 vimtop 命令进入插件交互模式后，可以使用各种命令行选项。 n
vimtop 的交互模式单键命令
以交互模式运行时，vimtop 可识别几个单键命令。
通过在交互模式中使用 vimtop 监控服务
可以使用 vimtop 插件实时监控服务。
vimtop 交互模式的默认视图包括概览表和主表。您可以在交互模式下使用单键命令将进程视图切换为磁 盘视图或网络视图。 步骤 1
从 SSH 客户端应用程序登录到 vCenter Server shell。 2
运行 vimtop 命令在交互模式下访问插件。
vCenter Server 配置
VMware, Inc.
59
[第60页]
交互模式命令行选项
运行 vimtop 命令进入插件交互模式后，可以使用各种命令行选项。
表 4-4. 交互模式命令行选项
选项
描述
-h
显示 vimtop 命令行选项的帮助。
-v
显示 vimtop 版本号。
-c filename
加载用户定义的 vimtop 配置文件。如果未使用 -c 选项，默认配置文件为 /root/vimtop/ vimtop.xml。
使用 W 单键交互式命令可以创建自己的配置文件，同时指定不同的文件名和路径。 -n number
设置 vimtop 退出交互模式前执行迭代的次数。vimtop 将更新显示的次数 (number) 并退出。默认 值为 10000。 -p / -dseconds 设置更新时间段，以秒为单位。
vimtop 的交互模式单键命令
以交互模式运行时，vimtop 可识别几个单键命令。
所有交互模式面板都可识别下表中列出的命令。
表 4-5. 交互模式单键命令
键名称
描述
h
显示当前面板的帮助菜单，提供命令的简短摘要以及安全模式的状态。 i
显示或隐藏 vimtop 插件概览面板的顶线视图。
t
显示或隐藏“任务”部分，该部分在概览面板中显示 vCenter Server 实例上当前正在运行的任务的相关 信息。 m
显示或隐藏概览面板的“内存”部分。
f
显示或隐藏“CPU”部分，该部分在概览面板中显示所有可用 CPU 的相关信息。 g
显示或隐藏“CPU”部分，该部分在概览面板中显示前 4 个物理 CPU 的相关信息。 空格键 立即刷新当前窗格。 p
暂停当前面板中显示的有关服务资源使用情况的信息。
r
刷新当前面板中显示的有关服务资源使用情况的信息。
s
设置刷新时间间隔。
q
退出 vimtop 插件的交互模式。
k
显示主面板的“磁盘”视图。
o
将主面板切换到“网络”视图。
vCenter Server 配置
VMware, Inc.
60
[第61页]
表 4-5. 交互模式单键命令 （续）
键名称
描述
Esc
清除选择或返回主面板的“进程”视图。
Enter
选择服务以查看其他详细信息。
n
显示或隐藏主面板中的标头名称。
u
显示或隐藏主面板标头中的测量单位。
向左、向右箭头
选择列。
向上、向下箭头
选择行。
<,>
移动选定列。
删除
移除选定列。
c
向主面板的当前视图添加一列。使用空格键向显示的列表中添加列或移除其中的列。 a 将选定列按升序排列。 d 将选定列按降序排列。 z 清除所有列的排序顺序。 l 设置选定列的宽度。 x 将列宽度恢复为默认值。 + 展开选定的项目。 - 折叠选定的项目。 w
将当前设置写入 vimtop 配置文件。默认文件名是通过 -c 选项指定的文件名，如果不使用 -c 选项，则
为 /root/vimtop/vimtop.xml。也可以在 w 命令生成提示时指定其他文件名。
vCenter Server 配置
VMware, Inc.
61
[第62页]
使用直接控制台用户界面配置
vCenter Server
5
部署vCenter Server 后，可以重新配置网络设置并启用对 Bash shell 的访问以进行故障排除。要访问直
接控制台用户界面，必须以 root 用户身份登录。
直接控制台用户界面的主页包含一个指向vCenter Server 支持包的链接。指向支持包的链接为以下类型：
https://appliance-host-name:443/appliance/support-bundle。 本章讨论了以下主题： n 登录直接控制台用户界面 n 更改 root 用户的密码 n
配置 vCenter Server 的管理网络
n
重新启动 vCenter Server 的管理网络
n
启用对 Bash Shell 的访问
n
访问 Bash shell 以进行故障排除。
n
导出 vCenter Server 支持包以进行故障排除
登录直接控制台用户界面
通过直接控制台用户界面，您可以使用基于文本的菜单本地与 vCenter Server 交互。 步骤 1
从 vSphere Client 导航到主机，然后单击配置 > 服务。确认 SSH 和直接控制台用户界面服务正在运 行。 2
打开 SSH 客户端并连接到 vCenter Server。
3
使用 root 帐户登录。
4
输入 DCUI 以启动直接控制台用户界面。
5
在控制台窗口内单击，并按 F2 自定义系统。
6
键入 root 用户的密码并按 Enter。
重要说明 如果您连续三次输入无效凭据，root 帐户将被锁定五分钟。 VMware, Inc. 62 [第63页] 结果
您已登录直接控制台用户界面。您可以更改 root 用户的密码、编辑网络设置以及启用对 vCenter Server
Appliance Bash shell 的访问。
更改 root 用户的密码
为阻止对 vCenter Server 直接控制台用户界面的非授权访问，您可以更改 root 用户的密码。
vCenter Server 实例的默认 root 密码是您在部署期间输入的密码。
重要说明 vCenter Server 的 root 帐户的密码会在 90 天后过期。可以通过以 root 身份登录到 vCenter
ServerBash shell 并运行 chage -M number_of_days -W warning_until_expiration user_name 以更
改帐户的到期时间。要将 root 密码的到期时间设为无限期，可运行 chage -M -1 -E -1 root 命令。 步骤 1 登录直接控制台用户界面。 2
选择配置密码并按 Enter。
3
键入 root 用户的旧密码并按 Enter。
4
设置新密码并按 Enter。
5
按 Esc 直到返回到直接控制台用户界面的主菜单。
结果
设备 root 用户的密码已更改。
配置 vCenter Server 的管理网络
vCenter Server 实例可从 DHCP 服务器获取网络连接设置，也可以使用静态 IP 地址。可以从直接控制台
用户界面更改vCenter Server 的网络连接设置。可以更改 IPv4、IPv6 和 DNS 配置。 前提条件
要更改vCenter Server 实例的 IP 地址，请验证系统名称是否为 FQDN。如果在部署期间将 IP 地址设置
为系统名称，则在部署后将无法更改该 IP 地址。系统名称始终用作主网络标识符。 步骤 1
登录到 vCenter Server 的直接控制台用户界面
2
选择配置管理网络并按 Enter。
vCenter Server 配置
VMware, Inc.
63
[第64页]
3
从 IP 配置更改 IPv4 设置。
选项
描述
使用动态 IP 地址和网络配置
从 DHCP 服务器（如果网络上存在）获取网络连接设置
设置静态 IP 地址和网络配置
设置静态网络连接配置
4
从 IPv6 配置更改 IPv6 设置。
选项
描述
启用 IPv6
启用或禁用 IPv6
使用 DHCP 有状态配置
使用 DHCP 服务器获取 IPv6 地址和网络连接设置
使用 ICMP 无状态配置
使用无状态地址自动配置 (SLAAC) 获取 IPv6 地址和网络设置 5
从 DNS 配置更改 DNS 设置。
选项
描述
自动获取 DNS 服务器地址和主机名
自动获取 DNS 服务器地址和主机名。
如果从 DHCP 服务器自动获取 IP 设置，请使用此选项。
使用以下 DNS 服务器地址和主机名
设置 DNS 服务器的静态 IP 地址和主机名。
6
从自定义 DNS 后缀设置自定义 DNS 后缀。
如果没有指定任何后缀，则从本地域名中派生默认后缀列表。
7
按 Esc 直到返回到直接控制台用户界面的主菜单。
重新启动 vCenter Server 的管理网络
重新启动 vCenter Server 的管理网络以恢复网络连接。 步骤 1
登录到 vCenter Server 的直接控制台用户界面。
2
选择重新启动管理网络并按 Enter。
3
按 F11。
启用对 Bash Shell 的访问
可以使用直接控制台用户界面启用对 Bash shell 的本地和远程访问。通过直接控制台用户界面启用的
Bash shell 访问权限可持续 3600 秒。
步骤
1
登录到 vCenter Server 的直接控制台用户界面。
2
选择故障排除选项，然后按 Enter。
vCenter Server 配置
VMware, Inc.
64
[第65页]
3
从“故障排除模式选项”菜单中，选择启用 Bash shell 或 SSH。 4
按 Enter 以启用该服务。
5
按 Esc 直到返回到直接控制台用户界面的主菜单。
后续步骤
访问 vCenter ServerBash shell 以进行故障排除。
访问 Bash shell 以进行故障排除。
仅为进行故障排除登录 Bash shell。
步骤
1
使用以下方法之一访问 shell。
n
如果您可以直接访问 vCenter Server 实例，请按 Alt+F1。 n
如果您想要远程连接，请使用 SSH 或其他远程控制台连接启动会话。 2
输入用户名和密码 (Windows session credentials cannot be used to log into this server. Enter a
user name and password)。
3
在 shell 中，输入命令 pi shell 或 shell 以访问 Bash shell。
导出 vCenter Server 支持包以进行故障排除
您可以使用 DCUI 主屏幕上显示的 URL 来导出设备中 vCenter Server 实例的支持包以进行故障排除。
您也可以通过运行 vc-support.sh 脚本，从 vCenter Server Appliance Bash shell 收集支持包。
支持包将以 .tgz 格式导出。
步骤
1
登录到要下载包的 Windows 主机。
2
打开 Web 浏览器，然后输入 DCUI 中显示的支持包的 URL。
https://appliance-fully-qualified-domain-name:443/appliance/support-bundle 3
输入 root 用户的用户名和密码。
4
单击 Enter。
支持包将在 Windows 计算机上下载为 .tgz 文件。
5
（可选） 要确定哪个 firstboot 脚本失败，请检查 firstbootStatus.json 文件。
如果在 vCenter Server Appliance Bash shell 中运行 vc-support.sh 脚本，要检查
firstbootStatus.json 文件，请运行
cat /var/log/firstboot/firstbootStatus.json
vCenter Server 配置
VMware, Inc.
65