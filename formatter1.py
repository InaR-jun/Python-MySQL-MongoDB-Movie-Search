from rich import print as rprint

def print_films(films):
    """
    Displays a numbered list of movies in the console.
    """
    rprint("-" * 70)
    for i, (title, year) in enumerate(films, 1):
        rprint(f"[purple]{i}.[/purple] {title.capitalize()} (Year: {year})")
    rprint("-" * 70)

def print_genres(genres):
    """
    Displays a list of genres.
    """
    rprint("\n[bold]----- List of genres -----[/bold]")
    for category_id, name in genres:
        rprint(f"{category_id}. {name.capitalize()}")

def print_popular_queries(queries):
    """
    Displays a list of popular queries.
    """
    rprint("\n[bold]----- 5 popular queries -----[/bold]")
    if not queries:
        rprint("[yellow]There are no popular queries yet.🤷[/yellow]")
        return
    for i, query in enumerate(queries, 1):
        query_id = query["_id"]
        count = query["count"]
        
        search_type = query_id.get("search_type")
        params = query_id.get("params", {})
        
        if search_type == "keyword":
            keyword = params.get("keyword")
            rprint(f"[bold]{i}.[/bold] Search by word: '[yellow]{keyword}[/yellow]' ([cyan]Frequency:[/cyan] {count})")
        elif search_type == "genre_and_year":
            genre_id = params.get("genre_id")
            start_year = params.get("start_year")
            end_year = params.get("end_year")
            rprint(f"[bold]{i}.[/bold] Search by genre ([blue]ID:[/blue] {genre_id}) from [yellow]{start_year}[/yellow] to [yellow]{end_year}[/yellow] ([cyan]Frequency:[/cyan] {count})")
        else:
            rprint(f"[bold]{i}.[/bold] Unknown request: {params} ([cyan]Frequency:[/cyan] {count})")

def print_recent_queries(queries):
    """
    Displays a list of recent queries.
    """
    rprint("\n[bold]----- 5 recent queries -----[/bold]")
    if not queries:
        rprint("[yellow]There are no recent requests yet.🤷[/yellow]")
        return
    for i, query in enumerate(queries, 1):
        timestamp = query.get("timestamp").strftime('%Y-%m-%d %H:%M:%S')
        search_type = query.get("search_type")
        params = query.get("params", {})

        if search_type == "keyword":
            keyword = params.get("keyword")
            rprint(f"[bold]{i}.[/bold] Search by word: '[yellow]{keyword}[/yellow]' ([cyan]Time:[/cyan] {timestamp})")
        elif search_type == "genre_and_year":
            genre_id = params.get("genre_id")
            start_year = params.get("start_year")
            end_year = params.get("end_year")
            rprint(f"[bold]{i}.[/bold] Search by genre ([blue]ID:[/blue] {genre_id}) from [yellow]{start_year}[/yellow] to [yellow]{end_year}[/yellow] ([cyan]Time:[/cyan] {timestamp})")
        else:
            rprint(f"[bold]{i}.[/bold] Unknown request: {params} ([cyan]Time:[/cyan] {timestamp})")