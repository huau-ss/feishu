# **原文链接**: https://docs.netapp.com/us-en/ontap/task_admin_recover_deleted_volumes.html

**文档ID**: `bed6e8eb-148f-4c68-8a4f-8bcdcfc7ce7e`
**来源文件**: `F:\知识库\爬取的解决方案\netapp\netapp_system_admin_md\task_admin_recover_deleted_volumes.md`
**文件类型**: `md`
**文档类型**: `article`
**清洗时间**: `2026-04-21 14:19:52`

---

## 正文

# Recover deleted volumes**原文链接**: https://docs.netapp.com/us-en/ontap/task_admin_recover_deleted_volumes.html---![](https://docs.netapp.com/common/2/images/notification-icons.svg)The requested article is not available. Either it doesn't apply to this version of the product or the relevant information is organized differently in this version of the docs. You can search, browse, or go back to the other version.![](https://docs.netapp.com/common/2/images/dismiss.svg)# Recover deleted volumes12/16/2024
Contributors
[![netapp-aherbin](https://avatars.githubusercontent.com/u/38955266?v=4)](https://github.com/netapp-aherbin)
[![netapp-thomi](https://avatars.githubusercontent.com/u/54111336?v=4)](https://github.com/netapp-thomi)
[![manishc](https://avatars.githubusercontent.com/u/5731400?v=4)](https://github.com/manishc)
[![netapp-aaron-holt](https://avatars.githubusercontent.com/u/177328925?v=4)](https://github.com/netapp-aaron-holt)
[![netapp-ahibbard](https://avatars.githubusercontent.com/u/85892662?v=4)](https://github.com/netapp-ahibbard)
[![netapp-lenida](https://avatars.githubusercontent.com/u/54081920?v=4)](https://github.com/netapp-lenida)![](https://docs.netapp.com/common/2/images/discuss-sm.svg)Suggest changes
![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)
![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)* [Create a GitHub issue](https://github.com/NetAppDocs/ontap/issues/new?template=new-from-page.yml&page-url=https://docs.netapp.com/us-en/ontap/task_admin_recover_deleted_volumes.html&page-title=Recover deleted volumes)
* [Send us an email](javascript:netapp_mailto())![](https://docs.netapp.com/common/2/images/pdf-icon.png)PDFs![](https://docs.netapp.com/common/2/images/dropdown-arrow.svg)* [![](https://docs.netapp.com/common/2/images/pdf-icon.png)PDF of this doc site](/us-en/ontap/pdfs/fullsite-sidebar/ONTAP_9_documentation.pdf)[![](https://docs.netapp.com/common/2/images/pdf-zip.png)```
Collection of separate PDF docs
```](#)# Creating your file...This may take a few minutes. Thanks for your patience.CancelYour file is readyOKIf you have accidently deleted one or more FlexVol volumes, you can use System Manager to recover these volumes. Beginning with ONTAP 9.8, you can also user System Manager to recover FlexGroup volumes. You can also delete the volumes permanently by purging the volumes.The volume retention time can be set on a storage VM level. By default, the volume retention time is set to 12 hours.## Selecting deleted volumesSteps1. Click **Storage > Volumes**.
2. Click **More > Show Deleted Volumes**.
3. Select the volumes and click the desired action to recover or permanently delete the volumes.## Resetting the volume configurationsDeleting a volume deletes the associated configurations of the volume. Recovering a volume does not reset all the configurations. Perform the following tasks manually after recovering a volume to bring the volume back to its original state:Steps1. Rename the volume.
2. Set up a junction path (NAS).
3. Create mappings for LUNs in the volume (SAN).
4. Associate a snapshot policy and export policy with the volume.
5. Add new quota policy rules for the volume.
6. Add a QOS policy for the volume.