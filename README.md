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
| **Profile Atlet** | Menampilkan profil atlet Paralympic. Guest hanya melihat daftar singkat, Member dapat melihat detail dan melaporkan data, Admin mengelola seluruh profil. | Nicholas Vesakha | C,R,U,D (Admin), R (Member), R (Guest) |
| **Following** | User dapat mengikuti cabang olahraga untuk update berita/event. | Angelo Benhanan Abinaya Fuun | C: User bisa create following pada suatu cabang olahraga) R: User bisa melihat cabang olahraga apa saja yang ia follow U: User bisa mengatur priority followingnya (mengatur berita/event apa yang diprioritaskan untuk ditunjukkan) D: User bisa unfollow suatu cabang olahraga.|

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



