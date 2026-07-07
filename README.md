progress:

V1

✔ FastAPI

✔ Upload

✔ Basic OCR

✔ Regex Extraction

✔ Validation

✔ Decision Engine


V2

✔ Hybrid OCR

✔ Document Model

V3.5 (Current)

✔ Field Alias Dictionary

✔ OCR Normalizer

✔ Parser Utilities

✔ Document Parser

✔ Document Tokens

✔ Base Extractor

✔ Vendor Extractor

✔ Invoice Number Extractor

✔ Date Extractor
------------------------------------------------------------------------------------------------------------------------------------------

invoice-agent/

app.py

config.py

engine/
│
├── pipeline.py
├── document_engine.py
├── parser_engine.py
├── extraction_engine.py
├── validation_engine.py
├── confidence_engine.py
├── decision_engine.py
│
models/
│
├── document.py
├── invoice.py
├── document_token.py
├── invoice_item.py
│
parser/
│
├── document_parser.py
├── parser_utils.py
│
normalizer/
│
├── ocr_normalizer.py
│
extractors/
│
├── base_extractor.py
├── vendor_extractor.py
├── invoice_number_extractor.py
├── date_extractor.py
├── subtotal_extractor.py
├── gst_extractor.py
├── grand_total_extractor.py
├── table_extractor.py
│
rules/
│
├── field_aliases.py
├── validation_rules.py
│
utils/
│
├── logger.py
├── confidence.py
├── helpers.py
