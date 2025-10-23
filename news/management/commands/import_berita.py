from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from news.models import Berita
import pandas as pd

class Command(BaseCommand):
    help = "Import berita from CSV sesuai model baru"

    def handle(self, *args, **kwargs):
        df = pd.read_csv("berita_final.csv")

        author = User.objects.first()  # pemilik semua data import

        for _, r in df.iterrows():
            Berita.objects.create(
                title   = r["judul"],
                content = r["isi"],
                category = "other",
                thumbnail = None,
                author  = author
            )

        self.stdout.write(self.style.SUCCESS(f"Imported {len(df)} berita"))
