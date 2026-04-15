from backend.ingest import extract_pdf, text_split

text = extract_pdf(r"C:\Users\crnyl\Desktop\Ceren_Yilmaz_Gulten_AI_Engineer_CV.pdf")
print(text)

chunks = text_split(text)
print(chunks[:2])