# Modules

import pyrebase
import streamlit as st

from datetime import datetime
from PIL import Image
from streamlit_option_menu import option_menu

from st_keyup import st_keyup

from training import *
from streamlit_pills import pills
from streamlit_lottie import st_lottie

def load_lottiefile(filepath: str):
  with open(filepath, "r") as f:
    return json.load(f)


import openai
openai.api_key = st.secrets['api_secret']

# Logo
logo = Image.open('images/Spotlit_Inc_Minimal_Logo_Icon.png')

#st.set_page_config(page_title='Spotlit', page_icon=logo)

PAGE_CONFIG = {
                "page_title": "Spotlit",
                "page_icon": logo,
                "layout": "centered"
}

st.set_page_config(**PAGE_CONFIG)




# Menu
Standard = """
<style>
#MainMenu{
  visibility:hidden;
}

[data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        
.css-6qob1r.e1fqkh3o3 {
      margin-top: -75px;
    }
    
    
.css-k1vhr4.egzxvld5 {
      margin-top: -65px;
      padding-top: 0rem;
      padding-bottom: 0rem;
      padding-left: 0rem;
      padding-right: 0rem;
    }
    
#footer{
  visibility:visible;
}

#footer:after{
  content: 'Copyright @ Spotlit 2023';
  display: block;
  position: relative;
  color: tomato;
}

</style>
"""

st.markdown(Standard, unsafe_allow_html=True)


# Imported Core 
sentence = ""

prediction = "" #predict_emotions(sentence)
probability = "" #get_prediction_proba(sentence)

ethics_tag = ""
ethics_reply = ""
nothing ="False"

# Configuration Key

firebaseConfig = {
  'apiKey': "AIzaSyDfrLczs2xsPDkPmYM4YQNw2tsb2Gc0EkY",
  'authDomain': "firelite-b0f86.firebaseapp.com",
  'projectId': "firelite-b0f86",
  'databaseURL': "https://firelite-b0f86-default-rtdb.europe-west1.firebasedatabase.app/",
  'storageBucket': "firelite-b0f86.appspot.com",
  'messagingSenderId': "251758260054",
  'appId': "1:251758260054:web:17668e92d17fe789e370f7",
  'measurementId': "G-MKH2N49D44"
}

# Authentication

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database

db = firebase.database()
storage = firebase.storage()

#st.sidebar.title("Spotlit")
st.sidebar.image("images/Spotlit_Inc_Complete_Logo.png")


# Login/SignUp

choice = st.sidebar.selectbox('SignIn/SignUp', ['🔓 SignIn', '🔐 SignUp'])

email = st.sidebar.text_input('📧 Enter your email address')
email = email.strip()

nickname = ""

password = st.sidebar.text_input('🚪  Enter your password', type='password')
password = password.strip()



if choice == '🔐 SignUp':
  handle = st.sidebar.text_input('Please input your nick name', value='default')
  handle = handle.strip()
  nickname = handle
  submit = st.sidebar.button('Join Spotlit!')
  
  spotlit_string = "🎇Spotlit Social - Empowering Safe Online Interactions"
    
  st.markdown("""
  <style>
  .big-font {
      font-size:28px !important;
      bold
  }
  </style>
  """, unsafe_allow_html=True)

  st.markdown(f'<p class="big-font"> <b> {spotlit_string} </b> </p>', unsafe_allow_html=True)
  
  signup_box = st.empty()

  st.success("🌞 Spotlit Team")   
  st.write("Welcome to Spotlit, a vibrant online community! Here, you can connect with others, share your thoughts, and explore new ideas. Join us and find fun, meaningful conversations and make new friends. Together, we can inspire, motivate and support each other. Come be a part of something special!")   
      
  st.info("🔆 Spotlit Vision")
  st.write("We are committed to building a brighter future, one where positivity reigns and negativity is not tolerated, where understanding and kindness replace insults, and knowledge and understanding supplant ignorance and superstition.")
    
  st.warning("⚡ Spotlit Mission")
  st.write("To be part of the new revolution of positivity and kindness. To embrace the power of knowledge and emotion to make the world a happier place together.")

    
  if submit:      
    user = auth.create_user_with_email_and_password(email, password)
    #st.success(f"Hello, {handle}, your account was successfully created 😉!")
    st.balloons()
  
    # Sign in 
    if email != "" and len(email) > 5 and password != "" and len(password) > 5 and handle != "default" and handle != "":
      user = auth.sign_in_with_email_and_password(email, password)
      db.child(user['localId']).child("Handle").set(handle)
      db.child(user['localId']).child("ID").set(user['localId'])
    
      signup_box.success(f"Hello, {handle}, your account was successfully created. Safely sign in via the sidebar dropdown select.")
      #st.info('Login via dropdown select')
      
    else:
      if handle == "default":
        signup_box.error(f"Stop joking! Get a real nick name, sign up and get going!")
      elif email == "" and len(email) < 5:
        signup_box.error(f"Use an actual email to sign up for a spotlit account!")
      elif password == "" and len(password) < 5:
        signup_box.error(f"Your password is too short. Create a long password!")
      else:
        signup_box.error(f"Stop joking! Be real, sign up and get going!")
      
      
    

