from firebase import firebase
import streamlit as st
import datetime, pytz, time

st.set_page_config("Simple Chat")

start_time = time.time()

messages = []

if ("password" not in st.session_state):
	password = st.text_input("Mật khẩu")
	if (st.button("Đăng nhập")):
		if (password == st.secrets["password"]):
			st.session_state["password"] = password
			st.rerun()

if (("username" not in st.session_state) and ("password" in st.session_state)):
	user_name = st.text_input("Tên người dùng")
	if (st.button("Vào chat")):
		if (user_name):
			st.session_state["username"] = user_name
			st.rerun()

if ("username" in st.session_state):
	chat = st.chat_input("Tin nhắn")

	firebase_app = firebase.FirebaseApplication(st.secrets["database_url"], None)
	temp_messages = firebase_app.get("/messages", None)

	if (temp_messages):
		if ("messages" not in st.session_state):
			st.session_state["messages"] = temp_messages
		else:
			st.session_state["messages"].extend(temp_messages[len(st.session_state["messages"]):])
	else:
		st.session_state["messages"] = messages

	if (chat):
		user_name = st.session_state["username"]
		date_time = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
		date_time_str = date_time.strftime("%d/%m/%Y %H:%M:%S")
		st.session_state["messages"].append(f"{date_time_str}|{user_name}|{chat}")
		firebase_app.put("/","messages", st.session_state["messages"])

	for message in st.session_state["messages"]:
		message = message.split('|')
		with st.chat_message(message[1]):
			st.write(message[1])
			st.text(message[0])
			st.write(message[2])

	end_time = time.time()

	st.info(f"Thời gian chạy: {(end_time - start_time):.3f}")
	
	time.sleep(1)
	st.rerun()
