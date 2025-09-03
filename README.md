# 📊 WhatsApp Chat Analyzer  

A Streamlit-based web app to analyze WhatsApp chat exports.  
Upload your exported `_chat.txt` file, and the app will generate **interactive visualizations** and **statistics** about the conversation.

Select the option from the dropdown menu for which you want see the analysis 
Click on Show analysis button w.r.t to which you want to see the analysis 
---

## 🚀 Features  

- 📈 **Top Statistics**  
  - Total messages  
  - Total words  
  - Total links shared  

- 🗓 **Timeline Analysis**  
  - Monthly timeline of messages  
  - Daily timeline of messages  

- 📅 **Activity Maps**  
  - Most busy day of the week  
  - Most busy month  
  - Weekly activity heatmap  

- 👥 **User Insights** *(for group chats)*  
  - Most active users (Top 5)  
  - Percentage contribution of each user  

- ☁️ **Word Cloud**  
  - Visualization of the most common words  
  - Hinglish stopwords are filtered out  

- 🔠 **Most Common Words**  
  - Top 20 most frequent words used  

- 😀 **Emoji Analysis**  
  - Emoji usage frequency  
  - Emoji distribution pie chart  

---

## 📂 How to Export a WhatsApp Chat  

To analyze your data, you first need to **export a chat from WhatsApp**.  

1. Open WhatsApp on your phone.  
2. Go to the chat or group you want to analyze.  
3. Tap on the **three dots (⋮)** in the top right corner.  
4. Select **More → Export Chat**.  
5. **Important:** Choose **Without Media** (this ensures a smaller, cleaner `_chat.txt` file).  
6. Save or share the exported file to your computer.  
7. Rename the file if needed (default is usually `_chat.txt`).  

---

## ⚙️ Installation  

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/whatsapp-chat-analyzer.git
   cd whatsapp-chat-analyzer
