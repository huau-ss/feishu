# **原文**: https://docs.netapp.com/us-en/ontap/performance-admin/index.html

**文档ID**: `e8ced098-b9d1-43e8-af39-eacd5f21fa0c`
**来源文件**: `F:\知识库\爬取的解决方案\netapp\netapp_final_docs\index.md`
**文件类型**: `md`
**文档类型**: `article`
**清洗时间**: `2026-04-21 14:19:54`

---

## 正文

# Learn about ONTAP Active IQ Unified Manager performance monitoring and management**原文**: https://docs.netapp.com/us-en/ontap/performance-admin/index.html---![](https://docs.netapp.com/common/2/images/notification-icons.svg)The requested article is not available. Either it doesn't apply to this version of the product or the relevant information is organized differently in this version of the docs. You can search, browse, or go back to the other version.![](https://docs.netapp.com/common/2/images/dismiss.svg)# Learn about ONTAP Active IQ Unified Manager performance monitoring and management04/02/2026
Contributors
[![netapp-aherbin](https://avatars.githubusercontent.com/u/38955266?v=4)](https://github.com/netapp-aherbin)
[![netapp-barbe](https://avatars.githubusercontent.com/u/55463742?v=4)](https://github.com/netapp-barbe)
[![netapp-thomi](https://avatars.githubusercontent.com/u/54111336?v=4)](https://github.com/netapp-thomi)
[![netapp-dbagwell](https://avatars.githubusercontent.com/u/53352450?v=4)](https://github.com/netapp-dbagwell)
[![dmp-netapp](https://avatars.githubusercontent.com/u/50704017?v=4)](https://github.com/dmp-netapp)![](https://docs.netapp.com/common/2/images/discuss-sm.svg)Suggest changes
![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)
![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)* [Create a GitHub issue](https://github.com/NetAppDocs/ontap/issues/new?template=new-from-page.yml&page-url=https://docs.netapp.com/us-en/ontap/performance-admin/index.html&page-title=Learn about ONTAP Active IQ Unified Manager performance monitoring and management)
* [Send us an email](javascript:netapp_mailto())![](https://docs.netapp.com/common/2/images/pdf-icon.png)PDFs![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)* [![](https://docs.netapp.com/common/2/images/pdf-icon.png)PDF of this doc site](/us-en/ontap/pdfs/fullsite-sidebar/ONTAP_9_documentation.pdf)[![](https://docs.netapp.com/common/2/images/pdf-zip.png)```
Collection of separate PDF docs
```](#)# Creating your file...This may take a few minutes. Thanks for your patience.CancelYour file is readyOKYou can set up basic performance monitoring and management tasks and identify and resolve common performance issues.You can use these procedures to monitor and manage cluster performance if the following assumptions apply to your situation:* You want to use best practices, not explore every available option.
* You want to display system status and alerts, monitor cluster performance, and perform root-cause analysis by using Active IQ Unified Manager (formerly OnCommand Unified Manager), in addition to the ONTAP command-line interface.
* You are using the ONTAP command line interface to configure storage quality of service (QoS). QoS is also available through the following:+ System Manager
+ ONTAP REST API
+ ONTAP tools for VMware vSphere
+ NetApp Service Level Manager (NSLM)
+ OnCommand Workflow Automation (WFA)
* You want to install Active IQ Unified Manager by using a virtual appliance, instead of a Linux or Windows-based installation.
* You're willing to use a static configuration rather than DHCP to install the software.
* You can access ONTAP commands at the advanced privilege level.
* You are a cluster administrator with the "admin" role.Related informationIf these assumptions are not correct for your situation, you should see the following resources:* [Active IQ Unified Manager 9.8 Installation](http://docs.netapp.com/ocum-98/topic/com.netapp.doc.onc-um-isg/home.html)
* [System administration](../system-admin/index.html)