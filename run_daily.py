import os
from datetime import datetime
from scanner_engine import run_scanner

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    
    df = run_scanner()
    
    os.makedirs("data", exist_ok=True)
    
    file_path = f"data/{today}.csv"
    df.to_csv(file_path, index=False)
    
    print(f"Snapshot guardado: {file_path}")

if __name__ == "__main__":
    main()
