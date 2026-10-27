# Ai 自媒体互动

结合账号方向、目标人群和具体任务，生成3—5篇小红书互动笔记，每篇包含一句封面标题和1—3句正文。

内置15篇真实图文案例的封面、正文学习摘要、来源链接与结构观察。先找不同讨论点，再选固定句式或自然问法，减少只换词的重复内容。生成不依赖作者的工作台、Get笔记或TikHub账号。

## 安装（Codex）

打开Codex，粘贴下面这段话：

```text
请使用 $skill-installer 安装「Ai 自媒体互动」：
https://github.com/wangguoqing123/ai-media-interaction

Skill在仓库根目录，路径是“.”，安装名为 ai-media-interaction。
请完整保留 references、封面和 scripts。
安装后检查15篇案例及15张封面齐全。
```

安装成功后，下一条消息即可调用。若暂时没有识别到新Skill，重启Codex再试。[OpenAI官方说明](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use)

## 使用

把下面三项换成自己的情况，直接发给Codex：

```text
使用 $ai-media-interaction，帮我生成3—5篇互动笔记。
账号方向：[填写]
目标人群：[填写]
最近正在做或想做的具体事情：[填写]
```

例如，具体事情可以是“给家里的猫做一条15秒短片”，不要只填“学习AI”。已有账号方向时可以直接说“结合前面的定位”，缺少的具体信息Skill会简短补问。

也可以上传自己的参考截图或文案，参与这次生成。选出符合自己情况的稿子，改成自己的口吻再发布。

## 可选：素材自检

在Skill目录运行：

```bash
python3 scripts/casebook.py check
```

没有Python时，AI也可以直接读取 `references/case-index.md`、`references/cases.json` 和本地封面。

## 案例来源

[案例索引](references/case-index.md)保留原作者与原帖链接，正文使用学习摘要，原帖未显示正文的案例已注明。指标是采集日期快照。第三方案例与封面保留原作者归属，用于观察和学习提问方式；生成时使用自己的表达和素材。
