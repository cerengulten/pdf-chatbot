import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Extract pages of PDF as text 
def extract_pdf(pdf_path: str) -> str:
  doc = fitz.open(pdf_path)
  return "\n".join(page.get_text() for page in doc)

# Getting text and splitting into smaller chunks for better processing and embedding 
def text_split(text:str)-> list[str]:
  splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
  )
  return splitter.split_text(text)

