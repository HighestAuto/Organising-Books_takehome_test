"""A script to analyse book data."""
import pandas as pd
import altair as atr
import vl_convert as vlc


def decade_round(year: int) -> int:
    """Gets the decade the year is in"""
    return int(10 * round(year/10))


def decade_releases(df: pd):
    """Makes a chart of books released in a decade then writes a .png 
    of the chart made"""
    rounded_years = df
    rounded_years['year'] = rounded_years['year'].apply(
        lambda year: decade_round(year))
    rounded_years = rounded_years.groupby(
        rounded_years['year']).count().reset_index()

    chart = atr.Chart(rounded_years).mark_arc(color='red').encode(
        atr.Theta('title').stack(True),
        color=atr.Color('year', scale=atr.Scale(scheme='category10'))
    )
    pie = chart.mark_arc(outerRadius=120)
    text = chart.mark_text(radius=140, size=10).encode(text="year")
    chart = pie+text
    png_data = vlc.vegalite_to_png(chart.to_json(),  scale=2)

    with open("decade_releases.png", "wb") as f:
        f.write(png_data)


def top_authors(df: pd):
    """Makes a chart of the 10 most reviewed authors then writes a .png 
    of the chart made"""
    authors = df
    authors = authors.groupby('author_name').sum('ratings').reset_index()
    authors = authors.sort_values('ratings', ascending=False)
    top_rated_authors = authors.head(10)

    chart = atr.Chart(top_rated_authors).mark_bar().encode(
        atr.X('author_name').sort('-y'),
        atr.Y('ratings')
    )
    png_data = vlc.vegalite_to_png(chart.to_json(),  scale=2)
    with open("top_authors.png", "wb") as f:
        f.write(png_data)


if __name__ == "__main__":
    dataframe = pd.read_csv('data/PROCESSED_DATA.csv')
    decade_releases(dataframe)
    top_authors(dataframe)
