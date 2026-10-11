# 🌿 Eco Plate AI — AI-Powered Food Waste Management

## 📌 Project Description

**Eco Plate AI** is a machine learning-powered food demand prediction and waste management application designed to help food service providers make smarter food preparation decisions.

The application analyzes historical food order data and uses a trained machine learning model to estimate the expected number of orders. Based on these demand estimates, users can explore demand trends, plan food preparation, and make better inventory decisions to reduce overproduction and food waste.

The interactive dashboard provides demand insights, data exploration, and a preparation planner that considers predicted demand, current stock, and a configurable safety buffer.

### 🎯 Project Objectives

* Predict food demand using a trained machine learning model.
* Help users plan food preparation based on estimated orders.
* Reduce unnecessary food production and potential food waste.
* Support inventory planning and stock management.
* Present useful insights through an interactive dashboard.

## ✨ Key Features

* **Demand Prediction:** Estimate expected orders using a trained ML model.
* **Overview Dashboard:** View key demand metrics and visual summaries.
* **Demand Insights:** Explore predicted demand across selected categories, cuisines, centers, and weeks.
* **Preparation Planner:** Estimate preparation quantities using predicted demand, available stock, and a safety buffer.
* **Data Exploration:** Filter and inspect the underlying dataset.
* **Interactive Visualizations:** Explore patterns and trends through charts and dashboard controls.

## 🛠️ Technology Stack

| Technology                | Purpose                                           |
| ------------------------- | ------------------------------------------------- |
| Python                    | Core programming language                         |
| Streamlit                 | Interactive web application and dashboard         |
| Pandas                    | Data loading, filtering, and processing           |
| Scikit-learn              | Machine learning model development and prediction |
| Joblib                    | Loading the saved model and feature configuration |
| Plotly                    | Interactive data visualizations                   |
| CSV                       | Storage of training and application data          |
| Git and GitHub            | Version control and source code hosting           |
| Streamlit Community Cloud | Online application deployment                     |

## 📁 Project Structure

```text
eco_plate_ai/
├── app.py
├── model.pkl
├── features.pkl
├── train_merged.csv
├── requirements.txt
└── README.md
```

* `app.py` — Main Streamlit application.
* `model.pkl` — Saved machine learning model.
* `features.pkl` — Saved list or configuration of model input features.
* `train_merged.csv` — Dataset used by the application.
* `requirements.txt` — Python dependencies required to run the application.
* `README.md` — Project description and setup instructions.

## ⚙️ Setup and Installation

### 1. Install Python

Install a compatible version of Python on your computer. Python 3.10 or 3.11 is a reasonable starting point, but use the version supported by your model dependencies.

Check your installation:

```bash
python3 --version
```

### 2. Download the Project

Clone your GitHub repository:

```bash
git clone https://github.com/YOUR_USERNAME/eco_plate_ai.git
cd eco_plate_ai
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

Alternatively, download the repository as a ZIP file and extract it.

### 3. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 4. Install Dependencies

Create a `requirements.txt` file containing the libraries used by the application:

```text
streamlit
pandas
scikit-learn
joblib
plotly
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

For reproducible deployment, pin compatible package versions after verifying the versions used to train and save the model.

### 5. Verify Project Files

Ensure the following files are present in the project directory:

* `app.py`
* `model.pkl`
* `features.pkl`
* `train_merged.csv`

The application needs the saved model, feature configuration, and dataset to run as written.

### 6. Run the Application

Start Streamlit with:

```bash
python3 -m streamlit run app.py
```

On Windows, you can also use:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use the Eco Plate AI dashboard.

**Important:** Run the app with Streamlit rather than `python app.py`. Also, make sure you launch it from the directory containing the required project files.

## ☁️ Deploy on Streamlit Community Cloud

1. Upload the project files to a GitHub repository.
2. Confirm that `app.py`, `model.pkl`, `features.pkl`, `train_merged.csv`, and `requirements.txt` are included.
3. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
4. Sign in using your GitHub account.
5. Select **Create app** and choose your repository, branch, and `app.py` as the main file.
6. Deploy the application.
7. Open the generated URL to access your dashboard online.

If deployment fails, check the build logs for missing dependencies, incorrect file paths, incompatible package versions, or missing model and dataset files.

## 📊 How to Use the Application

1. Open the dashboard.
2. Choose the desired category, cuisine, center, or week using the available filters.
3. Review the predicted demand and visual insights.
4. Open the Preparation Planner.
5. Enter or adjust the available stock and safety buffer.
6. Use the estimated preparation quantity to support food planning decisions.

## 🌍 Expected Impact

Eco Plate AI aims to help food service providers make data-informed preparation decisions, reduce avoidable food overproduction, improve stock planning, and support more sustainable food management practices.

The model's predictions are estimates rather than guarantees. Actual food waste reduction depends on how accurately the model predicts demand and how the recommendations are used.

## 🚀 Future Enhancements

* Food waste risk radar and stock-out risk indicators.
* Daily and weekly demand forecasting.
* Inventory tracking and expiry-date monitoring.
* Food donation recommendations for surplus stock.
* Dashboard reporting and downloadable insights.
* Model performance evaluation and forecast accuracy monitoring.

## 👩‍💻 Project Information

**Project Name:** Eco Plate AI
**Domain:** Machine Learning, Food Sustainability, and Waste Management
**Application Type:** Interactive Web Dashboard
**Primary Language:** Python
**Deployment Platform:** Streamlit Community Cloud
