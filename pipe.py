import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px 
import os

file_path = input("Enter the path to your dfset (CSV or Excel): ")
if file_path.endswith('.csv'):
    df = pd.read_csv(file_path,encoding="latin1", on_bad_lines="skip")
elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
    df = pd.read_excel(file_path )
else:
    print("Unsupported file type.")

print("\nFirst 5 rows:")
print(df.head())

print("\nShape of dfset:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\n Null values par column:")
print(df.isnull().sum())

#EDA
df.columns=df.columns.str.strip().str.lower().str.replace(" ","-").str.replace(r'[^\w\S]','',regex=True)
print("\n column name cleaned:")
print(df.columns.tolist())

#removing duplicate column   
duplicates= df.duplicated().sum()
print(f"\n found{duplicates} duplicate rows .")
if duplicates >0 :
    df= df.drop_duplicates()
    print("duplicate column is removed . ")

#outlier by Z-Score and IQR METHOD 
numeric_column = df.select_dtypes(include=[np.number]).columns.tolist()

for col in numeric_column:
    print(f"\n columns : {col}")

    #Z score method 
    z = np.abs(stats.zscore(df[col].dropna()))
    z_outlier= df[col][(z > 3)]
    print(f"Z score outlier (>3 std): {len(z_outlier)}")
#IQR METHOD
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    iqr_outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"IQR Outliers: {iqr_outliers.shape[0]}")
    

#standardize catogorical values 
cat_col = df.select_dtypes(include="object").columns
df[cat_col]= df[cat_col].apply(lambda x :x.str.lower())
print("categorical column is converted into the Lower case .")

#date time column 
for col in df.columns:
    if 'date' in col:
        try:
            df[col]= pd.to_datetime(df[col])
            print(f"columns is converted in date time format .")
        except:
            print(f"could not coverted {col} ")





#cleaning percentage and rating like columns 
for col in df. columns:
    if df[col].dtype== "object":
        if df[col].astype(str).str.contains("%").sum() > 0:
            print(f"cleaning percentage column if there : {col}")
            df[col]=df[col].astype(str).str.replace("%"," ").astype(float)

        elif df[col].astype(str).str.contains("/").sum() > 0:
            print(f"cleaning rating column if there: {col}")
            df[col]=df[col].astype(str).str.split("/").str[0]
            df[col]= pd.to_numeric(df[col], errors="coerce")
             
    

# making fillna function for columns

for col in df.columns:
    if df[col].isnull().sum() > 0:
        print(f"\ncolumn: {col}")
        print(f"missing values:{df[col].isnull().sum()}")
        print(f"df type: {df[col].dtype}")

        print("what you want to fill missing values ? :")
        if np.issubdtype(df[col].dtype , np.number):
            print("choose: mean / sum / 0 / custom value")
        else:
            print("choose : NAN/ custom string")

        Choice= input("Enter your choice : ").strip()

        if np.issubdtype(df[col].dtype , np.number):
            if Choice=="mean":
                df[col]=df[col].fillna(df[col].mean())
            elif Choice == "sum" :
                df[col]=df[col].fillna(df[col].sum())
            elif Choice=="0":
                df[col]=df[col].fillna(0)
            else:
                try:
                    df[col]= df[col].fillna(float(Choice))
                except:
                    print("invalid input. Skipped")
        else:
            if Choice.lower()=="nan":
              df[col]=df[col].fillna("NAN")
              print("filled with NAN string")
            else:
                df[col]=df[col].fillna(Choice)
                print("filled with custom string")
                            
#checking our code 
print("\n✅ Final Null Values Check:")
print(df.isnull().sum())

print(f"\n Do you want  to save cleaned dataset ?")
savechoice= input("type 'yes' to save , or press Enter to skip :").strip().lower()

if savechoice== 'yes':
    file_type = input("choose format to save : CSV or Excel :").strip().lower()
    file_name= input("Enter a file name (without extension) :").strip()
    if file_type == "csv":
        df.to_csv(f"{file_name}.csv", index=False,encoding="latin1")
        print(f"file saved as : {file_name}.csv")
    elif file_type == "excel":
        df.to_excel(f"{file_name}.xlsx", index=False)
        print(f"✅ File saved as: {file_name}.xlsx")
    else:
        print("invalid choice. file not saved")
else:
    print("skipped saving file.")


    #DATA VISUALIZATION 

#numerical columns
numeric_col= df.select_dtypes(include=["int64","float64"]).columns.tolist()
#categorical columns

categorical_col=df.select_dtypes(include="object").columns.tolist()
#datetime columns 

datetime_col=df.select_dtypes(include="datetime").columns.tolist()

