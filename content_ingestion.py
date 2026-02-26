import pdfplumber
import io


# PDFPLUMBER to extract text from pdf
try:
    def extract_text_from_pdf(file_path):
        full_text = []

        with pdfplumber.open(io.BytesIO(file_path.read())) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)

        return "\n".join(full_text)
except Exception as e:
    print(f"following exception occured:{e}")


if __name__ == "__main__":
    text = extract_text_from_pdf("Cover Letter- Shivam Puri.pdf")
    print(text[:500])
