import csv
import random

# Threshold in milliseconds (30 seconds = 30,000 ms)
MIN_PLAYTIME_MS = 30000 

def load_and_clean_data(filename):
    playlist_data = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    ms_played = int(row.get('ms_played', 0))
                except ValueError:
                    ms_played = 0

                # Check if the play meets the 30-second minimum rule
                if ms_played >= MIN_PLAYTIME_MS:
                    cleaned_row = {
                        'ts': row.get('ts', '').strip(),
                        'track_name': row.get('track_name', '').strip().title(),
                        'artist_name': row.get('artist_name', '').strip().title(),
                        'type': row.get('type', '').strip().lower(),
                        'genre': row.get('genre', '').strip().title(),
                        'respondent_id': row.get('respondent_id', '').strip(),
                        'device': row.get('device', '').strip(),
                        'ms_played': ms_played
                    }
                    playlist_data.append(cleaned_row)
                    
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Check your file path.")
    
    return playlist_data

def get_top_item(data, key):
    counts = {}
    for row in data:
        item = row.get(key)
        if item:
            counts[item] = counts.get(item, 0) + 1
    if not counts:
        return "No data available", 0
    top_item = max(counts, key=counts.get)
    return top_item, counts[top_item]

def show_top_song(data):
    song, count = get_top_item(data, 'track_name')
    print(f"\n🎵 Top Song: {song} (Played {count} times for at least 30s)")

def show_top_artist(data):
    artist, count = get_top_item(data, 'artist_name')
    print(f"\n🎤 Top Artist: {artist} ({count} qualifying plays)")

def show_top_genre(data):
    genre, count = get_top_item(data, 'genre')
    print(f"\n🎧 Top Genre: {genre} ({count} qualifying plays)")

def show_minutes_listened(data):
    total_ms = sum(row['ms_played'] for row in data)
    total_minutes = total_ms / 60000
    print(f"\n⏱️ Total Minutes Listened (30s+ plays only): {total_minutes:,.2f} minutes")

def play_garthle(data):
    # Extract unique artists and sort them alphabetically
    artists = sorted(list(set(row['artist_name'] for row in data if row['artist_name'])))
    if not artists:
        print("Not enough data to start Garthle.")
        return
        
    secret_artist = random.choice(artists)
    
    print("\n🎮 Welcome to Garthle!")
    print("-" * 30)
    print("📋 Available Artists to Guess From:")
    for idx, artist in enumerate(artists, start=1):
        print(f"  {idx}. {artist}")
    print("-" * 30)
    
    attempts = 6
    
    while attempts > 0:
        guess = input(f"\nGuess the artist ({attempts} attempts left): ").strip().title()
        if guess == secret_artist:
            print(f"🎉 Correct! It was {secret_artist}!")
            return
        attempts -= 1
        if attempts > 0:
            print("❌ Incorrect! Try again.")
        
    print(f"\n😢 Game over! The secret artist was: {secret_artist}")

def show_signature_report(data):
    print("\n📊 Signature Report: Valid Plays by Device (>=30s)")
    device_counts = {}
    for row in data:
        dev = row.get('device', 'Unknown')
        device_counts[dev] = device_counts.get(dev, 0) + 1
        
    for device, count in device_counts.items():
        print(f" - {device}: {count} plays")

def main():
    filename = "listening_survey.csv" 
    data = load_and_clean_data(filename)
    
    if not data:
        print("No valid data loaded after applying the 30-second filter.")
        return

    while True:
        print("\n==============================")
        print("   TA TABLE PLAYLIST MENU     ")
        print("==============================")
        print("1. Top Song")
        print("2. Top Artist")
        print("3. Top Genre")
        print("4. Minutes Listened")
        print("5. Garthle (Guess-the-Artist)")
        print("6. Signature Report")
        print("7. Exit")
        
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == '1':
            show_top_song(data)
        elif choice == '2':
            show_top_artist(data)
        elif choice == '3':
            show_top_genre(data)
        elif choice == '4':
            show_minutes_listened(data)
        elif choice == '5':
            play_garthle(data)
        elif choice == '6':
            show_signature_report(data)
        elif choice == '7':
            print("Exiting playlist application. Goodbye, Roll Tide, Roll!")
            break
        else:
            print("Invalid selection. Please choose options 1-7.")

if __name__ == "__main__":
    main()

















































