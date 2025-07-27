---
title: Github Release
author: derek
date: 2025-07-27 17:27:00 -0400
categories: [Notes, Code]
tags: [Git,Code]
render_with_liquid: false
---

# 🚀 GitHub Release 完整更新教學（UI版 + CLI版）

這份筆記教你兩種方式建立 GitHub Release，從程式修改 ➜ commit ➜ tag ➜ push ➜ 建立 Release，一步步做，適合初學者與熟手！

---

## ✅ 前置準備

請先準備好以下工具和條件：

- ✅ 一個已建立的 GitHub repository
- ✅ 已安裝 Git：https://git-scm.com/
- ✅ 如果你要用 CLI 方式，建議也安裝：
  - GitHub CLI（gh）：https://cli.github.com/
  - 並執行一次登入：
    ```bash
    gh auth login
    ```

---

## 📘 UI 版：用 GitHub 網頁建立 Release（適合初學者）

### 🪜 Step 1：程式修改並提交

1. 在本地修改好你的程式碼
2. 開啟終端機，執行：
   ```bash
   git add .
   git commit -m "feat: 加入新功能"
   git push origin main
   ```

---

### 🪜 Step 2：建立 Tag 並推送

```bash
git tag v1.2.3
git push origin v1.2.3
```

---

### 🪜 Step 3：到 GitHub 建立 Release

1. 打開你的 GitHub repository 頁面（例如：https://github.com/yourname/your-repo）
2. 找到右上角的 `About` 區塊，往下拉會見到 `Releases`  
3. 點擊 `Create a new release`
4. 填寫以下欄位：
   - **Tag version**：輸入剛剛推送的版本，例如 `v1.2.3`
   - **Release title**：也可以叫 `v1.2.3`
   - **Description**：輸入更新內容（支援 Markdown）
   - **可選：附加 zip 或執行檔**
5. 點擊藍色按鈕 `Publish release`

---

### 📝 Release Notes 範例（可複製貼上）

```markdown
## v1.2.3 (2025-07-27)

### ✨ 新功能
- 新增暗黑模式

### 🐛 Bug 修復
- 修正搜尋 JSON 特殊字元問題 (#2481)
```

---

## 🧑‍💻 CLI 版：全程使用 Git & GitHub CLI（不用開網頁）

### 🪜 Step 1：程式碼提交

```bash
git add .
git commit -m "feat: 加入新功能"
git push origin main
```

---

### 🪜 Step 2：建立並推送 Tag

```bash
git tag v1.2.3
git push origin v1.2.3
```

---

### 🪜 Step 3：建立 Release（兩種方式）

#### ✅ 方法一：直接輸入 notes

```bash
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes "### Bug Fixes\n- 修正 JSON 特殊字元處理 (#2481)"
```

#### ✅ 方法二：使用本地 Markdown 檔案

建立 `CHANGELOG.md` 檔案內容如下：

```markdown
## v1.2.3 (2025-07-27)

### ✨ 新功能
- 新增暗黑模式

### 🐛 Bug 修復
- 修正搜尋 JSON 特殊字元問題 (#2481)
```

然後執行：

```bash
gh release create v1.2.3 \
  --title "v1.2.3" \
  --notes-file CHANGELOG.md
```

---

### 📦 附加檔案（可選）

如果你有壓縮包或執行檔，例如 `./dist/app.zip`，可加上：

```bash
gh release create v1.2.3 ./dist/app.zip \
  --title "v1.2.3" \
  --notes-file CHANGELOG.md
```

---

### 🧩 快速全自動一行指令（選用）

```bash
git add . && git commit -m "feat: update" && git push origin main && \
git tag v1.2.3 && git push origin v1.2.3 && \
gh release create v1.2.3 --title "v1.2.3" --notes-file CHANGELOG.md
```

---

## 🧠 補充技巧

### 刪除 Release：
```bash
gh release delete v1.2.3
```

### 刪除遠端 Tag：
```bash
git tag -d v1.2.3
git push origin :refs/tags/v1.2.3
```

---

## ✅ 最終成果

你會在 GitHub 上看到一個 Release 頁面，包含：

- 🔖 版本號 v1.2.3
- 📝 Release notes 說明
- 📦 附加檔案（可選）

---

## 🎉 完成！

無論你使用 **UI** 或 **CLI**，現在你已經掌握從修改程式 ➜ commit ➜ tag ➜ 建立 Release 的完整流程！  
推薦方式：**熟手用 CLI，初學者先從 UI 開始！**