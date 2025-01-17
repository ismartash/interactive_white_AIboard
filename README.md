# **AI-Whiteboard**

## **Overview**
This project demonstrates **AI-Driven Digital Whiteboard**
An interactive digital whiteboard application enhanced with AI capabilities(**Gemini 2.0 Multimodal**, **llama-3.3-70b-versatile**, and **Groq**), including visual analysis and an integrated chatbot assistant. This application combines drawing tools, document handling, and image upload.user can ask and solve their doubt regards interface on whiteboard.
---

## **Features**
#### Visual Analysis about interface content
- 📸 Analysis of whiteboard content
- 🤖 Powered by Google Gemini 2.0 Flash
- 💡 Ask questions about your drawings and get solution
- 🔍 Real-time visual content interpretation

#### Intelligent Chatbot
- 💬 Built-in AI tutor using Groq LLM
- 🎯 Contextual learning support
- 📚 Educational assistance
- ⚡ Powered by LLama 3.3 70B model

### Document Features
- 📄 PDF document support
- ⏮️ Previous/Next slide navigation
- 📑 Multi-page document viewing
- 🖼️ Image insertion support
- 💡 Ask questions about your inserted image/pdf and get solution
---

## Tech Stack

**Frontend/UI:**
- Tkinter: For creating the graphical user interface (GUI) of the digital whiteboard.

**Backend:**
- Python

**Database:**
- MongoDB Atlas

**AI:**
- LangChain Framework
- Gemini 2.0 (Gemini API)
- ChatBot llama-3.3-70b-versatile (Groq API)
## Live demo using .exe  

1. **clone the  repository**  
    ```bash
   git clone https://github.com/ismartash/aidriven_whiteboard.git
   ```
   
2. **Run the Application**  
   - Double-click the `app.exe` file to launch the whiteboard application.

4. **Troubleshooting**  
   - If you encounter a security warning:
     - Click **"More info"**.
     - Select **"Run anyway"**.
   - Ensure your system has no restrictions on running `.exe` files from unverified publishers.

---
### **Steps to Run this Project**
1. Clone the repository:
   ```bash
   git clone https://github.com/ismartash/aidriven_whiteboard.git
   cd intelligentwhiteboard
   ```
2. **Create a `.env` file in the root directory** with the following content:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    MONGODB_URI=your_mongodb_atlas_connection_string_here
    GROQ_API_KEY=your_gemini_api_key_here
    ``` 
3. Create Conda Environment:
   ```bash
   conda create -n aiboard 
   conda activate aiboard
   ```
4. Install dependencies:
   ```bash
    pip install -r requirements.txt
    ```
5. Run the project:
   ```bash
     python app.py
     ```
