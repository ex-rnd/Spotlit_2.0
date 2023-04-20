from training import *
from streamlit_pills import pills

import openai
openai.api_key = st.secrets['api_secret']

# !!!!!!!! --- Streamlit App --- !!!!!!!!

# Main Function 

def main():
    st.title("Spotlit")
    menu = ["Home", "Monitor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        #st.subheader("Spotlit - Emotion Aware Chat Assist")
        
        #col_1, col_2 = st.columns([3,2])
        
        #with st.form(key='emotion_clf_form'):
        #with col_1:
        
        #sentence = st.text_area("Type Here")
        
        selected = pills("", ["Crackle", "Look-Up",  "Fact-Check", "AI Chat"], ["🦜", "🔎", "🕵️", "🤖"])
        sentence = st.text_area("", placeholder = "light a spot ...", key="input", height=1, label_visibility="hidden")
        
        #selected = pills("", ["Crackle!", "Look-Up",  "Fact-Check"], ["🦜", "🔎", "🕵️"])
        
        #submit_text = st.button(label='Submit')
            
            
            #submit_text = st.form_submit_button(label='Submit')
            
        if selected == "Crackle":
            button_clicked = st.button("🦜 Crackle", type = "primary")
        elif selected == "Look-Up":
            button_clicked = st.button("🔎 Look-Up")
        elif selected == "Fact-Check":
            button_clicked = st.button("🕵️ Fact-Check") 
        else:
            button_clicked = st.button("💬 Message") 
                
            
        if button_clicked:
            
            if selected == "Crackle":         
            
                col1, col2 = st.columns(2)
                
                # Apply Functions - Other Functions
                prediction = predict_emotions(sentence)
                probability = get_prediction_proba(sentence)
                
                with col1:
                    # hsentence = ""
                    # hselected = pills("", ["Look Upf", "Fact Checkf",  "Cracklef"], ["😮‍💨", "😶‍🌫️", "😮‍💨"])
                    # hsentence = st.text_area("", placeholder = "light a spot ...", key="hinput", height=1, label_visibility="hidden")
                    # #st.success("User-Text Input")
                    i_sentence = ""
                    #st.write(sentence)
                    
                    #st.success("Chat-Assist Reply")
                    sentence = tokenize(sentence)
                    X = bag_of_words(sentence, all_words)
                    X = X.reshape(1, X.shape[0])
                    X = torch.from_numpy(X).to(device)
                    
                    output = model(X)
                    _, predicted = torch.max(output, dim=1)
                    tag = tags[predicted.item()]
                    
                    probs = torch.softmax(output, dim=1)
                    prob = probs[0][predicted.item()]
                    
                    if prediction == "anger":
                        i_sentence = "You are angry!"
                    elif prediction == "disgust":
                        i_sentence = "You are disgusted!"
                    elif prediction == "fear":
                        i_sentence = "You are afraid!"
                    elif prediction == "happy":
                        i_sentence = "You are happy!"
                    elif prediction == "joy":
                        i_sentence = "You are joyful"
                    elif prediction == "neutral":
                        i_sentence = "You are neutral!"
                    elif prediction == "sad":
                        i_sentence = "You are sad!"
                    elif prediction == "sadness":
                        i_sentence = "You are feeling sadness!"
                    elif prediction == "shame":
                        i_sentence = "You are ashamed!"
                    else:
                        i_sentence = "You are surprised"
                    
                    if prob.item() > 0.75:
                        for intent in intents['intents']:
                            if tag == intent['tag']:
                                
                                sentence = random.choice(intent['responses'])
                            
                                if intent['tag'] == "insult":
                                    st.error("Insult detected ⋯")
                                    st.write(f" ❌ Kindly, stop the {intent['tag']}")
                                
                                elif intent['tag'] == "cursewords":
                                    st.error("Curseword detected ⋯")
                                    st.write(f" ❌ Kindly, do not use {intent['tag']}")
                                
                                else:
                                    st.success("No moral ethics violation")
                                    st.write(" 👌 Hey there .. spotlitter, keep up!")
                                
                                #st.write(intent['tag'])                        
                                                                  
                                                                
                    else:
                        sentence = "I do not understand ..."              
                                                    
                    
                    #st.write(f"{sentence}")
                    
                    
                    
                    emoji_icon = emotions_emoji_dict[prediction]
                    
                    i_sentence = i_sentence  
                    spotshot = "💨"                            
                    
                    if prediction == "anger":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Suggestions:")                 
                                    
                        user_input = f"Give me three random soothing suggestions for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')                       
                                                    
                    elif prediction == "disgust":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Suggestions:")                 
                                    
                        user_input = f"Give me three random charismatic suggestions for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "fear":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Suggestions:")                 
                                    
                        user_input = f"Give me three bold suggestions for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "happy":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three happy tips for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "joy":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three joyous sentences for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "neutral":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Tell me something very funny {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "sad":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three hopeful tips for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "sadness":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three exciting suggestions for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    elif prediction == "shame":
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three assertive statements for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')
                        
                        
                    else:
                        st.success("Emotion Detection:")
                        st.write(f"{spotshot} {i_sentence}: {emoji_icon}")
                        st.success("AI Confidence:")
                        st.write("🎯 Confidence: {}".format(np.max(probability)))     
                        
                        st.success("Rational Chat Tips:")                 
                                    
                        user_input = f"Give me three hilarious responses for {sentence}"
                        #st.markdown("----")
                        res_box = st.empty()
                        starter = ""
                        starter = "Try saying..."
                        res_box.markdown(f' {starter} ')
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
                            res_box.markdown(f' {result} ')          
                    
                    
                    ####
                    st.success("Emotion Prediction")
                    proba_dataset = pd.DataFrame(probability, columns=pipeline.classes_)
                    # st.write(proba_dataset.T)
                    proba_dataset_clean = proba_dataset.T.reset_index()
                    proba_dataset_clean.columns = ["emotions", "probability"]
                    
                    figure = alt.Chart(proba_dataset_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
                    st.altair_chart(figure, use_container_width=True)
                    
                    ####
                    
                    
                    
                    
                with col2:
                    pass
                    # st.success("Emotion Probability")
                    # # st.write(probability)
                    # proba_dataset = pd.DataFrame(probability, columns=pipeline.classes_)
                    # # st.write(proba_dataset.T)
                    # proba_dataset_clean = proba_dataset.T.reset_index()
                    # proba_dataset_clean.columns = ["emotions", "probability"]
                    
                    # figure = alt.Chart(proba_dataset_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
                    # st.altair_chart(figure, use_container_width=True)
                  
            if selected == "Fact-Check":
                user_input = f"Is this a fact (yes or no): ' {sentence} ' and please expound in summary"
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
            
            if selected == "Look-Up":
                user_input = f"Give me a summary of {sentence}"
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
             
            if selected == "Message":
                pass
            
    elif choice == "Monitor":
        st.subheader("Monitor App")
        
        
    else:
        st.subheader("About")
        
        
        
if __name__ == '__main__':
    main()