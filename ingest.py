from pypdf import PdfReader


reader = PdfReader("pdfs/All in one.pdf")
num_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()


for page in reader.pages:
        with open("files/content.txt", "a", encoding = "utf-8") as f:
            f.write(page.extract_text().encode('ascii', errors = 'ignore').decode("ascii"))


