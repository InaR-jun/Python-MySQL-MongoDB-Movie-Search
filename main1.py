import sys
from mysql_connector1 import search_by_keyword, search_by_genre_and_years, get_all_genres, get_min_max_years, check_exact_title_match
from log_writer1 import log_search_query
from log_stats1 import get_popular_queries, get_recent_queries
from formatter1 import print_films, print_genres, print_popular_queries, print_recent_queries
from rich import print as rprint 


def handle_navigation(page):
    """
    Handles user input for navigating through search results pages.
    """
    rprint("\n[bold]🗺️ Navigation:[/bold] 1️⃣ - previous, 2️⃣ - next, 3️⃣ - exit")
    choice = input("Please select: ")
    
    if choice == "3":
        return page, True  
    elif choice == "1":
        if page > 1:
            page -= 1
        else:
            rprint("[yellow]You're already here, on the first page😉[/yellow]")
        return page, False
    elif choice == "2":
        page += 1
        return page, False
    else:
        rprint("[bold red]Incorrect entry🤨.[/bold red]\nTry again, you can do it!👀")
        return page, False
        

def search_by_keyword_flow():
    """
    Keyword search.
    """
    keyword = input("\nVery good!👍\nNow, please enter a part of a film's title to search: ").strip()
    if not keyword:
        rprint("[bold red]Oops![/bold red] It looks like you forgot to enter a keyword. The search field cannot be empty. 😅\nPlease, try again")
        return

    is_exact_match = check_exact_title_match(keyword.upper())
    
    page = 1
    while True:
        offset = (page - 1) * 10
        films = search_by_keyword(keyword, offset=offset)

        if not films:
            rprint("[red]I'm so sorry, I couldn't find a film with that content.😢[/red] \nBut don't give up! We'll find something for you, just try again!🔍")
            break
        
        rprint(f"\n[bold green] ----- Search results for '[yellow]{keyword}[/yellow]' (page [yellow]{page}[/yellow]) ----- [/bold green]")
        print_films(films)

        log_search_query(
            search_type="keyword",
            params={"keyword": keyword},
            results_count=len(films)
        )

        has_next_page = len(films) == 10

        if films and not has_next_page:
            rprint("[bold green]That's all! ✅[/bold green]")
            rprint("[red]Unfortunately there are no more results for this search.😔[/red]")
            rprint("[yellow]Please try again or take another search!💡[/yellow]")
            break 
        
        page, should_exit = handle_navigation(page)
        if should_exit:
            break