if choice == '🔓 SignIn':
    login = st.sidebar.checkbox('🔑 SignIn')
    
    if not login:
    
      spotlit_string = "🎇Spotlit Social - Empowering Safe Online Interactions"
      
      st.markdown("""
      <style>
      .big-font {
          font-size:28px !important;
          bold
      }
      </style>
      """, unsafe_allow_html=True)

      st.markdown(f'<p class="big-font"> <b> {spotlit_string} </b> </p>', unsafe_allow_html=True)
        
      lottie_animation_a = load_lottiefile("animations/dancing-star.json")
      lottie_animation_b = load_lottiefile("animations/scrolling.json")
      lottie_animation_c = load_lottiefile("animations/prime-faya.json")

      col_a, col_b, col_c = st.columns([2,2,2])
      
      with col_a:
        fire_message1 = '<p style="font-family:sans-serif; color:Orange; font-size: 15px;">Hey, spotlitter! Did something come up your radar!</p>'
      
        st.markdown(fire_message1, unsafe_allow_html=True)
        st.write("")
        st_lottie(
          lottie_animation_a,
          speed=1,
          reverse=False,
          loop=True,
          quality="low", #medium #high
          height=None,
          width=None,
          key=1,
        )
        
      with col_b:
        fire_message2 = '<p style="font-family:sans-serif; color:Violet; font-size: 15px;">Wanna share the news, and show us what you are made of?</p>'
      
        st.markdown(fire_message2, unsafe_allow_html=True)
        st.write("")
        st_lottie(
          lottie_animation_b,
          speed=1,
          reverse=False,
          loop=True,
          quality="low", #medium #high
          height=250,
          width=None,
          key=2,
        )
        
      with col_c:
        fire_message3 = '<p style="font-family:sans-serif; color:Green; font-size: 15px;">Well, what are you waiting for? An alien app??</p>'
      
        st.markdown(fire_message3, unsafe_allow_html=True)
        st.write("")
        st_lottie(
          lottie_animation_c,
          speed=1,
          reverse=False,
          loop=True,
          quality="low", #medium #high
          height=200,
          width=180,
          key=3,
        )      
      
      spotlit_kick = '<p style="font-family:sans-serif; color:Green; font-size: 22px;">A little knowledge that acts is worth infinitely more than much knowledge that is idle. - Khalil Gibran</p>'
      fire_message = '<p style="font-family:Courier; color:Blue; font-size: 18px;">This quote emphasizes the importance of taking action and turning knowledge into tangible results.</p>'
      
      st.markdown(spotlit_kick, unsafe_allow_html=True)
      st.markdown(fire_message, unsafe_allow_html=True)
    
    
    if login:
      
      with st.sidebar:
        sio = option_menu(
          menu_title = None, #"Main Menu",
          options = ["Messages", "Settings", "About"],
          icons = ["chat-left-dots", "gear", "info-circle"],
          menu_icon = "cast",
          default_index = 1,
          orientation = "vertical",
          styles = {
            "container": {"padding": "0!important", "background-color": "#B2BEB5"},
            "icon": {"color": "#D8BFD8", "font-size": "20px"},
            "nav-link": {
                "font-size": "20px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#7393B3",
            },
            "nav-link-selected": {"background-color": "grey"},
          }
        )
      
      user = auth.sign_in_with_email_and_password(email, password)
      #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
      #bio = st.radio('Jump to', ['Shore', 'Currents', 'Recess' ])
      bio = option_menu(
        menu_title = None, #"Main Menu",
        options = ["Shore", "Currents", "Recess"],
        icons = ["bounding-box", "water", "exclude"],
        menu_icon = "cast",
        default_index = 0,
        orientation = "horizontal",
        styles = {
          "container": {"padding": "0!important", "background-color": "#CBC3E3"},
          "icon": {"color": "#D8BFD8", "font-size": "25px"},
          "nav-link": {
              "font-size": "25px",
              "text-align": "left",
              "margin": "0px",
              "--hover-color": "#AA98A9",
          },
          "nav-link-selected": {"font-size": "24px", "background-color": "#E6E6FA"},
        }
      )
      

      
