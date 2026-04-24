from load_files import process_files, load_to_db

def main():
    df1, df2 = process_files()
    load_to_db(df1, df2)

if __name__ == "__main__":
    main()