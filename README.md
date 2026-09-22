# FireflyBot · 赞助/加好友落地页

一个静态单页赞助站，用于展示机器人、引导加好友、以及收集赞助。

## 📁 文件结构

```
fireflytip/
├── index.html                 # 主页面（已含全部逻辑，可直接用静态托管部署）
├── assets/
│   ├── qq_friend_qr.png       # ← 图1：QQ 好友二维码（必填）
│   ├── wechat_code.jpg        # ← 图2：微信赞赏码（必填）
│   ├── alipay_code.jpg        # ← 图3：支付宝收款码（必填）
│   └── help.png               # ← 指令速查图（由 tools/ 生成，可替换）
└── tools/
    ├── help-card.html         # 指令速查图的源文件（改这里的文案/配色）
    └── build-help.py          # 渲染成 assets/help.png（需要 Edge/Chrome + Pillow）
```

## 🖼️ 指令速查图（帮助图）

页面里「一分钟上手」那一块展示的图片就是 `assets/help.png`，可以直接存下来发到群里当帮助图。

改完 `tools/help-card.html` 后重新生成：

```bash
python tools/build-help.py
```

脚本会用本机的 Edge / Chrome 无头模式渲染，再自动裁掉底部空白并压缩成 256 色 PNG。

> 图里的前缀（指令用 `-`、聊天用 `-AI`）对应 AstrBot 配置里的
> `wake_prefix` 和 `provider_settings.wake_prefix`。改了配置记得同步这张图和页面文案。

## 🖼️ 放入图片

把三张二维码图片，按上面的**文件名**放到 `assets/` 目录下即可：

| 文件名 | 对应图片 |
|--------|----------|
| `qq_friend_qr.jpg`  | QQ 好友二维码（带 Firefly 头像的那张） |
| `wechat_code.jpg`   | 微信赞赏码（带空/GitHub 的那张） |
| `alipay_code.jpg`   | 支付宝收款码（林克名字那张） |

## 🔗 加好友跳转

`index.html` 里已配置好：
```js
const QQ_ADD_URL = "https://qm.qq.com/q/dV6q9frRRY";
```
点击**二维码图片**或 Hero 的「加我为好友」按钮，就会跳转到该链接，直接弹出 QQ 添加好友确认页。如需更换，改这里即可。

## 🚀 部署

这是一个纯静态 HTML，任选一种托管即可：
- **GitHub Pages**
- **Vercel / Netlify**
- **maozi.io**（你参考的那个站）
- 任意静态空间 / OSS

把 `sponsor_site/` 整个目录上传即可（assets 要一起）。

## ✏️ 可自定义

- 机器人昵称、功能标签：改 HTML 里 `机器人` / `功能` 区块的文字
- 主题色：改 `:root` 里的 CSS 变量
