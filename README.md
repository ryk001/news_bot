# Google 新聞機器人 2024 版

<a href="url"><img src="https://s2.loli.net/2024/06/30/JqMlkrP4CSIz7jU.png" width="500" ></a>

想要每個上班日的早上在 LINE 收到特定關鍵字的新聞嗎？
請跟著這個步驟做下去^^

## 1. 申請 LINE 金鑰
這樣才可以傳訊息給自己，申請方式請參考: https://notify-bot.line.me/zh_TW


## 2. 複製這個專案到自己的帳號
- 專案地址：[github/news_bot](https://github.com/ryk001/news_bot.git)
- 點擊右上角 Fork 專案至自己的帳號底下

![run](https://s2.loli.net/2024/06/29/Zacqzg1kQ5wxKfu.png)


## 3. 設定新聞關鍵字、LINE 金鑰到 Secrets
(如果不設置 Secrets 的話所有人都可以傳 LINE 給你，也可以看到你的新聞關鍵字😂)
- 回到專案頁面，依次點擊`Settings`-->`Secrets`-->`New secret`

![run](https://s2.loli.net/2024/06/30/q9l67TORWCzSkVt.png)

- 建立一個名為`KEYWORDS`的 secret，裡面填上你要的關鍵字，假設你想要看到 "台積電"、"NVIDIA" 的新聞，則填入格式是：

  台積電
  
  NVIDIA
  
  (不需要加逗號，只需要換行來區分關鍵字)
- 再建立一個名為`LINE_NOTIFY_TOKEN`的 secret，裡面填上 LINE Notify 的金鑰
- **secret 必須按照以上格式填寫!!!**


## 4. 啟用 Actions

Actions 默認是關閉狀態，在 Fork 之後需要先手動執行一次，成功運行才會被激活。

返回項目主頁面，點擊上方的`Actions`，再點擊右側的`News-Bot`，再點擊`Run workflow`

![run](https://s2.loli.net/2024/06/30/KN9Ob2vy6dRMZzV.png)

運行成功後，就大功告成啦! 


## 結語/ 注意事項

感謝你看完文章，希望有幫助到你，有任何疑問與建議歡迎交流，我們下次見!!!

注意事項
- 約每 60 天 Actions 會重設一次，要記得上 GitHub 重新手動 Run
- GitHub 的 Actions 功能會延遲 5~30 分鐘，若有更可靠的自動化方法歡迎交流
- Google 新聞每隔一段時間會換介面，屆時爬蟲會失效
