from ScraperManager import ScraperManager

if __name__ == "__main__":
    print("Welcome to PriceTrace!")

    category_select = input("Select the pc category for better results(cpu,gpu,ram,motherboard,ssd,psu):")
    users_input = input("Enter the pc part you want to see price differences in the sites:")

    manager = ScraperManager(category_select, users_input)

    print("Web scrape is in progress...")
    results = manager.run_all()

    if not results:
        print("Product not found on any site.")
    else:
        for res in results:
            print(f"{res.site}: {res.price} - {res.title}")