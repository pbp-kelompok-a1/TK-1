# ParaWorld 🌟

**"Celebrating achievements, sharing stories, and connecting the world of Paralympic sports."**

ParaWorld adalah aplikasi berbasis web yang menghadirkan informasi seputar Paralympic Games internasional: mulai dari profil atlet dunia, berita terbaru, jadwal event, hingga ruang diskusi komunitas. Aplikasi ini bertujuan untuk memperluas pengetahuan masyarakat tentang olahraga difabel sekaligus menjadi wadah apresiasi terhadap perjuangan dan prestasi para atlet. Dengan ParaWorld, pengguna dapat mengikuti perkembangan cabang olahraga Paralympic, menemukan kisah inspiratif dari atlet, serta bergabung dalam komunitas global untuk mendukung gerakan inklusif dalam olahraga.

---

## 📅 Fitur Unggulan

- 🌍 **Berita Global**: Update berita internasional tentang Paralympic Games, hasil pertandingan, dan tren olahraga difabel di seluruh dunia.  
- 🏅 **Profil Atlet Dunia**: Informasi lengkap tentang atlet dari berbagai negara: biodata, cabang olahraga, prestasi, hingga riwayat medali.  
- 📆 **Event & Jadwal**: Kalender pertandingan Paralympic, detail cabang olahraga, serta lokasi penyelenggaraan event global.  
- 💬 **Forum Komunitas**: Wadah bagi pengguna dari berbagai negara untuk berdiskusi, berbagi opini, dan saling memberi dukungan kepada atlet Paralympic.  
- ⭐ **Bookmark & Dukungan**: Simpan atlet atau berita favorit, serta beri dukungan dengan komentar atau tanda like.

---

## 📚 Modul & Deskripsi

| Modul | Deskripsi | Developer | CRUD |
|-------|-----------|-----------|------|
| **Berita** | Admin dapat membuat, mengedit, dan menghapus berita. User dapat membaca & memberi komentar. | Delila Isrina Aroyo | Admin: C,R,U,D; User: R,C |
| **Comment** | User terautentikasi dapat membuat, mengedit, dan menghapus komentar sendiri. Admin dapat menghapus komentar orang lain. | Ilham Shahputra Hasim | C,R,U,D (sesuai role) |
| **Event & Jadwal** | Admin mengelola event global. User terautentikasi dapat menambahkan dan mengelola event pribadi. | Ahmad Anggara Bayuadji Prawirosoenoto | C,R,U,D (sesuai role) |
| **Profil Atlet** | Modul Profil Atlet berfungsi sebagai ensiklopedia digital mengenai para atlet Paralimpiade. Database-nya diisi secara efisien melalui impor data massal dari file CSV (dataset Kaggle) untuk memastikan kelengkapan data. Modul ini menerapkan sistem hak akses berjenjang yang membedakan konten berdasarkan status login pengguna: 👤 Guest (Pengunjung Biasa), yaitu pengguna yang tidak login sama sekali. Mereka hanya bisa membaca (Read) daftar nama atlet (name), negara asal (country), dan cabang olahraga (discipline) secara umum. Mereka tidak bisa melihat detail lengkap, membuat, mengedit, atau menghapus profil. 👤✅ Member (Pengguna Terautentikasi), yaitu pengguna yang sudah mendaftar dan login. Hak akses mereka meningkat menjadi bisa membaca (Read) profil atlet secara lengkap dan mendetail, seperti gender, birth_date, birth_place, birth_country, nationality, bahkan medal_type (Emas, Perak, Perunggu), event (Contoh: Men's 100m Freestyle S5), medal_date (Tahun atau tanggal medali diraih). Namun, mereka tetap tidak bisa membuat profil baru, mengedit data, atau menghapusnya. 👑 Admin (Administrator), yaitu pengelola situs dengan hak akses tertinggi. Admin memiliki kontrol penuh. Mereka bisa Membuat (Create) profil atlet baru, Membaca (Read) semua data tanpa batasan, Mengedit (Update) semua informasi profil termasuk status visibilitas, dan Menghapus (Delete) profil dari database. Fitur visibilitas diatur agar admin dapat menyembunyikan sementara profil atlet dari publik, misalnya saat datanya belum lengkap atau perlu diverifikasi, tanpa harus menghapusnya secara permanen. | Nicholas Vesakha | 👤 Guest: R (Read-Only, Terbatas), 👤✅ Member: R (Read-Only, Penuh), 👑 Admin (Administrator): CRUD: C-R-U-D (Penuh) |
| **Following** | User dapat mengikuti cabang olahraga untuk update berita/event. | Angelo Benhanan Abinaya Fuun | <ul><li>C: User bisa create following pada suatu cabang olahraga)<li>R: User bisa melihat cabang olahraga apa saja yang ia follow<li>U: User bisa mengatur priority followingnya (mengatur berita/event apa yang diprioritaskan untuk ditunjukkan)<li>D: User bisa unfollow suatu cabang olahraga.|

---

## 🕵️ Role / Peran Pengguna

| Role | Hak Akses |
|------|-----------|
| **Admin** | Mengelola semua data dan konten: berita, komentar, profil atlet, event. CRUD penuh. |
| **User Terautentikasi (Member)** | Mengakses detail atlet & berita, memberi komentar, bookmark, membuat & membalas forum, menandai event favorit. |
| **User Tidak Terautentikasi (Guest)** | Melihat daftar atlet, berita, event, dan forum (read-only). Tidak bisa memberi komentar, membuat topik, atau melakukan bookmark. |

---

## 👥 Anggota Kelompok A01

| No | NPM | Nama |
|----|-----|------|
| 1 | 2406495514 | Ahmad Anggara Bayuadji Prawirosoenoto |
| 2 | 2406405374 | Delila Isrina Aroyo |
| 3 | 2406495804 | Nicholas Vesakha |
| 4 | 2406495432 | Angelo Benhanan Abinaya Fuun |
| 5 | 2406401193 | Ilham Shahputra Hasim |

---

## 🔗 Sumber Dataset

- [Paralympics 2024 Dataset (Kaggle)](https://www.kaggle.com/datasets/jaseemck/paralympics-2024/data)  
- [Tokyo 2020 Paralympics Dataset (Kaggle)](https://www.kaggle.com/datasets/piterfm/tokyo-2020-paralympics)  

---

## 🌐 Tautan Deployment & Desain

- **Deployment PWS**: [Link Deployment](#)  
- **Link Desain**: [Link Desain](#)  






