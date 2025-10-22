# ini utk file profil_atlet/management/commands/import_atlet.py
import csv
from django.core.management.base import BaseCommand
from profil_atlet.models import Atlet, Medali
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Import data dari athletes.csv dan medals.csv (mengambil 110 sampel atlet yg PASTI punya medali)'

    def add_arguments(self, parser):
        parser.add_argument('athletes_csv', type=str, help='Lokasi file athletes.csv (LENGKAP 5000+ baris)')
        parser.add_argument('medals_csv', type=str, help='Lokasi file medals.csv')

    def handle(self, *args, **options):
        athletes_file_path = options['athletes_csv']
        medals_file_path = options['medals_csv']
        
        # hapus data  lama
        self.stdout.write(self.style.WARNING('Membersihkan database lama...'))
        Medali.objects.all().delete()
        Atlet.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database bersih.'))

        # BUAT SEMACAM 'DAFTAR BELANAJA' UTK 110 ATLET YG PNY MEDALI (>100 data)
        self.stdout.write(f'Membaca {medals_file_path} untuk mengambil 110 atlet unik...')
        
        # pakai set() agar namanya unik (tidak duplikat)
        atlet_sample_short_names = set() 
        
        with open(medals_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                atlet_short_name = row['athlete_short_name']
                atlet_sample_short_names.add(atlet_short_name)
                
                # stop jika sudah mengumpulkan 110 nama unik
                if len(atlet_sample_short_names) >= 110:
                    break
        
        self.stdout.write(self.style.SUCCESS(f'Berhasil mendapatkan {len(atlet_sample_short_names)} atlet unik (sampel).'))

        # IMPORT PROFIL ATLET HANYA UTK 110 NAMA TSB 
        self.stdout.write(f'Mencari dan mengimpor profil 110 atlet dari {athletes_file_path}...')
        
        with open(athletes_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # cek apakah atlet ini ada di "daftar belanja" kita
                if row['short_name'] in atlet_sample_short_names:
                    try:
                        tgl_lahir = row.get('birth_date') or None
                        
                        Atlet.objects.create(
                            short_name=row['short_name'],
                            name=row['name'],
                            country=row['country'],
                            discipline=row['discipline'],
                            gender=row.get('gender') or None,
                            birth_date=tgl_lahir,
                            birth_place=row.get('birth_place') or None,
                            birth_country=row.get('birth_country') or None,
                            nationality=row['country'], # isi nationality dari country jadi nationality = country
                            is_visible=True,
                        )
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f"Atlet {row['short_name']} sudah ada. Di-skip."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error memproses atlet {row['name']}: {e}"))

        self.stdout.write(self.style.SUCCESS('Impor atlet (sampel) selesai!'))

        # IMPORT MEDALI HANYA UNTUK 110 ATLET TSB 
        self.stdout.write(f'Mengimpor data medali HANYA untuk 110 atlet terpilih...')
        
        with open(medals_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                atlet_short_name = row['athlete_short_name']
                
                # cek lagi apakah medali ini milik atlet di "daftar belanja" kita
                if atlet_short_name in atlet_sample_short_names:
                    try:
                        atlet_obj = Atlet.objects.get(short_name=atlet_short_name)
                        tanggal_medali = row['medal_date'].split(' ')[0]
                        
                        Medali.objects.create(
                            atlet=atlet_obj,
                            medal_type=row['medal_type'],
                            event=row['event'],
                            medal_date=tanggal_medali
                        )
                    # exepction
                    except Atlet.DoesNotExist:
                        # mungkin ini tidak terjadi, tapi untuk jaga-jaga
                        self.stdout.write(self.style.WARNING(f"Atlet '{atlet_short_name}' tidak ditemukan. Medali di-skip."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error memproses medali untuk {row['athlete_name']}: {e}"))
        
        self.stdout.write(self.style.SUCCESS('Semua impor (sampel) selesai!'))