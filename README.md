[Running] python -u "c:\Users\LOQ 34\Downloads\New folder\analisis.py"
============================================================
  PRAKTIKUM ANALISIS DATA E-COMMERCE
============================================================

[1] LOAD DATA
----------------------------------------
Jumlah baris   : 150
Jumlah kolom   : 8

Info dataset:
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 150 entries, 0 to 149
Data columns (total 8 columns):
 #   Column            Non-Null Count  Dtype  
---  ------            --------------  -----  
 0   Order_ID          150 non-null    int64  
 1   CustomerID        150 non-null    int64  
 2   Order_Date        150 non-null    object 
 3   Product_Category  150 non-null    object 
 4   Quantity          150 non-null    int64  
 5   Price_Per_Unit    150 non-null    float64
 6   Ad_Budget         150 non-null    float64
 7   Total_Sales       143 non-null    float64
dtypes: float64(3), int64(3), object(2)
memory usage: 9.5+ KB
None

Preview 5 baris pertama:
   Order_ID  CustomerID  Order_Date  ... Price_Per_Unit  Ad_Budget  Total_Sales
0      1001        5039  2023-08-19  ...      1184000.0   982000.0    4736000.0
1      1002        5029  2023-08-29  ...      1733000.0  3513000.0    8665000.0
2      1003        5015  2023-02-21  ...      1767000.0  2117000.0    7068000.0
3      1004        5043  2023-04-06  ...       512000.0  4384000.0    1024000.0
4      1005        5008  2023-08-10  ...      1820000.0  2625000.0    3640000.0

[5 rows x 8 columns]

[2] DATA CLEANING
----------------------------------------
Missing values sebelum cleaning:
Order_ID            0
CustomerID          0
Order_Date          0
Product_Category    0
Quantity            0
Price_Per_Unit      0
Ad_Budget           0
Total_Sales         7
dtype: int64
Traceback (most recent call last):
  File "c:\Users\LOQ 34\Downloads\New folder\analisis.py", line 63, in <module>
    print(f"\n\u2713 {mask_null.sum()} baris Total_Sales kosong diimputasi (Quantity � Price_Per_Unit)")
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\LOQ 34\AppData\Local\Programs\Python\Python313\Lib\encodings\cp1252.py", line 19, in encode
    return codecs.charmap_encode(input,self.errors,encoding_table)[0]
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'charmap' codec can't encode character '\u2713' in position 2: character maps to <undefined>

[Done] exited with code=1 in 15.117 seconds
