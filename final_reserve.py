import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

st.title("Get to know Skyscrapers around the World in 2021!")
st.header("Welcome to my page!")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Search Skyscrapers", "Skyscrapers Year by Year", "Skyscraper Builder!", "Data Insights"])
skyscrapers_file = "Skyscrapers2021.csv"


def read_csv(skyscrapers_file): #function to read csv file and pop the last column
        df = pd.read_csv(skyscrapers_file)
        df.pop("Link")
        return df


def create_composite(fundament, middle, top): #function to create composite pictures of buit skyscrapers
    # Open the image files and combine them into a single image
    image1 = Image.open(top)
    image2 = Image.open(middle)
    image3 = Image.open(fundament)
    composite = Image.new('RGB', (image1.width, image1.height + image2.height + image3.height))
    composite.paste(image1, (0, 0))
    composite.paste(image2, (0, image1.height))
    composite.paste(image3, (0, image1.height + image2.height))
    return composite


def get_total_height(fundament, middle, top): #function that returns a height of a built skyscraper by combining the assigned values for fundament, middle and top of the skyscraper
    # Assign height values to each fundament, middle, and top
    fundament_heights = {
        "fundament1": 100,
        "fundament2": 100,
        "fundament3": 100,
    }
    middle_heights = {
        "middle1": 300,
        "middle2": 250,
        "middle3": 200,
    }
    top_heights = {
        "top1": 400,
        "top2": 300,
        "top3": 200,
    }

    # Look up the selected options' height values
    fundament_height = fundament_heights[fundament]
    middle_height = middle_heights[middle]
    top_height = top_heights[top]

    # Calculate the total height
    total_height = fundament_height + middle_height + top_height
    return total_height


def rank_total_height(total_height): #function to rank the created skyscraper prototype by the user
    if total_height > 750:
        return 2
    elif 700 < total_height <= 750:
        return 3
    elif 650 < total_height <= 700:
        return 4
    elif 600 < total_height <= 650:
        return 5
    elif 550 < total_height <= 600:
        return 6
    elif 500 < total_height <= 550:
        return 7
    else:
        return 8


with tab1: #About the website
    st.header("Home")
    intro = """
Learn interesting facts about the skyscrapers around the World and have some fun while you are at it! Our website offers a variety of tools to improve your knowledge about skyscrapers. Firstly, you are able to find a skyscraper that interests you simply by typing a letter in its Name or in the City it's located. If you want to view skyscrapers built before or after a certain date, or over a certain number of floors - our website would help you as well!

Next you are welcome to explore how the geography of skyscrapers has changed over the years by using an interactive map with a slider. After an extensive data analysis, you are welcome to have some fun in Skyscraper Builder! page of our website. There you are able to build a prototype of a skyscraper using exisitng parts and then viewing its height. Finally, interesting data patterns found through our research are in Data Insights section of our website and provide an important bottom line for the whole project.
"""
    st.write(intro, markdown=True)
    st.image("sky_intro.jpg", width=700)

with tab2: #Skyscraper Search Tab
    df = read_csv(skyscrapers_file)
    column = st.sidebar.radio("Select a criteria to filter by:", ['Name', 'City', 'Full Address', 'Latitude', 'Longitude', 'Number of Floors', 'Year of Completion'])
    if column in ["Name", "City", "Full Address"]: # text inputs for these criteria to allow a user to search the datafile by letters found in these columns
        input_str = st.sidebar.text_input(f"Enter a word to search for in the '{column}' column:")
        search_button = st.sidebar.button("Search")
        if search_button:
            filtered_df = df[df[column].str.contains(input_str, case=False)]
            st.dataframe(filtered_df, width=None)
    elif column in ["Latitude", "Longitude", "Number of Floors"]: #numeric input for these criteria
        input_value = st.sidebar.number_input(f"Enter a value to search for in the '{column}' column:")
        over_below = st.sidebar.radio("Search for data before or after the entered value?", ["Over", "Below"])# option to sort resulting data either Over or Below inputted value
        search_button = st.sidebar.button("Search")
        if search_button:
            if over_below == "Below":
                filtered_df = df[df[column] < input_value]
            else:
                filtered_df = df[df[column] > input_value]
            st.dataframe(filtered_df, width=None)
    elif column in ["Year of Completion"]:
        input_value = st.sidebar.number_input(f"Enter a value to search for in the '{column}' column:")
        before_after = st.sidebar.radio("Search for data before or after the entered value?", ["Before", "After"]) #option to sort resulting data either Before or After inputted value
        search_button = st.sidebar.button("Search")
        if search_button:
            if before_after == "Before":
                filtered_df = df[df[column] < input_value]
            else:
                filtered_df = df[df[column] > input_value]
                st.dataframe(filtered_df, width=None)
    else:
        search_button = st.sidebar.button("Search")
        if search_button:
            filtered_df = df[df[column].notnull()]
            st.dataframe(filtered_df, width=None)


