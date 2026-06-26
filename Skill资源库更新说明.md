# Skill 资源库更新说明

后续更新行业 Skill 资源库，只需要做这几步：

1. 更新底表  
   把最新内容维护在：
   `/Users/pirateli/Desktop/workbuddy/workbuddy共创营/Skill收集评测表.xlsx`

2. 保持这 4 列结构不变
   - `Skill类型`
   - `Skill名称`
   - `Skill能力描述`
   - `下载/教程链接`

3. 尽量把真实链接挂在第 4 列单元格上  
   页面会优先读取单元格超链接。

4. 双击运行：
   `/Users/pirateli/Documents/WB共创营/wb-workshop/一键更新行业Skill资源库.command`

脚本会自动完成：
- 读取 Excel
- 更新网页数据
- 生成提交
- 推送到 GitHub

如果推送失败，通常是网络或 GitHub 登录状态问题。此时本地提交还在，可以稍后重新推送。
