import streamlit as st

# Display the image in the sidebar first
st.logo("image_imdb_copy.png", size='large',icon_image="logo_golden.png",)

# Create the navigation and run it
pg = st.navigation([st.Page('advanced_filter.py', icon="🔍",title="Advanced Filter"), st.Page('plots.py',icon="📈",title="Analysis plots")])
pg.run()