# Recess
      if bio == 'Recess':
        # Check for image
        nImage = db.child(user['localId']).child("Image").get().val()
        
        # Image found
        if nImage is not None:
          # We plan to store all our image under the child image
          Image = db.child(user['localId']).child("Image").get()
          
          for img in Image.each():
            img_choice = img.val()
            
            # st.write(img_choice)
            st.image(img_choice)
            # exp = st.beta_expander('Change Bio and Image')
            exp = st.expander('Change Bio and Image')
            
            # User plan to change profile picture
            with exp:
              
              newImgPath = st.text_input('Enter full path of your profile image')
              upload_new = st.button('Upload')
              
              if upload_new:
                uid = user['localId']
                fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                
                db.child(user['localId']).child("Image").push(a_imgdata_url)
                st.success('Success')
                
                
        # If there is no image
        else:
          st.info("No profile picture yet")
          newImgPath = st.text_input('Enter full path of your profile picture')
          upload_new = st.button('Upload')
          
          if upload_new:
            uid = user['localId']
            # Store initiated bucket in firebase
            fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
            
            # Get the url for easy access
            a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
            
            # Put it in our real time database 
            db.child(user['localId']).child("Image").push(a_imgdata_url)
            
            
            
# Shore
      elif bio == 'Shore':
        col1, col2, col3 = st.columns([4, 4, 4])
        
        # Column for profile picture
        with col1:
          nImage = db.child(user['localId']).child("Image").get().val()
          
          if nImage is not None:
            val = db.child(user['localId']).child("Image").get()
            
            for img in val.each():
              img_choice = img.val()
              
            st.image(img_choice, use_column_width=True)
                        
          else:
            st.info("No profile picture yet. Go to Edit Profile and choose one!")
            
          selected = pills("", ["Crackle", "Fact-Check",  "Look-Up", "Message"], ["🦜", "🕵️", "🔎", "💬"])
          #post = st.text_area("", placeholder = "light a spot ...", key="input", height=1, label_visibility="hidden")
          
          if "temp" not in st.session_state:
            st.session_state["temp"] = ""
           
          def clear_text():
                st.session_state["temp"] = st.session_state["text"]
                st.session_state["text"] = ""       
            
          post = st.text_input("Let's light a spot 🔥!", max_chars = 100, key="text")
          
          if selected == "Crackle":
            button_clicked = st.button("🦜 Crackle", type = "primary", on_click=clear_text)
            post = st.session_state["temp"]
            
          elif selected == "Fact-Check":
              button_clicked = st.button("🕵️ Fact-Check", on_click=clear_text)
              post = st.session_state["temp"]              
          elif selected == "Look-Up":
              button_clicked = st.button("🔎 Look-Up", on_click=clear_text) 
              post = st.session_state["temp"] 
          else:
              button_clicked = st.button("💬 Message", on_click=clear_text) 
              post = st.session_state["temp"]
              message = post 
          
        if button_clicked: #add_post:
          if selected == "Crackle":
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H: %M: %S")
            
            post = {
              'Post' : post,
              'Timestamp' : dt_string
            }
            
            st.balloons()
            
            #Crackle Section
            sentence = tokenize(sentence)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            
                            
            if prob.item() > 0.75:
              for intent in intents['intents']:
                  if tag == intent['tag']:
                    # Generating a random response from neural net
                    sentence = random.choice(intent['responses'])
                                                
                    if intent['tag'] == "insult":
                        #st.error("Insult detected ⋯")
                        ethics_tag = "🙅‍♂️ Insult detected"
                        #st.write(f" ❌ Kindly, stop the {intent['tag']}")
                        ethics_reply = f"Stop the {intent['tag']}"
                        
                    
                    elif intent['tag'] == "cursewords":
                        #st.error("Curseword detected ⋯")
                        ethics_tag = "👀 Curseword detected"
                        #st.write(f" ❌ Kindly, do not use {intent['tag']}")
                        ethics_reply = f"Don't use {intent['tag']}"
                    
                    else:
                        nothing = "True"
                        # #st.success("No moral ethics violation")
                        # ethics_tag = "👍 Great moral ethics"
                        # #st.write(" 👌 Hey there .. spotlitter, keep up!")
                        # ethics_reply = f"Keep up!"
                        
                        if post['Post'] != "":
                          results =db.child(user['localId']).child("Posts").push(post)
                          sentence = post["Post"]
                        else:
                          sentence = "None"
                        
            else:
              ethics_tag = "👍 Great work spotlitter!"
              ethics_reply = f"Peace."
              
              if post['Post'] != "":
                results =db.child(user['localId']).child("Posts").push(post)
                sentence = post["Post"]
              else:
                sentence = "None"
            
          elif selected == "Fact-Check":
            fact = post
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H: %M: %S")
            
            fact = {
              'Fact' : fact,
              'Timestamp' : dt_string
            }
            
            if fact['Fact'] != "":
              results =db.child(user['localId']).child("Facts").push(fact)
              sentence = fact["Fact"]
            else:
              sentence = None
              
          elif selected == "Look-Up":
            lookup = post
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H: %M: %S")
            
            lookup = {
              'LookUp' : lookup,
              'Timestamp' : dt_string
            }
            
            if lookup['LookUp'] != "":
              results =db.child(user['localId']).child("LookUp").push(lookup)
              sentence = lookup["LookUp"]
            else:
              sentence = None
          
          else:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H: %M: %S")
            #message = post
            
            message = {
              'Message' : message,
              'Timestamp' : dt_string
            }
                        
            # if message['Message'] != "":
            #   results =db.child(user['localId']).child("Messages").push(message)
            #   sentence = message["Message"]
            # else:
            #   sentence = "None"
              
            # prediction = predict_emotions(sentence)
            # probability = get_prediction_proba(sentence)
            
            # emoji_icon = emotions_emoji_dict[prediction]
            
            st.balloons()
            
            #sentence = post
            
            ######################
            
            #Crackle Section
            sentence = tokenize(sentence)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
                            
            if prob.item() > 0.75:
              for intent in intents['intents']:
                  if tag == intent['tag']:
                    # Generating a random response from neural net
                    sentence = random.choice(intent['responses'])
                                                
                    if intent['tag'] == "insult":
                        #st.error("Insult detected ⋯")
                        ethics_tag = "🙅‍♂️ Insult detected"
                        #st.write(f" ❌ Kindly, stop the {intent['tag']}")
                        ethics_reply = f"Stop the {intent['tag']}"
                        
                    
                    elif intent['tag'] == "cursewords":
                        #st.error("Curseword detected ⋯")
                        ethics_tag = "👀 Curseword detected"
                        #st.write(f" ❌ Kindly, do not use {intent['tag']}")
                        ethics_reply = f"Don't use {intent['tag']}"
                    
                    else:
                        nothing = "True"
                        # #st.success("No moral ethics violation")
                        # ethics_tag = "👍 Great moral ethics"
                        # #st.write(" 👌 Hey there .. spotlitter, keep up!")
                        # ethics_reply = f"Keep up!"
                        
                        if message['Message'] != "":
                          results =db.child(user['localId']).child("Messages").push(message)
                          sentence = message["Message"]
                        else:
                          sentence = "None"
                        
            else:
              ethics_tag = "👍 Great work spotlitter!"
              ethics_reply = f"Peace."
              
              if message['Message'] != "":
                results =db.child(user['localId']).child("Messages").push(message)
                sentence = message["Message"]
              else:
                sentence = "None"
              
              
            
            #######################################
              
          
        # Column for post display
        with col2:
          if button_clicked: #add_post:
            if selected == "Crackle":
              all_posts = db.child(user['localId']).child('Posts').get()
              
              if all_posts.val() is not None:
                for Posts in reversed(all_posts.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Posts.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Posts.val()['Post']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')
              
            elif selected == "Fact-Check":
              all_facts = db.child(user['localId']).child('Facts').get()
              
              if all_facts.val() is not None:
                for Facts in reversed(all_facts.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Facts.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Facts.val()['Fact']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')
            
            elif selected == "Look-Up":
              all_lookups = db.child(user['localId']).child('LookUp').get()
              
              if all_lookups.val() is not None:
                for LookUp in reversed(all_lookups.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {LookUp.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{LookUp.val()['LookUp']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')    
              
            else:
              all_messages = db.child(user['localId']).child('Messages').get()
              
              if all_messages.val() is not None:
                for Messages in reversed(all_messages.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Messages.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Messages.val()['Message']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')
            
          else:
            if selected == "Crackle":
              all_posts = db.child(user['localId']).child('Posts').get()
                
              if all_posts.val() is not None:
                for Posts in reversed(all_posts.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Posts.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Posts.val()['Post']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')   
             
            elif selected == "Fact-Check":
              all_facts = db.child(user['localId']).child('Facts').get()
              
              if all_facts.val() is not None:
                for Facts in reversed(all_facts.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Facts.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Facts.val()['Fact']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '') 
            
            elif selected == "Look-Up":
              all_lookups = db.child(user['localId']).child('LookUp').get()
              
              if all_lookups.val() is not None:
                for LookUp in reversed(all_lookups.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {LookUp.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{LookUp.val()['LookUp']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')
            
            else:
              all_messages = db.child(user['localId']).child('Messages').get()
              
              if all_messages.val() is not None:
                for Messages in reversed(all_messages.each()):
                  # st.write(Posts.key())
                                                          
                  res_box = st.container()
                  #res_box.markdown("----")
                  #res_box.write("<style> <div> </style>", unsafe_allow_html=True)
                  res_box.write(f"_``` {Messages.val()['Timestamp']} ```_ \n >  **:white[{'▪️ '}{Messages.val()['Message']}]** ")
                  #res_box.write(f">  **:white[{':pencil'}{Posts.val()['Post']}]**")
                  #res_box.write("<style> </div> </style>", unsafe_allow_html=True)
                  res_box.write("<style> <br /> </style>", unsafe_allow_html=True)
                  #res_box.markdown("--")
                  #res_box.write(Posts.val())
                  
                  #st.code(Posts.val(), language = '')
              
              
              
        with col3:
          #st.write("I love this app!!!!")
          #Crackle Display
          prediction = predict_emotions(sentence)
          probability = get_prediction_proba(sentence)
          emoji_icon = emotions_emoji_dict[prediction]
                     
          i_prediction = ""
          spotshot = "💨"
          
          if button_clicked: #add_post:
            if selected == "Crackle":
          
              if prediction == "anger":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ')
             
              elif prediction == "disgust":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "fear":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "happy":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "joy":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "neutral":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "sad":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "sadness":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "shame":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              else:
                prediction = "anxiety"
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
            elif selected == "Fact-Check":
              st.success("🎇 Is this a fact?")
              user_input = f"Is this a fact (yes or no): ' {fact['Fact']} ' and expound in about thirty words!"
              #st.markdown("----")
              res_box = st.empty()
              
              report = []
              
              for resp in openai.Completion.create(model='text-davinci-003',
                                      prompt=user_input,
                                      max_tokens=1024,
                                      temperature=0.5,
                                      stream=True):
              
                  # join method to concatenate the elements of the list
                  # into a single string,
                  # then strip out any empty strings
                  
                  report.append(resp.choices[0].text)
                  result = "".join(report).strip()
                  # result = result.replace("*", "")
                  # result = result.replace("\n", "\n")
                  # result = result.replace("?", "? \n")
                  # result = result.replace("!", "? \n")
                  res_box.markdown(f' {result} ')

              st.info("✨ What I know?")
              user_input = f"Expound in about forty words what you know about? ' {fact['Fact']} ' !"
              #st.markdown("----")
              info_box = st.empty()
              
              report = []
              
              for resp in openai.Completion.create(model='text-davinci-003',
                                      prompt=user_input,
                                      max_tokens=1024,
                                      temperature=0.5,
                                      stream=True):
              
                  # join method to concatenate the elements of the list
                  # into a single string,
                  # then strip out any empty strings
                  
                  report.append(resp.choices[0].text)
                  result = "".join(report).strip()
                  # result = result.replace("*", "")
                  # result = result.replace("\n", "\n")
                  # result = result.replace("?", "? \n")
                  # result = result.replace("!", "? \n")
                  info_box.markdown(f' {result} ')
              
            elif selected == "Look-Up": 
              st.success("🧩 General Knowledge")
              user_input = f"Who/When/What is : ' {lookup['LookUp']} ' ? Informatively, shed some light in about thirty words!"
              #st.markdown("----")
              res_box = st.empty()
              
              report = []
              
              for resp in openai.Completion.create(model='text-davinci-003',
                                      prompt=user_input,
                                      max_tokens=1024,
                                      temperature=0.5,
                                      stream=True):
              
                  # join method to concatenate the elements of the list
                  # into a single string,
                  # then strip out any empty strings
                  
                  report.append(resp.choices[0].text)
                  result = "".join(report).strip()
                  # result = result.replace("*", "")
                  # result = result.replace("\n", "\n")
                  # result = result.replace("?", "? \n")
                  # result = result.replace("!", "? \n")
                  res_box.markdown(f' {result} ')

              st.info("🥏 Detailed History")
              user_input = f"In about forty words, what is the history of ' {lookup['LookUp']} ' ?"
              #st.markdown("----")
              info_box = st.empty()
              
              report = []
              
              for resp in openai.Completion.create(model='text-davinci-003',
                                      prompt=user_input,
                                      max_tokens=1024,
                                      temperature=0.5,
                                      stream=True):
              
                  # join method to concatenate the elements of the list
                  # into a single string,
                  # then strip out any empty strings
                  
                  report.append(resp.choices[0].text)
                  result = "".join(report).strip()
                  # result = result.replace("*", "")
                  # result = result.replace("\n", "\n")
                  # result = result.replace("?", "? \n")
                  # result = result.replace("!", "? \n")
                  info_box.markdown(f' {result} ')
            
            else:
              if prediction == "anger":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ')
             
              elif prediction == "disgust":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "fear":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "happy":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "joy":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "neutral":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "sad":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "sadness":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              elif prediction == "shame":
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice / Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
              else:
                prediction = "anxiety"
                i_prediction = prediction
                #st.write(f" Prediction : {prediction}")
                ethics_box = st.container()
                
                if nothing == "True":
                  st.success(f"👃 Ethics Ruler")
                  
                  user_input = f"Naturally, tell me the problem to '{sentence}' online and give me ethical advice in less than or exactly ten words."
                  #st.markdown("----")
                  ethics_box = st.empty()
                  starter = ""
                  starter = "📝..."
                  ethics_box.markdown(f' {starter} ')
                  report = []
                  
                  for resp in openai.Completion.create(model='text-davinci-003',
                                          prompt=user_input,
                                          max_tokens=120,
                                          temperature=0.5,
                                          stream=True):
                  
                      # join method to concatenate the elements of the list
                      # into a single string,
                      # then strip out any empty strings
                      
                      report.append(resp.choices[0].text)
                      t_result = "".join(report).strip()
                      # result = result.replace("*", "")
                      # result = result.replace("\n", "\n")
                      # result = result.replace("?", "? \n")
                      # result = result.replace("!", "? \n")
                      ethics_box.markdown(f' {t_result} ')
                
                if nothing != "True":
                  st.success(f"⚠️ Ethics Check")
                  st.write(f"*_{ethics_tag}_*: *{ethics_reply}*")
                  #st.write(f" *{ethics_reply}*")
                st.warning(f"🤒 Emotion Meter")
                st.write(f"{spotshot} _{prediction}_: {emoji_icon}")
                st.info("🎯 Certitude Meter")
                st.write("⚓ Surety: {:.2f} %".format(np.max(probability)*100))
                
                st.success("💡 Advice Tips:")                 
                            
                user_input = f"Specifically, tell me three socially better ways to say {sentence} if it is triggered by emotion {i_prediction} "
                #st.markdown("----")
                ai_box = st.empty()
                starter = ""
                starter = "📝..."
                ai_box.markdown(f' {starter} ')
                report = []
                
                for resp in openai.Completion.create(model='text-davinci-003',
                                        prompt=user_input,
                                        max_tokens=120,
                                        temperature=0.5,
                                        stream=True):
                
                    # join method to concatenate the elements of the list
                    # into a single string,
                    # then strip out any empty strings
                    
                    report.append(resp.choices[0].text)
                    result = "".join(report).strip()
                    # result = result.replace("*", "")
                    # result = result.replace("\n", "\n")
                    # result = result.replace("?", "? \n")
                    # result = result.replace("!", "? \n")
                    ai_box.markdown(f' {result} ') 
        
          else:
            st.success("🌞 Random Facts")
            user_input = f"Induct me three random facts from a random discipline of knowledge in about thirty words!"
            #st.markdown("----")
            res_box = st.empty()
            
            report = []
            
            for resp in openai.Completion.create(model='text-davinci-003',
                                    prompt=user_input,
                                    max_tokens=1024,
                                    temperature=0.87,
                                    stream=True):
            
                # join method to concatenate the elements of the list
                # into a single string,
                # then strip out any empty strings
                
                report.append(resp.choices[0].text)
                result = "".join(report).strip()
                # result = result.replace("*", "")
                # result = result.replace("\n", "\n")
                # result = result.replace("?", "? \n")
                # result = result.replace("!", "? \n")
                res_box.markdown(f' {result} ')

            st.info("🌟 Bright Day")
            user_input = f"Each in new line, give me three inspiring quotes from arbitrary historical figures!"
            #st.markdown("----")
            info_box = st.empty()
            
            report = []
            
            for resp in openai.Completion.create(model='text-davinci-003',
                                    prompt=user_input,
                                    max_tokens=1024,
                                    temperature=0.93,
                                    stream=True):
            
                # join method to concatenate the elements of the list
                # into a single string,
                # then strip out any empty strings
                
                report.append(resp.choices[0].text)
                result = "".join(report).strip()
                # result = result.replace("*", "")
                # result = result.replace("\n", "\n")
                # result = result.replace("?", "? \n")
                # result = result.replace("!", "? \n")
                info_box.markdown(f' {result} ')
    
              
              
              
# Currents 
      else:
        all_users = db.get()
        
        res = []
        
        # Store all the users handle name 
        for users_handle in all_users.each():
          k = users_handle.val()["Handle"]
          res.append(k)
          
        # Total users 
        nl = len(res)
        
        st.write('Total users here: ' + str(nl))
        
        # Allow the user tochoose which other user he/she wants to see
        
        choice = st.selectbox('My Colleagues', res)
        push = st.button('Show Profile')
        
        # Show the choosen profile
        if push:
          for users_handle in all_users.each():
            k = users_handle.val()["Handle"]
            
            if k == choice:
              lid = users_handle.val()["ID"]
              
              handlename = db.child(lid).child("Handle").get().val()
              
              st.markdown(handlename, unsafe_allow_html=True)
              
              nImage = db.child(lid).child("Image").get().val()
              
              if nImage is not None:
                val = db.child(lid).child("Image").get()
                for img in val.each():
                  img_choice = img.val()
                  st.image(img_choice)
                  
              else:
                st.info("No profile picture yet. Go to Edit Profile and choose one!")
                
                
              # All posts 
              all_posts = db.child(lid).child("Posts").get()
              
              if all_posts.val() is not None:
                for Posts in reversed(all_posts.each()):
                  st.code(Posts.val(), language = '')