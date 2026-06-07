from ScraperManager import ScraperManager

if __name__ == "__main__":
    print(r"""
    ==================================================
       _____         _            _______                     
      |  __ \       (_)          |__   __|                    
      | |__) | __ _  _   ___  ___   | | _ __  __ _   ___  ___ 
      |  ___/ '__| || | / __|/ _ \  | || '__|/ _` | / __|/ _ \
      | |   | |  | || || (__|  __/  | || |  | (_| || (__|  __/
      |_|   |_|  |_||_| \___|\___|  |_||_|   \__,_| \___|\___|
    ==================================================
    """)

    valid_categories = ["cpu", "gpu", "ram", "motherboard", "ssd", "psu"]

    while True:
        category_select = input(
            "Select the pc category for better results(cpu,gpu,ram,motherboard,ssd,psu): ").strip().lower()
        if category_select in valid_categories:
            break
        print("Invalid input! Please enter exactly one of the valid categories.\n")

    users_input = input("Enter the pc part you want to see price differences in the sites: ").strip()

    manager = ScraperManager(category_select, users_input)

    print("\nWeb scrape is in progress...")
    results = manager.run_all()

    for res in results:
        if res.price == 0 and res.title == "EMPTY":
            print(f"{res.site}: Not found or no exact match.")
        elif res.price == 0 and res.title == "BANNED":
            print(f"{res.site}: Access denied (Bot blocked).")
        elif res.price == 0 and res.title == "TIMEOUT":
            print(f"{res.site}: Connection timeout.")
        else:
            print(f"{res.site}: {res.price}₺ - {res.title} product link: {res.link}")

    valid_results = [res for res in results if res.price > 0]

    if valid_results:
        cheapest = min(valid_results, key=lambda x: x.price)

        print("\n--------------------------------------------------")
        print(f"The Site with the Lowest Prices: {cheapest.site}")
        print(f"Product Name: {cheapest.title}")
        print(f"Price: {cheapest.price}₺")
        print(f"Product Link: {cheapest.link}")
        print("--------------------------------------------------")
    else:
        print("\n[!] No valid price was found for comparison.")