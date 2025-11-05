# 🌳 Survey Grove



A free, no-code survey analysis tool built with Streamlit.



Survey Grove helps you quickly analyze survey results directly from a CSV file — no coding required. Upload your data, define attributes and question types, and view clean visualizations with automatic statistical tests.





## 🚀 Features

Upload any survey CSV (one row per participant, one column per question)



Select up to three grouping attributes (e.g., Region, Location, Role)



Classify question columns as numeric or categorical



Define “positive” responses for categorical questions (e.g., Agree, Yes)



Automatically visualize results with:

* Boxplots for numeric questions
* Bar charts for categorical questions (% positive)
* Run statistical tests:
* ANOVA for numeric questions
* Chi-square for categorical questions
* Interactive app interface powered by Streamlit and Plotly
* 

## 🧠 How It Works

### Upload Data

Load your survey CSV file — each row should represent one respondent, and each column should be a question or attribute.



### Select Attributes

Choose up to three columns that define your groups (e.g., region, gender, department).



### Classify Questions

The app automatically detects numeric and categorical columns, but you can manually override each question’s type.



#### Define Positive Responses

For each categorical question, select which responses should count as “positive” (for example, Agree or Strongly Agree).



#### Run Analysis

Click 🚀 Run Survey Analysis to view:

* Interactive boxplots or bar charts
* Statistical tests (ANOVA or Chi²)
* Group-level summaries (% positive or mean differences)

# 

## 🧩 Example Use Case

Suppose you run a staff survey with columns like:



region	role	satisfaction	workload	recommend

North	Teacher	4	High	Yes

South	Admin	3	Medium	No



You could:

1. Select region as an attribute,
2. Mark satisfaction as numeric,
3. Mark recommend as categorical (positive = “Yes”),
4. Then visualize satisfaction and recommendation rates by region — complete with p-values for group differences.



#### ⚙️ Installation

Clone this repository and install dependencies:



&nbsp;	git clone https://github.com/yourusername/survey-grove.git

&nbsp;	cd survey-grove

&nbsp;	pip install -r requirements.txt





Run the app locally:



&nbsp;	streamlit run app.py



### 📦 Requirements

The app uses the following Python libraries:



streamlit

pandas

numpy

scipy

plotly



### 📊 Example Output

Numeric questions: Boxplot + ANOVA results



Categorical questions: Percent-positive bar chart + Chi² test



Statistical feedback: Clear messages about significance thresholds (p < 0.05)



#### 🔄 Resetting

The app includes reset buttons:



🔄 Reset App: Clears session state and restarts the workflow



🔄 Reset All: Clears all selections and data for a fresh start



#### 🪴 Author

Survey Grove was created by Kevin Verhoff to make data-driven survey analysis accessible for educators, nonprofits, and small organizations.



### 🪪 License



This project is licensed under the \*\*GNU Affero General Public License v3.0 (AGPL-3.0)\*\*.



You are free to use, modify, and distribute this software under the terms of the AGPL-3.0 license.  

If you modify or run this application on a server and allow users to interact with it over a network,  

you must make the source code of your modified version available to those users.



See the \[LICENSE](LICENSE) file for the full text.



