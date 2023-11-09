import streamlit as st
from utils import get_caption, generate_titles


def main():
    st.set_page_config(page_title="Image group title", page_icon="\U0001F642")
    st.header("Title ideas for a group of images.")
    images = st.file_uploader(
        "Upload up to four images:", type="jpg", accept_multiple_files=True
    )

    all_captions = ""
    all_img_names = []

    for img in images:
        if img:
            # get the image bytes
            img_bytes = img.getvalue()
            img_name = img.name
            img_stem = img.name.split(".")[0]
            all_img_names.append(img_name)

            # save the image locally
            with open(f"./img/{img_name}", "wb") as f:
                f.write(img_bytes)

            # step 1: get caption from image
            caption = get_caption(f"./img/{img_name}")
            if all_captions:
                all_captions = all_captions + ", " + caption
            else:
                all_captions = caption

    cols = st.columns(4)
    for i, img_name in enumerate(all_img_names):
        cols[i].image(f"./img/{img_name}")

    print(all_captions)
    with st.expander("Image Captions"):
        st.write(all_captions)

    if len(images) > 0:
        # create a few title ideas using GPT
        titles = generate_titles(all_captions)
        print(titles)

        with st.expander("Title Ideas"):
            st.write(titles)


if __name__ == "__main__":
    main()