print("\n numeric columns:")
print(numeric_col if numeric_col else "None")
print("\n categorical  columns:")
print(categorical_col if categorical_col else "None")
print("\n datetime columns:")
print(datetime_col if datetime_col else "None")

#making graphs 

if not os.path.exists("plots"):
    os.mkdir("plots")

def plot_graph(column, graph_type):
    plt.figure(figsize=(10,8))

    if graph_type== "histogram":
        sns.histplot(df[column],kde=True)
        plt.title(f"histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("frequency")
    elif graph_type == "boxplot":
        sns.boxplot(x=df[column])
        plt.title(f"boxplot of {column}")
    elif graph_type== "bar":
        df[column].value_counts().plot(kind= "bar")
        plt.title(f"bar chart of {column}")
        plt.xlabel(column)
        plt.ylabel("count")
    elif graph_type == "line":
        plt.plot(df[column])
        plt.title(f"line  chart of {column}")
        plt.ylabel(column)
        plt.xlabel("index")
    elif graph_type == "pie":
        df[column].value_counts().head(15).plot(kind="pie",autopct="%1.1f%%")
        plt.title(f"pie chart of top 15 {column}")
    else:
        print("invalid graph type .")
        return
    plt.tight_layout()

    save= input("do you want to save this plot as PNG ? (yes/no):").lower()
    if save=="yes":
        file_name=f"plots/{column}_{graph_type}.png"
        plt.savefig(file_name)
        print(f"plots saved as {file_name}")

    plt.show()
    plt.close()


while True:
    print("\n Available columns :")
    print("Numerical :", numeric_col)
    print("categorical :", categorical_col)
    print("Datetime :", datetime_col)

    choice= input("\nDo you want to plot a single-column graph or a relation between a categorical and numerical column? (single/relation/exit): ").strip().lower()
    
    if choice=="exit":
        print("exiting the visualization .")
        break
    elif choice=="single":

      cols = input("Enter column name you want to visualiz:").strip()
      if cols not in df.columns:
        print("Invalid column. TRY AGAIN.")
        continue


        print("\nAvailable Graph Types:")
        print("1. histogram (numerical only)")
        print("2. boxplot (numerical only)")
        print("3. bar (categorical or discrete numerical)")
        print("4. line (numerical or datetime)")
        print("5. pie (categorical or limited unique values)")
 
        graph_types=input("ENter the graph type you want : ").strip().lower().split(",")

        for gtype in graph_types:
           gtype= gtype.strip()
           if gtype in ["histogram","boxplot"]and col not in numeric_col:
            print(f"Skipped: {gtype} not valid for non numeric column '{col}' .")
            continue
            if gtype=="line " and col not in numeric_col + datetime_col:
             print(f"Skipped: line chart not valid for this column .")
            continue
            if gtype in ["bar","pie"]and col not in categorical_col + numeric_col:
             print(f"Skipped: {gtype} not valid for this column .")
            continue


        plot_graph(cols,gtype)
        again=input("Do you want to visualize more graph ?(yes/no) :").lower()
        if again != "yes":
            continue

    elif choice== "relation":
        cat_col=input("Enter the categorical column name (x-axis) :").strip()
        num_col=input("Enter the numerical column name (y-axis) :").strip()
        if cat_col not in categorical_col or num_col not in numeric_col:
            print("Invalid column types . Try again sir.")
            continue

        print("\n Available plot Types for relation :")
        print("1. Bar (mean of numeric by category)")
        print("2. Box(distribution per category)")
        print("3. Voilin (detailed distribution)")


        relation_type= input("Enter the relation plot type :").strip().lower()

        plt.figure(figsize=(14,10))
        if relation_type=="bar":
            sns.barplot(x=cat_col, y=num_col,data=df,ci=None)
            plt.title(f"mean{num_col} per {cat_col}")
            plt.xticks(rotation= 45)
            
        elif relation_type=="box":
            sns.boxplot(x=cat_col, y=num_col,data=df)
            plt.title(f"{num_col}  distribution per {cat_col}")
            plt.xticks(rotation= 45)
        elif relation_type=="voilin":
            sns.violinplot(x=cat_col, y=num_col,data=df)
            plt.title(f"{num_col} distribution per {cat_col}")
            plt.xticks(rotation= 45)
        else:
            print("Invalid relation plot type")
            continue
        plt.tight_layout()
        save= input("Do you want to save this plot as PNG ? (yes/no) :").strip().lower()

        if save == "yes":
            file_name= f"plots/{cat_col}_{num_col}_{relation_type}.png"
            plt.savefig(file_name)
            print(f"plots saved as {file_name}")
            plt.show()
            plt.close

    else:
        print("invalid choice . Try again sir .")
















    
