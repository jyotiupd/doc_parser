#!sudo apt install poppler-utils -y
#%pip install  "unstructured[all-docs]" pydantic lxml langchainhub

from typing import Any

from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import pandas as pd

class unstructured_pdf_extrcator:
    def __init__():
        pass
    def get_raw_pdf_elements(self,path):
        # Get elements
        raw_pdf_elements = partition_pdf(
            filename=path + "Attention.pdf",
            # Unstructured first finds embedded image blocks
            extract_images_in_pdf=False,
            # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
            # Titles are any sub-section of the document
            infer_table_structure=True,
            # Post processing to aggregate text once wze have the title
            chunking_strategy="by_title",
            # # Chunking params to aggregate text blocks
            # # Attempt to create a new chunk 3800 chars
            # # Attempt to keep chunks > 2000 chars
            max_characters=4000,
            new_after_n_chars=3800,
            combine_text_under_n_chars=2000,
            image_output_dir_path=path,
        )

        # Create a dictionary to store counts of each type
        category_counts = {}

        for element in raw_pdf_elements:
            category = str(type(element))
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1

        # Unique_categories will have unique elements
        unique_categories = set(category_counts.keys())
        print(category_counts)

        tables_dec = [el for el in raw_pdf_elements if el.category == "Table"]
        table_html = ''
        for i,table in enumerate(tables_dec):
            table_html += table.metadata.text_as_html+'/n'
        table_html

        return table_html


    def create_df_list(self,html_data):
        df_list=pd.read_html(html_data)
        return df_list

    def multiple_dfs(self,df_list, sheets, file_name, spaces):
        writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
        row = 0
        for dataframe in df_list:
            dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)   
            row = row + len(dataframe.index) + spaces + 1
        writer.close()


if __name__ == "__main__":
    path= "Attention.pdf"
    table_extractor= unstructured_pdf_extrcator()
    table_html= table_extractor.get_raw_pdf_elements(path)
    df_list = table_extractor.create_df_list(table_html)
    table_extractor.multiple_dfs(df_list, 'unstructured_output', 'unstructured_output.xlsx', 1)


