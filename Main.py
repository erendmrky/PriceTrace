from ScraperManager import ScraperManager

if __name__ == "__main__":
    print("Welcome to PriceTrace!")

    valid_categories = ["cpu", "gpu", "ram", "motherboard", "ssd", "psu"]

    while True:
        category_select = input("Select the pc category for better results(cpu,gpu,ram,motherboard,ssd,psu): ").strip().lower()
        if category_select in valid_categories:
            break
        print("Invalid input! Please enter exactly one of the valid categories.\n")

    users_input = input("Enter the pc part you want to see price differences in the sites: ").strip()

    manager = ScraperManager(category_select, users_input)

    print("Web scrape is in progress...")
    results = manager.run_all()

    for res in results:
        if res.price == 0 and res.title == "EMPTY":
            print(f"{res.site}: Not found or no exact match.")
        elif res.price == 0 and res.title == "BANNED":
            print(f"{res.site}: Access denied (Bot blocked).")
        elif res.price == 0 and res.title == "TIMEOUT":
            print(f"{res.site}: Connection timeout.")
        else:
            print(f"{res.site}: {res.price}₺ - {res.title}")