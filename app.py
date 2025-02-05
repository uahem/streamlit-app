import streamlit as st
from PIL import Image
import base64


# Funktion för att konvertera bild till base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def format_number(number):
    return f"{number:,}".replace(",", " ")

# Funktion för att ändra storlek på bild
def resize_image(image_path, width, height):
    image = Image.open(image_path)
    return image.resize((width, height))

# Titel och introduktion
st.title("Bygg ditt spartorn! 🏗️")
st.write("Välj åtgärder och se ditt torn växa medan du sparar energi, vatten eller hjälper klimatet!")
st.write("_💡Tips! Tryck på texterna bredvid klossarna för mer information kring åtgärden.💡_")


# Välj kategori
kategori = st.selectbox("Välj det område där du vill spara:", ["Klimat", "Vatten", "Energi"])

# Välj antal personer är ni i hushållet
persons = st.number_input("Hur många personer är ni i hushållet?", min_value=1, step=1)

# Klossar och besparingar baserat på kategori
klossar = {}
if kategori == "Klimat":
    klossar = {
        "Källsortera sopor": {"bild": "led.png", "besparing": 950, "info": "Genom att källsortera sopor istället för att lägga allt i brännbart kan mer material återvinnas."},
        "Buss istället för bil": {"bild": "led.png", "besparing": 438, "info": "Om du har 8 km enkelväg till jobbet och väljer att åka buss istället för bensinbil till jobbet blir det en tydlig vinst för klimatet."}, #16 km per dag i 250 arbetsdagar. Co2e eller co2? Bil = 2,507 kg co2 & 3,063 co2e. Buss = 0,756 co2 och 1,167 co2e.
        "Byt ut mjölken": {"bild": "led.png", "besparing": 75*persons, "info": "Svensken dricker i genomsnitt 1,75 liter mjölk i veckan och genom att byta ut mot havremjölk minskar du miljöpåverkan med 70%!"},
        "Second hand istället för nytt": {"bild": "led.png", "besparing": 1430, "info": "Kom på senare."}, 
        "Vegetarisk mat": {"bild": "led.png", "besparing": 987, "info": "Kom på senare."}, 

    }
elif kategori == "Vatten":
    klossar = {
        "Snålspola när du kissat": {"bild": "led.png", "besparing": 2920*persons, "info": "Om varje person använder snålspolning när hen har kissat halveras vattenförbrukning vid spolning."}, #Genomsnitt är kissa 5-8 gånger per dag. Säg 8 och 4 av dem är hemma. Snålspola är 2 liter istället för 4 l. 4*365=2920
        "Duscha 2 minuter kortare": {"bild": "led.png", "besparing": 300*persons, "info": "Genom att varje person duschar 2 minuter kortare sparas stora mängder vatten."}, 
        "Full tvättmaskin": {"bild": "led.png", "besparing": 789, "info": "Kom på senare."}, 
        "Diska utan rinnande vatten": {"bild": "led.png", "besparing": 1430, "info": "Kom på senare."}, 
        "Kallt vatten i kylen": {"bild": "led.png", "besparing": 450, "info": "Kom på senare."}, 


    }
elif kategori == "Energi":
    klossar = {
        "Använd vattenkokaren": {"bild": "led.png", "besparing": 50, "info": "Om du ersätter cirka 2 liter vattenkokning i kastrull med vattenkokare varje dag så sparar du 50 kWh/år."},
        "Frosta av frysen": {"bild": "led.png", "besparing": 50, "info": "En isig frys kan använda 50 kWh mer om året, jämfört med en avfrostad."},
        "Blockera inte elementen": {"bild": "led.png", "besparing": 600, "info": "Om en säng, soffa eller långa gardiner står framför elementen så kan värmen inte komma ut i rummet. Det kan i sin tur innebära att du upplever rum eller bostad som onödigt kalla, helt i onödan!"},
        "Timer på kaffekokaren": {"bild": "led.png", "besparing": 1430, "info": "Kom på senare."}, 
        "Släck när du går": {"bild": "led.png", "besparing": 140, "info": "Kom på senare."}, 

    }

# Ladda bilder (måste finnas i samma mapp som scriptet eller en webbadress)
bildmap = {}
for namn, data in klossar.items():
    bild = Image.open(data["bild"])
    bild = bild.resize((int(bild.width / 4), int(bild.height / 4)))  # Gör bilden mindre
    bildmap[namn] = bild

# Användaren väljer åtgärder
valda_klossar = st.multiselect("Välj dina åtgärder:", list(klossar.keys()))
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
# Visa rätt subheader baserat på kategori
if kategori == "Klimat":
    st.subheader("Ditt klimatspartorn")
elif kategori == "Vatten":
    st.subheader("Ditt vattenspartorn")
elif kategori == "Energi":
    st.subheader("Ditt energispartorn")

# Lägg till extra utrymme ovanför rubriken   
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

