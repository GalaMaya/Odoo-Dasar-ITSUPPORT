# 🎫 IT Support Ticket Module for Odoo 18

Sebuah modul Odoo kustom *full-stack* yang dirancang untuk membantu tim IT internal dalam mengelola, melacak, dan menyelesaikan tiket dukungan teknis secara efisien. Dibangun dari nol menggunakan Odoo 18, modul ini mengimplementasikan fitur *enterprise-grade* seperti otomatisasi backend, keamanan berbasis peran (RBAC), analitik dashboard, pelaporan PDF, dan integrasi API eksternal.

## ✨ Fitur Utama

- **Manajemen Tiket Lengkap**: Pembuatan, penugasan, dan pelacakan status tiket (Baru, Dikerjakan, Selesai) dengan tampilan List, Form, dan Kanban.
- **Keamanan Data (RBAC)**: 
  - **Staf IT**: Hanya dapat melihat dan mengelola tiket yang ditugaskan kepada mereka sendiri.
  - **Manager IT**: Memiliki akses penuh untuk melihat dan mengelola semua tiket di sistem.
- **Otomatisasi Cerdas**: 
  - *Computed Fields*: Menghitung durasi pengerjaan tiket secara otomatis.
  - *Backend Automation*: Auto-ubah status menjadi "Sedang Dikerjakan" dan kirim notifikasi Chatter jika judul tiket mengandung kata "URGENT".
- **Chatter & Tracking**: Terintegrasi dengan modul `mail` untuk mencatat riwayat perubahan status, komentar, dan notifikasi real-time.
- **Dashboard & Analitik**: Tampilan Graph (Grafik Batang) dan Pivot (Tabel Excel) untuk menganalisis performa staf dan durasi tiket.
- **Laporan PDF (QWeb)**: Tombol "Print" untuk men-generate dokumen PDF tiket yang rapi dan profesional untuk arsip fisik.
- **Custom Action**: Tombol "Buka Kembali" (Reopen) dengan validasi UI dan log otomatis untuk menangani tiket yang dibuka ulang.
- **Integrasi API (XML-RPC)**: Mendukung pembuatan dan pembacaan tiket secara programatik dari aplikasi eksternal (Python, monitoring tools, website).

## 🛠️ Teknologi yang Digunakan

- **Framework**: Odoo 18 (Community/Enterprise)
- **Bahasa Pemrograman**: Python 3, XML (QWeb)
- **Database**: PostgreSQL
- **Environment**: Docker, VS Code

## 📂 Struktur Modul

```text
it_support_ticket/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── ticket.py          # Logika database, computed fields, automation, dan API
├── security/
│   ├── ir.model.access.csv # Hak akses dasar (ACL)
│   ├── it_support_rules.xml # Record Rules (Keamanan data per user)
│   └── it_support_security.xml # Definisi Grup (Staf IT & Manager IT)
├── views/
│   └── ticket_views.xml   # Tampilan UI (List, Form, Kanban, Graph, Pivot)
└── reports/
    └── ticket_report.xml  # Template QWeb untuk Laporan PDF
```

## 🚀 Cara Instalasi

1. Pastikan Anda memiliki instance Odoo 18 yang berjalan (disarankan menggunakan Docker).
2. Salin folder `it_support_ticket` ke dalam direktori `custom-addons` Anda.
3. Pastikan path `custom-addons` sudah terdaftar di file konfigurasi Odoo (`odoo.conf` pada parameter `addons_path`).
4. Masuk ke Odoo sebagai Administrator, aktifkan **Developer Mode**.
5. Buka menu **Apps**, klik **Update Apps List**.
6. Cari "IT Support Ticket" dan klik **Install**.

## 💡 Cara Penggunaan

### 📊 Analitik & Dashboard
- Buka menu *IT Support > Ticket*.
- Klik ikon **Grafik** atau **Pivot** di pojok kanan atas untuk melihat statistik durasi dan performa staf IT.

### 🖨️ Cetak Laporan PDF
- Buka salah satu tiket.
- Klik tombol **🖨️ Print PDF** di bagian atas form untuk mengunduh dokumen arsip.

### 🤖 Integrasi API (XML-RPC)
Modul ini dapat dikontrol sepenuhnya dari luar Odoo menggunakan Python `xmlrpc.client`.
Contoh script untuk membuat tiket secara otomatis:
```python
import xmlrpc.client

url, db, username, password = 'http://localhost:8069', 'your_db_name', 'admin', 'admin'
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Membuat tiket baru via API
ticket_id = models.execute_kw(db, uid, password, 'it.support.ticket', 'create', [{
    'name': 'Server Down - URGENT (Via API)',
    'description': 'Dibuat otomatis oleh script monitoring.',
    'status': 'draft'
}])
print(f"Tiket dibuat dengan ID: {ticket_id}")
```
*(Catatan: Karena fitur otomatisasi aktif, tiket dengan kata "URGENT" akan otomatis berubah statusnya menjadi "Sedang Dikerjakan" saat dibuat).*

## 👨‍💻 Penulis

Dibuat oleh **Blue** (IT Specialist) sebagai demonstrasi kemampuan Full-Stack Odoo Development.

---
*Catatan: Modul ini dikembangkan dan diuji pada Odoo 18. Sintaks XML menggunakan standar terbaru (tag `<list>` dan `<chatter/>`).*