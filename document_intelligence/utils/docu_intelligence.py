## Modules ##
from tabulate import tabulate
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import datetime
from datetime import date
import fitz
import re
import json
import os
from dotenv import load_dotenv
_ = load_dotenv("./config/azure.env")


class PDF_extractor:
    def __init__(self):
        self.endpoint = os.getenv("DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("DOCUMENT_INTELLIGENCE_KEY")
        self.model_id = os.getenv("DOCUMENT_INTELLIGENCE_MODEL_ID")



    def analyze_pdf(self,pdf_path='./012024_127180.pdf'):
        #pdf_path='/home/azureuser/cloudfiles/code/Users/JyotiSubhash.Upadhyay/adhoc/012024_127180.pdf'
        document_analysis_client = DocumentAnalysisClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)
        )

        overall_text = ""
        tables=[]
        pages = fitz.open(pdf_path)
        tablesCollected = []
        for index, page in enumerate(pages):
            pix = page.get_pixmap()  # render page to an image
            pix.save(os.path.join('./temp_folder/','temp.png'))
            with open(os.path.join('./temp_folder/','temp.png'), "rb") as f:
                poller = document_analysis_client.begin_analyze_document(self.model_id, document=f)
            result = poller.result()
            overall_text += "\n\n\n"+"page_number"+str(index+1)+": "+re.sub("Page|page|PAGE","",result.content.encode("ascii",errors="ignore").decode())

            for table_idx, table in enumerate(result.tables):
                #Initialize an empty matrix
                matrix = [["" for _ in range(table.column_count)] for _ in range(table.row_count)]
                tablesCollected.append(matrix)
                table_data=[]
                for cell in table.cells:
                    row_index = cell.row_index
                    column_index = cell.column_index
                    if row_index < table.row_count and column_index < table.column_count:
                        matrix[row_index][column_index] = cell.content
                    table_data.append({
                        "row":cell.row_index,
                        "column":cell.column_index,
                        "text":cell.content}
                    )
                tables.append({"page_number":index+1,"table":table_data})

            # Remove tables with only empty cells
            tablesCollected = [table for table in tablesCollected if any(any(cell.strip() for cell in row) for row in table)]
        return overall_text, tables, tablesCollected

    #format tables as text
    def tables_to_text(self,extracted_tables):
        table_as_text=[]
        for i, table in enumerate(extracted_tables):
            table_text = f"page_number{table['page_number']}: Table {i+1}:\n"
            table['table'].sort(key=lambda x: (x["row"],x["column"]))
            current_row=-1
            row_data=[]
            for cell in table['table']:
                if cell["row"]!= current_row:
                    if row_data:
                        table_text+="/t".join(row_data)+"\n"
                    current_row = cell["row"]
                    row_data=[]
                row_data.append(cell['text'])
            if row_data:
                table_text+="/t".join(row_data)+"\n"
            table_as_text.append(table_text)
            
        combined_tables= "\n".join(table_as_text)
        return combined_tables

    def tab_to_list(self,tab_data):
        df_list = []
        for i in tab_data:
            header = i[0]
            table = i[1:]
            # Create a DataFrame from the table
            df_list.append(pd.DataFrame(table,columns=header))
        return df_list

    def multiple_dfs(self,df_list, sheets="afr_output", file_name= "./afr_output.xlsx", spaces=1):
        """
        Function to write list of DF to excel
        """
        writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
        row = 0
        for dataframe in df_list:
            dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)   
            row = row + len(dataframe.index) + spaces + 1
        writer.save()

