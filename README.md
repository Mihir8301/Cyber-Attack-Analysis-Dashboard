# Cyber-Attack-Analysis-Dashboard

![Screenshot (195)](https://github.com/user-attachments/assets/a8e11298-7678-41ef-ad52-51faedf9a79d)

This work addresses critical cybersecurity challenges by introducing a unique open-source platform that utilizes data analysis and advanced Large Language Models (LLMs) such as Llama3. The platform is designed to empower various users—including individuals, business owners, and government officials—by allowing them to input specific parameters to visualize analyzed data on cyber threats. Additionally, Llama3 will provide personalized recommendations for system protection and strategic advice in the event of a cyber-attack. By integrating AI-driven insights with customizable user inputs, this platform aims to offer a comprehensive, accurate, and user-friendly approach to understanding and mitigating cyber risks. The open-source nature of the platform democratizes access to vital cybersecurity insights, contributing significantly to global digital security efforts.

![hb](https://github.com/user-attachments/assets/36753a28-ea9f-4793-a6ba-929b36bb080d)

1. Data Collection: The platform gathered data from various cyber databases and government websites, ensuring an up-to-date repository of cyber threat information. Python scripts and SQL were used to fetch and aggregate data from multiple sources based on the data's structure.
2. Data Preprocessing and Warehousing: The collected data was cleaned, transformed, and stored in a MS SQL Server data warehouse. This process involved using Python libraries such as Pandas for data cleaning and transformation and SQL for data retrieval.
3. Analysis of Data: The preprocessed data was analyzed to identify patterns and trends in cyber threats. Tools and libraries such as Pandas, Seaborn and others were used for statistical analysis to understand the behavior and evolution of cyber threats over time. This analysis assisted in deriving actionable insights and formed the basis for further recommendations.
4. Platform Development with Streamlit: The platform was developed using Streamlit, chosen for its ease of use and ability to create interactive web applications. Streamlit facilitated the creation of a user-friendly interface where users could input parameters and visualize data insights.
5. User Input and Data Visualization with Streamlit: Users provided specific parameters through the Streamlit interface. Based on these inputs, the platform generated graphs and visual representations of the analyzed data.
6. Integration of Llama3 for Recommendations: Llama3 was integrated to offer personalized recommendations by analyzing user inputs and providing strategic advice on mitigating cyber threats. Llama3 utilized a transformer architecture that processed input data through attention mechanisms, ensuring relevant and context-aware recommendations.

Moreover, the platform's user-centric approach allowed for customized inputs, leading to more relevant and actionable insights. Existing solutions often offered a one-size-fits-all approach, which might not address specific user needs. By allowing users to tailor their input parameters, the platform ensured that the generated data visualizations and recommendations were highly relevant to their unique contexts.

A critical feature of this platform was the integration of Llama3 with Streamlit. Llama3 leveraged advanced natural language processing capabilities to analyze user inputs and provide personalized cybersecurity recommendations. Embedding Llama3’s APIs within the Streamlit-based platform ensured an interactive and user-friendly interface where users could input specific parameters and instantly visualize analyzed data.

# Check Out the Walkthrough Video of the Platform
