# zomato-chatbot

A conversational AI chatbot that provides menu insights and recommendations for Ghaziabad restaurants by leveraging web-scraped data, semantic search (RAG), and a Streamlit interface.

---

## 🚀 Project Overview

This project demonstrates a full end-to-end pipeline—from data collection to deploying a chat-based web app—for empowering users to explore local restaurant menus via a conversational interface. Key components include:

1. **Web Scraping**

   * Scraped menus and metadata (name, price, type, ratings, hours, etc.) for Ghaziabad restaurants from Zomato.
   * Tools: Selenium, BeautifulSoup, Pandas.
   * Adopted ethical practices: delays between requests, robots.txt compliance.

2. **Data Preprocessing & Feature Engineering**

   * Cleaned and enriched the raw dataset by filling missing descriptions.
   * Classified dishes by price range: **cheap**, **moderate**, **expensive**.
   * Created composite tags (e.g., cuisine, course) for improved searchability.
   * Final dataset: **1,375** menu items with new features `dish_type` and `tag`.

3. **Data Transformation**

   * Converted the processed CSV to structured JSON documents combining human-readable summaries with machine-friendly metadata.
   * Prepared data for semantic retrieval.

4. **RAG (Retrieval-Augmented Generation) Pipeline**

   * Embedded menu and restaurant data using `sentence-transformers/all-mpnet-base-v2`.
   * Stored embeddings in Pinecone for fast similarity search.
   * Utilized MistralAI to generate context-driven responses and enforce domain focus with prompt engineering.

5. **User Interface**

   * Built a Streamlit web app (`app2.py`) providing a real-time chat interface.
   * Displays answers, chat history, and relevant context snippets.

---

## 🎯 Features

* **Price Queries:** e.g., "List dishes under ₹150."
* **Dietary Filters:** Best vegetarian, vegan, or gluten-free options.
* **Category Insights:** Top-rated desserts, spice-level comparisons.
* **Budget Recommendations:** Affordable meal combos by price range.
* **Out-of-Scope Handling:** Refuses questions not covered by scraped data.

---

## ⚙️ Prerequisites

* Python ≥ 3.8
* pip or conda
* Streamlit
* Pinecone account & API key
* MistralAI credentials
* Google Chrome & ChromeDriver (for Selenium)

---

## 📦 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ghaziabad-restaurant-chatbot.git
   cd ghaziabad-restaurant-chatbot
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   export PINECONE_API_KEY="<your_pinecone_key>"
   export MISTRALAI_API_KEY="<your_mistralai_key>"
   ```

---

## 🏃‍♂️ How to Run

1. **Scrape & Preprocess Data**

   ```bash
   python scrape.py             # Runs Selenium + BeautifulSoup pipeline
   python preprocess.py        # Cleans and enriches CSV data
   ```

2. **Convert & Ingest**

   ```bash
   python data_converter.py     # CSV → JSON transformation
   python ingest.py            # Push JSON to Pinecone
   ```

3. **Launch RAG Pipeline**

   ```bash
   python rag_pipeline.py      # Build embedding + query functions
   ```

4. **Start the Streamlit App**

   ```bash
   streamlit run app2.py       # Opens chat UI in browser
   ```
---

## 🔍 Challenges & Solutions

* **Dynamic Web Content:** Handled with Selenium’s explicit waits and smart selectors.
* **Model Latency:** Switched from local Hugging Face to MistralAI API for faster inference.
* **Domain Control:** Used strict prompt engineering to prevent hallucinations and out-of-scope answers.

---

## 🌟 Future Improvements

* **Conversational Memory:** Maintain context across multi-turn dialogues.
* **Real-Time Updates:** Periodic re-scraping or streaming updates for menu changes.
* **Multimodal Search:** Integrate images of dishes for richer interaction.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

> *Built with ❤️ by Ayush Talan*
