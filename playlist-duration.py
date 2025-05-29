#!/usr/bin/env python3
"""
YouTube Playlist Duration Calculator - Versione Semplificata
Calcola la durata totale di una playlist YouTube e tempo necessario per guardarla
"""

import subprocess
import json
import sys
from datetime import timedelta

class YouTubePlaylistCalculator:
    def __init__(self):
        self.videos = []
        self.total_duration = 0
        
    def check_ytdlp_installed(self) -> bool:
        """Controlla se yt-dlp è installato"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def extract_playlist_info(self, url: str) -> bool:
        """Estrae informazioni dalla playlist usando yt-dlp"""
        try:
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--dump-json',
                '--no-warnings',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                # Prova metodo alternativo per video singoli
                return self.extract_single_video_info(url)
            
            lines = result.stdout.strip().split('\n')
            self.videos = []
            
            for line in lines:
                if line.strip():
                    try:
                        video_info = json.loads(line)
                        if 'duration' in video_info and video_info['duration']:
                            self.videos.append(video_info['duration'])
                    except json.JSONDecodeError:
                        continue
            
            return len(self.videos) > 0
            
        except Exception:
            return self.extract_single_video_info(url)
    
    def extract_single_video_info(self, url: str) -> bool:
        """Estrae info da video singolo"""
        try:
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-download',
                '--no-warnings',
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return False
            
            video_info = json.loads(result.stdout.strip())
            if 'duration' in video_info and video_info['duration']:
                self.videos = [video_info['duration']]
                return True
            
            return False
            
        except Exception:
            return False
    
    def calculate_total_duration(self) -> int:
        """Calcola durata totale in secondi"""
        self.total_duration = sum(self.videos)
        return self.total_duration
    
    def format_duration(self, seconds: int) -> str:
        """Formatta durata in formato leggibile"""
        if seconds == 0:
            return "0 secondi"
        
        td = timedelta(seconds=seconds)
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days} giorni")
        if hours > 0:
            parts.append(f"{hours} ore")
        if minutes > 0:
            parts.append(f"{minutes} minuti")
        if secs > 0:
            parts.append(f"{secs} secondi")
        
        return ", ".join(parts) if parts else "0 secondi"
    
    def calculate_viewing_days(self, hours_per_day: int) -> float:
        """Calcola giorni necessari guardando X ore al giorno"""
        total_hours = self.total_duration / 3600
        return total_hours / hours_per_day if hours_per_day > 0 else 0
    
    def process_url(self, url: str) -> bool:
        """Processa URL e mostra risultati"""
        # Verifica yt-dlp
        if not self.check_ytdlp_installed():
            print("ERRORE: yt-dlp non installato")
            print("Installa con: pip install yt-dlp")
            return False
        
        print("Analizzando...")
        
        # Estrai informazioni
        if not self.extract_playlist_info(url):
            print("ERRORE: Impossibile estrarre informazioni")
            return False
        
        # Calcola durata
        self.calculate_total_duration()
        
        # Mostra risultati
        self.show_results()
        return True
    
    def show_results(self):
        """Mostra risultati essenziali"""
        print(f"\nNumero video: {len(self.videos)}")
        print(f"Durata totale: {self.format_duration(self.total_duration)}")
        
        print(f"\nTempo necessario:")
        print(f"1 ora/giorno: {self.calculate_viewing_days(1):.1f} giorni")
        print(f"2 ore/giorno: {self.calculate_viewing_days(2):.1f} giorni") 
        print(f"3 ore/giorno: {self.calculate_viewing_days(3):.1f} giorni \n")

def main():
    url = input("Inserisci URL playlist/video YouTube: ").strip()
    
    if not url:
        print("ERRORE: URL vuoto")
        return
    
    calculator = YouTubePlaylistCalculator()
    calculator.process_url(url)

if __name__ == "__main__":
    main()
