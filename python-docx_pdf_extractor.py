#%pip install pdf2docx mammoth python-docx

from pydocx import PyDocX
from pdf2docx import Converter
import mammoth
from docx import Document
import pandas as pd

class docx_pdf_extractor:
    def __init__():
        pass

    def convert_pdf_to_docx(self,pdf_file, docx_file):
        '''
        Function to convert pdf to docx
        '''
        cv = Converter(pdf_file)
        cv.convert(docx_file, start=0, end=None)
        cv.close()


    def remove_images(self,docx_path):
        '''
        Function to remove images from docx file, as we are interested in content
        '''
        doc = Document(docx_path)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                rel.target_part._blob = b""
        temp_path = "temp_no_images.docx"
        doc.save(temp_path)
        return temp_path

    def convert_html(self,docx_path):
        """
        Function to convert docx file to html
        """
        style_map="""
        br[type='td'] => tr
        """
        with open(docx_path,"rb") as docx_file:
            result=mammoth.convert_to_html(docx_file,style_map=style_map)
        return result.value


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

if __name__ =="__main__":
    extractor = docx_pdf_extractor()
    pdf_path = "Attention.pdf"
    docx_path = "Attention.docx"
    extractor.convert_pdf_to_docx(pdf_path,docx_path)
    temp_path= extractor.remove_images(docx_path)
    html_content = extractor.convert_html(temp_path)
    df_list = extractor.create_df_list(html_content)
    extractor.multiple_dfs(df_list,"Attention.xlsx",1,"docx_output")