def search_by_genre_and_year_flow():
    """
    Search by genre and year.
    """
    genres = get_all_genres()
    print_genres(genres)

    genre_phrases = {
        1: "🎞️ Action: Prepare for epic explosions! 💥",
        2: "🎞️ Animation: The best kind of cartoon therapy. 📺",
        3: "🎞️ Children: Let's find something the kids will like. Or you will. 😉",
        4: "🎞️ Classics: Old school, but still cool. 🕺",
        5: "🎞️ Comedy: Laughing is the best medicine! 😂",
        6: "🎞️ Documentary: Time to get smart! 🤓",
        7: "🎞️ Drama: Get your emotions ready. 😭",
        8: "🎞️ Family: Let's keep everyone happy. Good luck! 🙏",
        9: "🎞️ Foreign: Time for a movie vacation. ✈️",
        10: "🎞️ Games: It's like playing a game, but with less buttons. 🎮",
        11: "🎞️ Horror: Is that a noise I hear? 😱",
        12: "🎞️ Music: Let the soundtrack be your guide. 🎶",
        13: "🎞️ New: Let's see what's fresh! 🆕",
        14: "🎞️ Sci-fi: Beam me up, movie night! 🤖",
        15: "🎞️ Sports: Go, team, go! 🏈",
        16: "🎞️ Travel: Let's explore the world from the couch. 🌎"
    }
    
    try:
        while True:
            genre_id_input = input("\nPlease enter the genre number➡️ : ")
            if genre_id_input.isdigit() and 1 <= int(genre_id_input) <= 16:
                genre_id = int(genre_id_input)
                rprint(f"\n[bold]{genre_phrases[genre_id]}[/bold]")
                break
            else:
                rprint("[bold red]That's not a valid genre number. 🙈[/bold red]\n[yellow]Please enter a number between 1 and 16.[/yellow]")
                rprint("[green]Let's try again!🔍[/green]")

        min_year, max_year = get_min_max_years()
        rprint(f"\n[bold blue]Film release years:[/bold blue] from [yellow]{min_year}[/yellow] to [yellow]{max_year}[/yellow]\n")
        
        while True:
            start_year_input = input("Please enter the starting year📅: ")
            if start_year_input.isdigit() and min_year <= int(start_year_input) <= max_year:
                start_year = int(start_year_input)
                break
            else:
                rprint(f"[bold red]That's not a valid starting year. 🙈[/bold red]\n[yellow]Please enter a number between {min_year} and {max_year}.[/yellow]")
                rprint("[green]Let's try again!🔍[/green]")

        while True:
            end_year_input = input("Please enter the end year📅: ")
            if end_year_input.isdigit() and min_year <= int(end_year_input) <= max_year and int(end_year_input) >= start_year:
                end_year = int(end_year_input)
                break
            else:
                rprint(f"[bold red]That's not a valid ending year. 🙈[/bold red]\n[yellow]Please enter a number between {min_year} and {max_year}.[/yellow]")
                rprint("[green]Let's try again!🔍[/green]")

        rprint("\n[bold green]Excellent choice!👏[/bold green] \n[italic]Let's find some great films for you🌟 🎬[/italic]")
    except ValueError:
        rprint("[red]\nUnfortunately, the input is incorrect🥺.[/red] \n[yellow]Only numbers are allowed.1️⃣, 2️⃣, 3️⃣ \nPlease try again![/yellow]")
        return

    page = 1
    while True:
        offset = (page - 1) * 10
        films = search_by_genre_and_years(genre_id, start_year, end_year, offset=offset)

        rprint(f"\n[bold green] ----- Search results (page [yellow]{page}[/yellow]) ----- [/bold green]")
        print_films(films)

        log_search_query(
            search_type="genre_and_year",
            params={"genre_id": genre_id, "start_year": start_year, "end_year": end_year},
            results_count=len(films)
        )
        has_next_page = len(films) == 10

        if not has_next_page:
            rprint("[bold green]That's all! ✅[/bold green]")
            rprint("[red]Unfortunately there are no more results for this search.😔[/red]")
            rprint("[yellow]Please try again or take another search!💡[/yellow]")
            break 
            
        page, should_exit = handle_navigation(page)
        if should_exit:
            break


def show_statistics():
    """
    Displays statistics on search queries.
    """
    popular_queries = get_popular_queries()
    print_popular_queries(popular_queries)

    recent_queries = get_recent_queries()
    print_recent_queries(recent_queries)


def main_menu():
    """
    The main menu of the application.
    """
    while True:
        rprint("\n[bold blue]" + "="*70 + "[/bold blue]")
        rprint("[bold yellow]Welcome to Movie Explorer - Your Personal Film Finder!🎬 ✨[/bold yellow]")
        rprint("[italic green]Let's find a movie you'll love or discover something new together!🍿 🎥[/italic green]")
        rprint("[bold blue]" + "="*70 + "[/bold blue]\n")
        
        rprint("[bold]What would you like to do❓ [/bold]\n")
        rprint("1️⃣ Search by keyword📝")
        rprint("2️⃣ Search by genre and year🎬📅")
        rprint("3️⃣ Show search statistics📊")
        rprint("4️⃣ Exit🔚\n")

        choice = input("Please enter your choice✏️ :  ")

        if choice == "1":
            search_by_keyword_flow()
        elif choice == "2":
            search_by_genre_and_year_flow()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            rprint("\n[bold green]Thank you for using Movie Explorer!🙏[/bold green]")
            rprint("[italic][blue]Hope you found the movie you were looking for. See you next time!👋[/italic][/blue]\n")
            sys.exit(0)
        else:
            rprint("[bold red]\nOops! That’s not a valid choice.🙈[/bold red]\nPlease try again.")


if __name__ == "__main__":
    main_menu()