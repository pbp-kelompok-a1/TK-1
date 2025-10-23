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
| **Berita** | Admin dapat membuat, mengedit, dan menghapus berita. User terautentikasi dapat membaca & memberi komentar pada berita tersebut. user tidak terutentikasi hanya dapat membaca berita| Delila Isrina Aroyo |  👤_Guest_: Read Only <br> 👤✅ _Member_: R <br> 👑 _Admin_: C-R-U-D |
| **Comment** | User tidak terautentikasi hanya dapat membaca komentar. User terautentikasi dapat membuat, mengedit, dan menghapus komentar sendiri. Admin dapat membuat dan mengedit komentar serta memiliki akses untuk menghapus komentar orang lain. | Ilham Shahputra Hasim | 👤_Guest_: Read Only <br> 👤✅ _Member_: C-R-U-D(own comment) <br> 👑 _Admin_: C-U(own comment) and R-D(all comment)  |
| **Event & Jadwal** | Modul Event & Jadwal berfungsi sebagai pusat informasi event dengan pemisahan tegas antara konten umum dan pribadi. Inti dari modul ini adalah menginformasikan Event Global (acara resmi, pengumuman umum, atau kegiatan situs yang dikelola Administrator) dan memungkinkan Event Pribadi (agenda, jadwal latihan, atau sparring yang dibuat oleh pengguna terautentikasi untuk keperluan mereka sendiri). Pengguna yang tidak terautentikasi (guest) hanya bisa melihat informasi dan tidak bisa menambahkan event pribadi. | Ahmad Anggara Bayuadji Prawirosoenoto | 👤 _Guest_: Read Only <br> 👤✅ _Member_: C-R-U-D <br> 👑 _Admin_: C-R-U-D|
| **Profil Atlet** | Modul Profil Atlet berfungsi sebagai ensiklopedia digital mengenai para atlet Paralimpiade. Database-nya diisi secara efisien melalui impor data massal dari file CSV (_dataset_ Kaggle) untuk memastikan kelengkapan data. Modul ini menerapkan sistem hak akses berjenjang yang membedakan konten berdasarkan status _login_ pengguna: 👤 _Guest_ (Pengunjung Biasa), yaitu pengguna yang tidak _login_ sama sekali. Mereka hanya bisa membaca (_Read_) daftar nama atlet (_name_), negara asal (_country_), dan cabang olahraga (_discipline_) secara umum. Mereka tidak bisa melihat detail lengkap, membuat, mengedit, atau menghapus profil. 👤✅ _Member_ (Pengguna Terautentikasi), yaitu pengguna yang sudah mendaftar dan _login_. Hak akses mereka meningkat menjadi bisa membaca (_Read_) profil atlet secara lengkap dan mendetail, seperti _gender_, _birth_date_, _birth_place_, _birth_country_, _nationality_, bahkan _medal_type_ (Emas, Perak, Perunggu), _event_ (Contoh: Men's 100m Freestyle S5), _medal_date_ (Tahun atau tanggal medali diraih). Namun, mereka tetap tidak bisa membuat profil baru, mengedit data, atau menghapusnya. 👑 _Admin_ (_Administrator_), yaitu pengelola situs dengan hak akses tertinggi. Admin memiliki kontrol penuh. Mereka bisa Membuat (_Create_) profil atlet baru, Membaca (_Read_) semua data tanpa batasan, Mengedit (_Update_) semua informasi profil termasuk status visibilitas, dan Menghapus (_Delete_) profil dari _database_. Fitur visibilitas diatur agar admin dapat menyembunyikan sementara profil atlet dari publik, misalnya saat datanya belum lengkap atau perlu diverifikasi, tanpa harus menghapusnya secara permanen. | Nicholas Vesakha | 👤 _Guest_: R (_Read-Only_, Terbatas) <br> 👤✅ _Member_: R (_Read-Only_, Penuh) <br> 👑 _Admin_ (_Administrator_): C-R-U-D (Penuh) |
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
- **Link Desain**: https://www.figma.com/design/yqei3c8chnYDVT8bl7F4dD/Design-Web-A1?node-id=28-3&t=T5QoflADc6s3ku5s-1 