# Visa klossar som staplas
for index, kloss in enumerate(valda_klossar):
    bild_base64 = get_image_base64(klossar[kloss]["bild"])
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(
            f"""
            <div style="position: relative; text-align: left; margin-top: -50px; z-index: {len(valda_klossar) - index};">  <!-- Justera margin-top och z-index för att överlappa bilderna -->
                <img src="data:image/png;base64,{bild_base64}" style="width: 100px;">
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        if st.button(f"{kloss}", key=f"button_{index}"):
            st.session_state[f"info_{index}"] = not st.session_state.get(f"info_{index}", False)

        if st.session_state.get(f"info_{index}", False):
            st.info(klossar[kloss]["info"])

# Beräkna total besparing
total_besparing = sum(klossar[kloss]["besparing"] for kloss in valda_klossar)

st.markdown("<div style='height: 90px;'></div>", unsafe_allow_html=True)


# Landvetter till London och tillbaka = 1011 kg CO2e (2080 km) 
flyg = total_besparing/1011
tree = total_besparing/25 # ej kontrollerad källa
# Mobil - Iphone 15 = 13Wh batteri = 0,013 kWh batteri. 0,037 kg CO2e/kWh (Boverket) => 1 kg CO2 = 27 kWh => 27/0,013 = 2076,9230769230769230769230769231
mobil = total_besparing*2076.9230769230769230769230769231


# 1 liter vatten =  0,5 kronor
kronor_vatten = total_besparing*0.5
# En kaffemugg = 20 cl
kaffe = total_besparing/0.2
# Hink = 10 liter
hink = total_besparing/10
# Badkar = 200 liter
badkar = total_besparing/200


# 1 kwh = 1,5 kronor (dubbelkolla kwh värme och kwh el)
kronor_energi = total_besparing*1.5
# Dammsugare = 700 W = 0,7 kW
damm = total_besparing/0.7
# Elbil = 2 kWh/mil
elbil = total_besparing/2
# TV = 0,054 kWh/h
tv = total_besparing/0.054


# Snyggar till värden.
flyg = round(flyg,1)
flyg = format_number(flyg)
kronor_energi = round(kronor_energi)
kronor_energi = format_number(kronor_energi)
kronor_vatten = round(kronor_vatten)
kronor_vatten = format_number(kronor_vatten)
total_besparing = format_number(total_besparing)
kaffe = round(kaffe)
kaffe = format_number(kaffe)
hink = round(hink)
hink = format_number(hink)
tree = round(tree)
tree = format_number(tree)
mobil = round(mobil)
mobil = format_number(mobil)
badkar = round(badkar)
badkar = format_number(badkar)
damm = round(damm)
damm = format_number(damm)
elbil = round(elbil)
elbil = format_number(elbil)
tv = round(tv)
tv = format_number(tv)

# Visa olika meddelanden baserat på vald kategori
if kategori == "Klimat":
    st.write(f"### 🎉 Du sparar **{total_besparing}** kg koldioxid per år!")
elif kategori == "Vatten":
    st.write(f"### 🎉 Du sparar **{total_besparing}** liter vatten och {kronor_vatten} kronor per år!")
elif kategori == "Energi":
    st.write(f"### 🎉 Du sparar **{total_besparing}** kilowattimmar och {kronor_energi} kronor per år!")





kaffe = f"{kaffe} koppar kaffe"
kronor_vatten = f"{kronor_vatten} kronor varje år"
hink = f"{hink} hinkar med vatten"
flyg = f"{flyg} flygresor tur och retur till London"
tree = f"Koldioxidupptag från {tree} träd"
mobil = f"Ladda din mobiltelefon {mobil} gånger "
badkar = f"{badkar} fulla badkar med vatten"
damm = f"{damm} timmar dammsugning"
elbil = f"{elbil} mil med en elbil"
tv = f"{tv} timmar TV-tittande"

# Lista med bilder och beskrivningar för varje kategori
bilder_och_beskrivningar = {
    "Klimat": [
        {"bild": "flygplan.png", "beskrivning": flyg, "bredd": 200, "höjd": 150},
        {"bild": "tree.png", "beskrivning": tree, "bredd": 200, "höjd": 150},
        {"bild": "mobil.png", "beskrivning": mobil, "bredd": 200, "höjd": 150},
    ],
    "Vatten": [
        {"bild": "badkar.png", "beskrivning": badkar, "bredd": 200, "höjd": 150},
        {"bild": "hink.png", "beskrivning": hink, "bredd": 200, "höjd": 150},
        {"bild": "te.png", "beskrivning": kaffe, "bredd": 200, "höjd": 150},
    ],
    "Energi": [
        {"bild": "bil.png", "beskrivning": elbil, "bredd": 200, "höjd": 150},
        {"bild": "damm.png", "beskrivning": damm, "bredd": 200, "höjd": 150},
        {"bild": "tv.png", "beskrivning": tv, "bredd": 200, "höjd": 150},
    ],
}




# Visa tre bilder med text under längst ner baserat på vald kategori
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# Initialisera session state för knappen om den inte redan finns
if "visa_bilder" not in st.session_state:
    st.session_state.visa_bilder = False

# Funktion för att växla knappens tillstånd
def toggle_bilder():
    st.session_state.visa_bilder = not st.session_state.visa_bilder

# Bestäm knapptext baserat på tillståndet
knapp_text = "Se vad det motsvarar:" if not st.session_state.visa_bilder else "Dölj bilder"

# Lägg till en knapp för att visa/dölja bilderna
st.button(knapp_text, on_click=toggle_bilder)

# Visa eller dölj bilderna baserat på knappens tillstånd
if st.session_state.visa_bilder:
    cols = st.columns([1, 0.5, 1, 0.5, 1])  # Lägg till extra kolumner för mellanrum
    for i, item in enumerate(bilder_och_beskrivningar[kategori]):
        col = cols[i * 2]  # Använd varannan kolumn för bilderna
        bild = resize_image(item["bild"], item["bredd"], item["höjd"])
        col.image(bild)
        col.write(item["beskrivning"])


#st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
#st.write("Vill du skapa ett mål?")
#st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
#bra = st.slider("Välj hur många liter du vill spara per år", min_value=1, max_value=1000)
#st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
#good = f"För att spara {bra} liter vatten behöver du ..."
#st.write(good)
# Du behöver åka så här mycket kollektiv för att nå ditt mål (eller liknande)
