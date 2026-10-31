---
name: jimeng-canvas
description: 即梦（Jimeng / dreamina）画布命令行工具：安装登录、做图（Seedream）、做视频（Seedance 2.5 样片模式）、做音乐、积分账本、提示词引用资产、运镜预设、参考视频、常见故障。在即梦上生成图片、视频或音乐之前先读。
---

# 即梦画布（dreamina-canvas CLI）

## 安装和登录（每个新容器都要做一次）
1. 安装：`curl -fsSL https://jimeng.jianying.com/canvas-cli/install.sh | bash`。**先下载脚本读一遍再运行。** CLI 装到 `~/.local/bin/dreamina-canvas`，官方 skill 装到 `~/.agents/skills/dreamina-canvas-cli/`（这个 skill 要读一遍）。
2. 登录：
   - `dreamina-canvas auth login --force`，拿到 device code 和授权链接；
   - **把链接用中文发给用户**，请用户在浏览器里确认；
   - `dreamina-canvas auth wait --device-code <code>`；
   - `auth status` 检查。登录有效期以 `auth status` 返回的 `expiresAt` 为准（实测约 6 小时），过期就重来。打开页面不等于授权完成，要以 `auth wait` 返回 `logged_in` 为准。
3. 核对参数：先运行 `dreamina-canvas schema` 和 `model list --type video/image/audio`，以实际返回为准。

## 用 tools/jm.py 生成（自带积分账本）
每个项目或每部片单独建一个画布和状态文件，例如 `projects/<名字>/jimeng-state.json`。状态文件里只存节点和资源 ID，不存 token。

```bash
S=projects/xxx/jimeng-state.json
python3 tools/jm.py $S upload KEY 本地图片.jpg          # 上传参考图，登记成节点 KEY
python3 tools/jm.py $S img KEY --title T --prompt "… @char_lead …"        # 做图：Seedream 5.0 Pro 2K，约 8 积分/张
python3 tools/jm.py $S vid KEY --title T --prompt "…" --mode m2v --model seedance_2.5_draft --res 480p --dur 15   # 视频：样片模式
python3 tools/jm.py $S music KEY --title T --prompt "…" --dur 60          # Seed Music，约 6 积分
python3 tools/jm.py $S quote KEY …     # 只报价
python3 tools/jm.py $S run KEY …       # 报价 → 检查预算 → 确认 → 运行
python3 tools/jm.py $S wait 输出目录 KEY …   # 等结果并下载
python3 tools/jm.py $S ledger          # 查积分账本
```
- **提示词里写 `@KEY`**（状态文件里已有的节点）会自动换成 `{{node:ID}}`，并把这个节点挂成参考。
- 新画布：`dreamina-canvas canvas create "名字" --project-id <自己生成的 UUID>`，然后手写状态文件 `{"projectId": …, "webUrl": …, "nodes": {}, "ledger": {"budget": N, "runs": []}}`。

## 规则
- **视频一律用样片模式**（`seedance_2.5_draft`，480p，约 9 积分 / 秒）。满意后由用户在网页画布上**直出 1080p**（10 秒约 640 积分），命令行没有这个入口。
- 做图可以直接做。**视频每次先报价，在预算内才运行。** 预算由用户定。
- 一次报价或运行最多约 10 个节点，多了会被拒（`service.2`），要分批。
- **运镜预设只能在网页上设：** 迎面跟拍、侧面跟拍、镜头左移/右移/上移/下移、急速推进、急速后移、FPV 穿越机、一镜到底等。
  - 做法：Claude 建好节点、写好提示词，告诉用户每个节点选哪个预设，由用户在网页上点选并运行。
  - 设过运镜预设的节点，`node show` 不再返回生成参数。**不要再用命令行改这类节点。**
  - 实测：预设能明显改善运镜，但要逐帧检查前景物体是否合理。
- Seedance 2.5 的全能参考模式（m2v）最多可以挂 30 张图、10 段视频、10 段音频做参考。可以用参考视频来指定运镜。

## 常见故障
- `upload_state_unknown`：用同一个 resource id 重试，jm.py 会自动沿用。
- 下载超过约 15 MB 会被拒（`download_too_large`），用户上传的参考片请用 480p。
- 连接中途断开（`ws_closed_mid_exchange`）：重试。
- 保存节点偶尔报 `invalid_input`：重试。
- 大 PNG 上传失败：改成 JPEG 再传。
- Seed Music 下载下来的是 MP3，后缀却是 `.wav`。它不按提示词里的时间点走。
- 生成结果失败（例如 serviceCode 20107）：平台侧失败，换提示词重试或报告用户。
