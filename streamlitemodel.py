import streamlit as st
import cv2
import keras
import numpy as np
import my_test
import subprocess

def install_system_packages():
    subprocess.call(['apt-get', 'update', '-y'])
    subprocess.call(['apt-get', 'install', '-y', '--no-install-recommends', '-q', '-o', 'Dpkg::Options::=--force-confdef', '-o', 'Dpkg::Options::=--force-confold', '-o', 'APT::Install-Suggests=0', '-o', 'APT::Install-Recommends=0', '-o', 'Debug::pkgProblemResolver=1', '-o', 'Debug::Acquire::http=true', '-o', 'Debug::pkgDPkgPM=1', '-o', 'Debug::pkgProblemResolver=1', '-o', 'Debug::pkgAcquire::http=true', '-o', 'Debug::pkgAcquire::Worker=1', '-o', 'Debug::pkgDPkgPM=1'] + open('packages.txt').read().split())


@st.cache(allow_output_mutation=True)
def my_model():
    model = keras.models.load_model("C:/Users/Meir/Downloads/model_finalyolo77-20230313T214546Z-001/model_finalyolo77")
    return model

def main2():
    install_system_packages()
    model = my_model()
    # Define the page title
    iii = cv2.imread("C:/Users/Meir/Downloads/ISRAELGARB.jpg")
    iii = cv2.cvtColor(iii, cv2.COLOR_BGR2RGB)
    #imgj = cv2.imdecode(np.fromstring(iii.read(), np.uint8), cv2.IMREAD_COLOR)
    st.image(iii)#imgj)
    #st.title("EcoVision")
    st.markdown("<h1 style='text-align: center; color: red;'>EcoVision</h1>", unsafe_allow_html=True)
    confidence_threshold = st.slider('Confidence Threshold', 0, 100, 80)
    t1 = st.slider('Confidence Threshold', 0, 100, 40)
    t1 = t1/100
    t2 = st.slider('Confidence Threshold', 0, 100, 60)
    t2 = t2/100
    image_path = st.file_uploader("Select a picture to help your planet breath (without any pressure of course)", type=["jpg", "jpeg", "png"])
    img = 0
    if image_path is not None:
        st.write("Image path :", image_path)
        img = cv2.imdecode(np.fromstring(image_path.read(), np.uint8), cv2.IMREAD_COLOR)
        st.image(img)

        my_img, my_class, my_res, img_final = my_test.main45(img, model, t1, t2)
        st.title('PREDICTED RESULTS')
        st.title(f'{len(my_img)} objects were found.')
        #st.image(img_final)
        st.image(cv2.cvtColor(img_final, cv2.COLOR_BGR2RGB))
        st.title('Display RESULTS')

        g = {
                'battery': 'ELEC_DEPOSIT',
                'biodegradable': 'BROWN_ORGANIC',
                'book': 'BLUE_PAPER_CARDBOARD_CARTONS',
                'cardboard': 'WHITE_CARDBOARD',
                'clothes': 'CLOTHING_DEPOSIT',
                'glass': 'PURPLE_GLASS',
                'lunchbox': 'ORANGE_PACK',
                'metal': 'GREY_METAL',
                'metals': 'GREY_METAL',
                'organics': 'BROWN_ORGANIC',
                'paper': 'BLUE_PAPER_CARDBOARD_CARTONS',
                'plastic': 'ORANGE_PACK',
                'wasterpaper': 'GREEN_GENERAL',
                'other': 'GREEN_GENERAL'
        }

        for i in range(len(my_img)):
            mysize = 128
            iimmgg = my_img[i]

            #taux = mysize / iimmgg.shape[0]
            #xshape = mysize#round(iimmgg.shape[0] * taux)
            #yshape = round(iimmgg.shape[1] * taux)
            ise = mysize / iimmgg.shape[1]
            iimmgg2 = cv2.resize(iimmgg, (round(iimmgg.shape[1] * ise), mysize))
            #iimmgg2 = cv2.resize(iimmgg, (xshape, yshape))
            col1, col2, col3 = st.columns(3)
            with col1:
                st.header(f"{my_class[i]}")
                st.image(iimmgg2, use_column_width=True)

            iii3 = cv2.imread("C:/Users/Meir/Downloads/recyclearrow.png")
            with col2:
                st.image(iii3, use_column_width=True)

            if my_res[i] < confidence_threshold:
                iii4 = cv2.imread(f"C:/Users/Meir/Downloads/GARBAGES/GREEN_GENERAL.png")
                ise = mysize / iii4.shape[0]
                iii4 = cv2.resize(iii4, (mysize, round(iii4.shape[1] * ise)))
                with col3:
                    st.header(f"The detection is not relevant..Please use the general garbage.")
                    st.image(iii4, use_column_width=True)
            else:
                #selected_options = st.checkbox('Is it a bottle (In a future version this question \
                                               #will be filled automatically :', ['Y', 'N'])
                selected_options = 'N'
                if selected_options == 'N':
                    iii4 = cv2.imread(f"C:/Users/Meir/Downloads/GARBAGES/{g[my_class[i]]}.png")
                    ise = mysize/iii4.shape[0]
                    iii4 = cv2.resize(iii4, (mysize, round(iii4.shape[1]*ise)))
                    with col3:
                        st.header(f"Confidence: {my_res[i]:.2f}%")
                        st.image(iii4, use_column_width=True)
                else:
                    iii4 = cv2.imread(f"C:/Users/Meir/Downloads/GARBAGES/BOTTLE_DEPOSIT.png")
                    ise = mysize / iii4.shape[0]
                    iii4 = cv2.resize(iii4, (mysize, round(iii4.shape[1] * ise)))
                    with col3:
                        st.header(f"Confidence: {my_res[i]:.2f}%")
                        st.image(iii4, use_column_width=True)



if __name__ == '__main__':
    main2()
