# Git 子模块使用指南

## 什么是 Git 子模块？

Git 子模块允许您将一个 Git 仓库作为另一个 Git 仓库的子目录。这让我们可以：

- 保持 IndexTTS 原始代码的独立性
- 方便地更新到最新版本
- 避免代码冲突
- 保持项目结构清晰

## 当前项目结构

```
index-tts2/                    # 主项目（您的二次开发）
├── .git/                      # 主项目的 Git 仓库
├── .gitmodules                # 子模块配置文件
├── index-tts/                 # IndexTTS 子模块
│   ├── .git/                  # IndexTTS 的 Git 仓库
│   ├── indextts/              # IndexTTS 源码
│   └── ...                    # 其他文件
└── src/                       # 您的二次开发代码
```

## 常用命令

### 1. 克隆包含子模块的项目

```bash
# 方法一：克隆时同时初始化子模块
git clone --recursive <your-repo-url>

# 方法二：先克隆，再初始化子模块
git clone <your-repo-url>
cd index-tts2
git submodule update --init --recursive
```

### 2. 更新子模块

```bash
# 更新到子模块的最新版本
git submodule update --remote

# 更新并合并到当前分支
git submodule update --remote --merge

# 使用批处理脚本（推荐）
更新tts2.bat
```

### 3. 查看子模块状态

```bash
# 查看子模块状态
git submodule status

# 查看子模块详细信息
git submodule foreach git status
```

### 4. 提交子模块更新

```bash
# 更新子模块后，需要提交主项目的更改
git add .gitmodules index-tts
git commit -m "Update IndexTTS submodule to latest version"
```

## 注意事项

### 1. 不要直接修改子模块代码

- 子模块 `index-tts/` 中的代码是原始 IndexTTS 项目
- 您的二次开发代码应该放在 `src/` 目录中
- 如果需要修改 IndexTTS 代码，建议 Fork 原始项目

### 2. 子模块更新流程

1. 运行 `更新tts2.bat` 或手动更新子模块
2. 测试更新后的功能
3. 提交主项目的更改（包含子模块指针的更新）

### 3. 团队协作

当团队成员拉取项目时，需要初始化子模块：

```bash
git pull
git submodule update --init --recursive
```

## 故障排除

### 问题1：子模块显示为未初始化

```bash
# 解决方案
git submodule update --init --recursive
```

### 问题2：子模块更新失败

```bash
# 清理并重新初始化
git submodule deinit -f index-tts
git submodule update --init --recursive
```

### 问题3：网络连接问题

```bash
# 使用镜像源
git config submodule.index-tts.url https://gitee.com/mirrors/index-tts.git
git submodule update --remote
```

## 最佳实践

1. **定期更新**：定期运行 `更新tts2.bat` 获取最新功能
2. **测试更新**：更新后测试所有功能是否正常
3. **版本控制**：为重要的子模块更新创建标签
4. **文档记录**：在提交信息中说明子模块更新的原因

## 示例工作流程

```bash
# 1. 更新子模块
更新tts2.bat

# 2. 测试功能
python web_ui.py

# 3. 提交更新
git add .gitmodules index-tts
git commit -m "Update IndexTTS to v1.5.1 - 添加新功能"

# 4. 推送到远程仓库
git push origin main
```

这样，您就可以安全地使用 Git 子模块来管理 IndexTTS 依赖，同时保持代码的独立性和可维护性。