with tab3: # Map of Skyscrapers built in the World year-by-year
    st.text("How did geography of skyscrapers change over the years?")
    df = pd.read_csv(skyscrapers_file)
    df2 = df[["City", "Latitude", "Longitude"]]
    myList = list(df2.itertuples(index=False, name=None))
    df3 = pd.DataFrame(myList, columns=["City", "lat", "lon"])
    st.title("Locations of the World's Tallest Skyscrapers")

    dates = df['Year of Completion']
    dates = sorted(dates)
    min_date = dates[0]
    max_date = dates[-1]
    slider = st.slider("Select a date:", min_value=min_date, max_value=max_date)
    selected_df = df3[df['Year of Completion'] <= slider] # connects df3 and Year of Completion slider to creare an interactive application
    st.map(selected_df[["lat", "lon"]])
    st.write(f"Number of skyscrapers built: {len(selected_df)}")

with tab4: #Skyscraper builder application
    fundaments = ["builder_images/fundament1.png","builder_images/fundament2.png","builder_images/fundament3.png"]
    middles = ["builder_images/middle1.png","builder_images/middle2.png","builder_images/middle3.png"]
    tops = ["builder_images/top1.png","builder_images/top2.png","builder_images/top3.png"]

# Create lists of image names without the extension
    fundament_names = [f.split("/")[-1].split(".")[0] for f in fundaments]
    middle_names = [m.split("/")[-1].split(".")[0] for m in middles]
    top_names = [t.split("/")[-1].split(".")[0] for t in tops]

    st.title('Skyscraper Prototype Builder')
    st.image("builder_images/builder_menu.png", width=700)

    # Use the image names as the options in the selectboxes
    selected_fundament_name = st.selectbox('Select a fundament', fundament_names)
    selected_middle_name = st.selectbox('Select a middle', middle_names)
    selected_top_name = st.selectbox('Select a top', top_names)
    # Find the corresponding image files based on the selected image names
    selected_fundament_file = [f for f in fundaments if f.split("/")[-1].split(".")[0] == selected_fundament_name][0]
    selected_middle_file = [m for m in middles if m.split("/")[-1].split(".")[0] == selected_middle_name][0]
    selected_top_file = [t for t in tops if t.split("/")[-1].split(".")[0] == selected_top_name][0]

    # Display the selected image files on the canvas
    image1 = Image.open(selected_fundament_file)
    image2 = Image.open(selected_middle_file)
    image3 = Image.open(selected_top_file)
    st.image(image1, width=200, caption='Fundament')
    st.image(image2, width=200, caption='Middle')
    st.image(image3, width=200, caption='Top')

    if st.button('Create Composite'):
        composite = create_composite(selected_fundament_file, selected_middle_file, selected_top_file)
        st.image(composite, caption='Composite')
        total_height = get_total_height(selected_fundament_name, selected_middle_name, selected_top_name)
        rank = rank_total_height(total_height)
        st.text(f"Total Height in meters: {total_height}")
        st.text(f"The rank of your prototype: {rank}nd in the World!")



with tab5:
    st.set_option('deprecation.showPyplotGlobalUse', False) #command to disable warnings when displaying plots in streamlit
    st.title("Year of Completion vs Skyscrapers Built")
    df = pd.read_csv(skyscrapers_file)
    df = df[df["Year of Completion"].notnull() & df["Number of Floors"].notnull()]
    df_grouped = df.groupby("Year of Completion").count()
    years = df_grouped.index.tolist()
    num_floors = df_grouped["Number of Floors"].tolist()
    plt.bar(years, num_floors)
    plt.xlabel("Year of Completion")
    plt.ylabel("Number of Skyscrapers Built")
    st.pyplot()



    st.title("Year of Completion vs Change in Number of Floors")
    df = pd.read_csv(skyscrapers_file)
    df = df[df["Year of Completion"].notnull() & df["Number of Floors"].notnull()]
    df_grouped = df.groupby("Year of Completion").mean()
    years = df_grouped.index.tolist()
    num_floors = df_grouped["Number of Floors"].tolist()
    diff = [num_floors[i] - num_floors[i-1] for i in range(1, len(num_floors))]
    plt.barh(years[1:], diff, color=["green" if x > 0 else "red" for x in diff])
    plt.xlabel("Change in Number of Floors")
    plt.ylabel("Year of Completion")
    st.pyplot()

    st.title("Materials that are used in Construction of Skyscrapers")
    df = pd.read_csv(skyscrapers_file)
    materials = df['Materials']
    material_counts = materials.value_counts()
    labels = material_counts.index
    sizes = material_counts.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    st.pyplot()

    st.title("Functions of the current Skyscrapers")
    df = pd.read_csv(skyscrapers_file)
    function = df['Function']
    function_counts = function.value_counts()
    labels = function_counts.index
    sizes = function_counts.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    st.pyplot()
