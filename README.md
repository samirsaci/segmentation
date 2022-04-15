# Automate ABC Analysis & Product Segmentation with Streamlit 📈
*A statistical methodology to segment your products based on turnover and demand variability using an automated solution with a web application designed with the framework Streamlit*

<p align="center">
  <img align="center" src="images/streamlit_capture.PNG" width=75%>
</p>
<p align="center"><b>streamlit Application UI</b></p>

Product segmentation refers to the activity of grouping products that have similar characteristics and serve a similar market. It is usually related to marketing _(Sales Categories)_ or manufacturing _(Production Processes)_. However as a **Supply Chaine Engineer** your focus is not on the product itself but more on the complexity of managing its flow.

Your want to understand the sales volumes distribution (fast/slow movers) and demand variability to optimize your production, storage and delivery operations to ensure the best service level by considering: 
- The highest contribution to your total volume: ABC Analysis
- The most unstable demand: Demand Variability

I have designed this **Streamlit App** to provide a tool to **Supply Chain Engineers** for Product Segmentation, with a focus on retail products, of their portofolio considering the complexity of the demand and the volumes contribution of each item.

### Understand the theory behind 📜
In this [Article](https://www.samirsaci.com/product-segmentation-for-retail-with-python/), you can find details about the theory used to build this tool. 

# Access the application 🖥️ 
> Access it here: [Product Segmentation for Retail](https://share.streamlit.io/samirsaci/segmentation/main/segmentation.py)

## **Step 0: Why should you use it?**
This Streamlit Web Application has been designed for Supply Chain Engineers to support them in their Inventory Management. It will help you to automate product segmentation using statistics.

## **Step 1: What do you want to do?**
You have two ways to use this application:
- 🖥️ Look at the results computed by the model using the pre-loaded dataset: in that case you just need to scroll to see the visuals and the analyses
OR
- 💾 Upload your dataset of sales records that includes columns related to:
  - **Item master data**
  _For example: SKU ID, Category, Sub-Category, Store ID_
  - **Date of the sales**:
  _For example: Day, Week, Month, Year_
  - **Quantity or value**: this measure will be used for the ABC analysis
  _For example: units, cartons, pallets or euros/dollars/your local currency_

## **Step 2: Prepare the analysis**

### **1. 💾 Upload your dataset of sales records**
<p align="center">
  <img align="center" src="images/step_1.PNG" width=40%>
</p>
<p align="center"><b>Step 1:</b> upload your dataset of sales records</p>


💡 _Please make sure that you dataset format is csv with a file size lower than 200MB. If you want to increase the size, you'd better copy this repository and deploy the app locally following the instructions below._

### **2. 📅 [Parameters] select the columns for the date (day, week, year) and the values (quantity, $)**
<p align="center">
  <img align="center" src="images/step_2.PNG" width=75%>
</p>
<p align="center"><b>Step 2:</b> select the columns for the date (day, week, year) and the values (quantity, $)</p>


💡 _If you have several columns for the date (day, week, month) and for the values (quantity, amount) you can use only one column per category for each run of calculation._

### **3. 📉 [Parameters] select all the columns you want to keep in the analysis**
<p align="center">
  <img align="center" src="images/step_3.PNG" width=75%>
</p>
<p align="center"><b>Step 3:</b> select the columns for the date (day, week, year)</p>


💡 _This step will basically help you to remove the columns that you do not need for your analysis to increase the speed of computation and reduce the usage of ressources._

### **4. 🏬 [Parameters] select all the related to product master data (SKU ID, FAMILIY, CATEGORY, STORE LOCATION)**
<p align="center">
  <img align="center" src="images/step_4.PNG" width=75%>
</p>
<p align="center"><b>Step 4:</b> select all the related to product master data (SKU ID, FAMILIY, CATEGORY, STORE LOCATION)</p>


💡 _In this step you will show at what granularity you want to do your analysis. For example it can be at:_
  - _Item, Store level: that means the same item in two stores will represent two SKU_
  - _Item ID level: that means you group the sales of your item in all stores_

### **5. 🛍️ [Parameters] select one feature you want to use for analysis by family**
<p align="center">
  <img align="center" src="images/step_5.PNG" width=75%>
</p>
<p align="center"><b>Step 5:</b> select one feature you want to use for analysis by family</p>


💡 _This feature will be used to plot the repartition of (A, B, C) product by family_

### **6. 🖱️ Click on Start Calculation? to launch the analysis**
<p align="center">
  <img align="center" src="images/step_6.PNG" width=75%>
</p>
<p align="center"><b>Step 6:</b> Start Calculation</p>


💡 _This feature will be used to plot the repartition of (A, B, C) product by family_

# Get insights about your sales records 💡

### **Pareto Analysis**

<p align="center">
  <img align="center" src="images/pareto.PNG" width=75%>
</p>
<p align="center"><b>Concept</b> Pareto Analysis</p>


**INSIGHTS:** 
1. How many SKU represent 80% of your total sales?
2. How much sales represent 20% of your SKUs?

_For more information about the theory behind the pareto law and its application in Supply Chain Management: [Pareto Principle for Warehouse Layout Optimization](https://www.samirsaci.com/reduce-warehouse-space-with-the-pareto-principle-using-python/)_

### **ABC Analysis with Demand Variability**

<p align="center">
  <img align="center" src="images/abc_analysis.PNG" width=75%>
</p>
<p align="center"><b>Streamlit App Screenshot:</b> ABC Analysis plot</p>


**QUESTIONS: WHAT IS THE PROPORTION OF?** 
1. **LOW IMPORTANCE SKUS**: C references
2. **STABLE DEMAND SKUS**: A and B SKUs with a coefficient of variation below 1 
3. **HIGH IMPORTANCE SKUS**: A and B SKUS with a high coefficient of variation

Your inventory management strategies will be impacted by this split:
- A minimum effort should be put in **LOW IMPORTANCE SKUS**
- Automated rules with a moderate attention for **STABLE SKUS**
- Complex replenishment rules and careful attention for **HIGH IMPORTANCE SKUS**


_For more information: [Article](https://www.samirsaci.com/product-segmentation-for-retail-with-python/)_

<p align="center">
  <img align="center" src="images/split_category.PNG" width=75%>
</p>
<p align="center"><b>Streamlit App Screenshot:</b> ABC SKU split for each family/category</p>


**QUESTIONS:** 
1. What is the split of SKUS by FAMILY?
2. What is the split of SKUS by ABC class in each FAMILY?


### **Normality Test**

<p align="center">
  <img align="center" src="images/normality.PNG" width=75%>
</p>
<p align="center"><b>Streamlit App Screenshot:</b> Normality test</p>


**QUESTION:** 
- Which SKUs have a sales distribution that follows a normal distribution?

Many inventory rules and safety stock formula can be used only if the sales distribution of your item is following a normal distribution. Thefore, it's better to know the % of your portofolio that can be managed easily.

_For more information: [Inventory Management for Retail — Stochastic Demand](https://www.samirsaci.com/inventory-management-for-retail-stochastic-demand-2/)_


# Build the application locally 🏗️ 

## **Build a python local environment (recommanded)** 

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv 

### Now create a virtual environment 

    virtualenv venv 
  
### Active your virtual environment    
    
    source venv/bin/activate
  
## Launch Streamlit 🚀

### Install all dependencies needed using requirements.txt

     pip install -r requirements.txt 

### Run the application  

    streamlit run segmentation.py 

### Click on the Network URL in the shell   
  <p align="center">
    <img align="center" src="images/network.PNG" width=50%>
  </p>
  
> -> Enjoy!
# About me 🤓
Senior Supply Chain Engineer with an international experience working on Logistics and Transportation operations. \
Have a look at my portfolio: [Data Science for Supply Chain Portfolio](https://samirsaci.com) \
Data Science for Warehousing📦, Transportation 🚚 and Demand Forecasting 📈 
