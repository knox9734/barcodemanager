# 📦 Barcode Manager

A Django-based web application for managing products and generating EAN13 barcode labels with custom format logic. Designed for small shops or inventory managers who need a clean and efficient way to print and organize barcode labels in Sinhala and English.

---

## 🚀 Features

- ✅ Add, edit, and delete products
- ✅ Custom EAN13 barcode generation with structured pattern:  
  `CategoryCode(3) + ProductCode(4) + Serial(5) + CheckDigit(1)`
- ✅ Printable barcode label image generation with product info
- ✅ Sinhala & English text on labels
- ✅ Store barcode images per product
- ✅ Admin panel for product management
- ✅ Tailwind CSS frontend for beautiful UI
- ✅ Bulk product entry form

---

## 🖼️ Screenshots (optional)

> Add screenshots in the `/screenshots` folder and link here:
```md
![Add Product](screenshots/add_product.png)
![Barcode Label](screenshots/barcode_label_example.png)
```

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML + Tailwind CSS
- **Barcode Generator**: [`python-barcode`](https://pypi.org/project/python-barcode/) + [`Pillow`](https://pypi.org/project/Pillow/)
- **Database**: SQLite (or switch to PostgreSQL)
- **File Handling**: Barcodes stored in `media/barcodes/<product_name>/`

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/yourusername/barcode-manager.git
cd barcode-manager
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Create Admin User

```bash
python manage.py createsuperuser
```

### 6️⃣ Start Development Server

```bash
python manage.py runserver
```

---

## ✨ Usage

- Home: `http://127.0.0.1:8000/`
- Admin Panel: `http://127.0.0.1:8000/admin/`

### Generate Barcodes
- Go to product detail → click “Generate Barcodes”
- Set price, MFD, EXP, quantity
- Barcode label will be saved as image in `media/barcodes/<product_name>/`

---

## 📁 Project Structure

```
barcode-manager/
│
├── products/               # Django app with models, views, forms
├── templates/products/     # All HTML templates (styled with Tailwind)
├── static/                 # (optional) Static files
├── media/barcodes/         # Generated barcode images
├── db.sqlite3              # SQLite database
├── manage.py               # Django entry point
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

---

## ✅ Barcode Format

The barcodes follow a custom format:

```
[CCC][PPPP][SSSSS][C]
CCC   = Category code (e.g., 200 = rice)
PPPP  = Product code (e.g., 1543 = Samba Rice)
SSSSS = Serial/Batch ID (random)
C     = Check digit (EAN13 compliant)
```

---

## 🧪 Example

For a product like **Samba Rice**:

```text
Category: Rice => Code = 200
Product Code: 1543
Generated Serial: 09576
EAN13 Barcode: 2001543095764
```

---

## 🧠 Future Improvements

- PDF export of labels
- Barcode reprint history
- Category/product code maps stored in DB
- REST API support

---

## 🔐 License

Licensed under the MIT License.

---

## 🙋‍♂️ Author

**Developed by:** Kavindu Bandaranayake
📧 Email: kavindubandaranayakemaho@gmail.com
🌐 Website: None

---

## 🤝 Contributing

Pull requests are welcome.  
For major changes, open an issue first to discuss what you'd like to change.

---
