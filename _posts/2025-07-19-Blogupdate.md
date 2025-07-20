---
title: BlogS Notes
author: derek
date: 2025-07-19 19:27:00 -0400
categories: [Notes, Blog]
tags: [Blog]
render_with_liquid: false
---

# 🛠️ 今日筆記：Git + Jekyll 修改與上傳流程（2025-07-20）

## ✅ 修改流程回顧

### 1. 修改多個檔案後，如何一次加入 Git 暫存區
```bash
git add .
```
說明：`.` 表示加入所有已修改或新增的檔案。

---

### 2. 正確格式提交訊息（避免 commitlint 錯誤）

```bash
git commit -m "feat: update about page and fix broken icons"
```

#### 常見類型（type）對應用途：
| type    | 用途說明               |
|---------|------------------------|
| feat    | 新增功能               |
| fix     | 修復 bug              |
| docs    | 說明文件修改           |
| style   | 格式調整（排版、空格） |
| refactor| 程式碼重構（非修 bug） |
| chore   | 雜項（不影響功能）     |

> ⚠️ 提交訊息格式必須為：`type: message`  
> 否則 `commitlint` 或 `husky` 會擋住你提交。

---

### 3. 將修改 push 到 GitHub

```bash
git push origin main
```

- 如果你在其他分支（例如 `dev`），請將 `main` 改成該分支名。

---

## 🐛 今天遇到的錯誤與解決方法

### YAML 語法錯誤
錯誤訊息：
```
could not find expected ':' while scanning a simple key
```

👉 解決方法：
- 使用 VS Code 或 Notepad++ 開啟對應 `.yml` 檔案
- 檢查 **縮排、冒號、引號** 是否正確
- 尤其多語言檔（如 `en.yml`, `fr-FR.yml`）要特別小心格式

---

## 🔁 本地 Jekyll 測試

```bash
bundle exec jekyll serve
```

- 啟動後可在 `http://localhost:4000` 預覽網站
- 出現 YAML 錯誤會導致啟動失敗，要修正後重啟

---

## 📘 小技巧備註

- 檔案有錯但不清楚哪個語言，可以嘗試先刪掉 `_data/locales` 裡的語言檔逐一測
- 提交前可先用 `git status` 查看有哪些檔案已修改
- commit message 遇到格式錯誤時，不妨加上 `--no-verify` 忽略檢查（不推薦長期用）

---

📅 日期：2025-07-20  
✍️ 記錄人：Derek